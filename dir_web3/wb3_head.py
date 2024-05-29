########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# types
from typing import Union, Optional
from web3.types import HexBytes

# libraries
import random
import asyncio
from web3 import Web3

# dir: func
from web3.middleware import geth_poa_middleware
from dir_common.cmn_func import read_json_from_file


########################################################################################################################
# GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS
########################################################################################################################

# globals: networks with ETH native token
NETWORKS_ETH_LIST = ['Arbitrum One', 'Base', 'Optimism', 'Scroll']

# globals: networks with only Legacy transactions type
NETWORKS_LEGACY_LIST = ['Scroll']

# globals: eth rpc
RPC_ETH = 'https://rpc.ankr.com/eth'

# globals: Celo gas
GAS_CELO_2B = 2000000000
GAS_CELO_10B = 10000000000


########################################################################################################################
# CLASS: CLIENT # CLASS: CLIENT # CLASS: CLIENT # CLASS: CLIENT # CLASS: CLIENT # CLASS: CLIENT # CLASS: CLIENT # CLASS:
########################################################################################################################

# class: Client
class Client:
    filename_abi_erc20 = 'dir_web3/storage/ERC20.json'
    abi_erc20 = read_json_from_file(filename_abi_erc20)

    def __init__(self, private_key: str, network_rpc: str, network_name: str, proxy: Optional[str] = None):
        """
        Initializing class parameters

        :param private_key: private key to network wallet
        :param network_rpc: url link to rpc network connector
        :param network_name: the name of the rcp network
        """
        self.private_key = private_key
        self.url_rpc = network_rpc
        self.name_network = network_name
        self.proxy = proxy

        if proxy is not None:
            self.w3 = Web3(
                provider=Web3.HTTPProvider(
                    endpoint_uri=self.url_rpc,
                    request_kwargs={'proxies': {'http': f'http://{proxy}', 'https': f'http://{proxy}'}}
                ),
            )
        else:
            self.w3 = Web3(
                provider=Web3.HTTPProvider(
                    endpoint_uri=self.url_rpc
                ),
            )
        self.address = Web3.to_checksum_address(self.w3.eth.account.from_key(private_key=private_key).address)

    ####################################################################################################################
    # IS CONNECTED # IS CONNECTED # IS CONNECTED # IS CONNECTED # IS CONNECTED # IS CONNECTED # IS CONNECTED # IS CONNEC
    ####################################################################################################################

    # function: checking connection
    async def is_connected(self, ) -> (int, Union[bool, Exception]):
        try:
            if self.w3.is_connected():
                return 0, True
            else:
                return -1, False
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # GET BALANCE NATIVE # GET BALANCE NATIVE # GET BALANCE NATIVE # GET BALANCE NATIVE # GET BALANCE NATIVE # GET BALAN
    ####################################################################################################################

    # function: getting account balance in native token
    async def get_balance_native(self, ) -> (int, Union[int, Exception]):
        try:
            contract = self.w3.eth.account.from_key(private_key=self.private_key)
            wallet_address = Web3.to_checksum_address(contract.address)
            balance = int(self.w3.eth.get_balance(wallet_address))
            return 0, balance
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # SEND TRANSACTION # SEND TRANSACTION # SEND TRANSACTION # SEND TRANSACTION # SEND TRANSACTION # SEND TRANSACTION #
    ####################################################################################################################

    # function: sending transaction
    async def send_transaction(
            self, address_to: str, address_from: str = None, data=None, value=None,
            gas_increase_gas: float = None, gas_increase_base: float = None, gas_eth_max_gwei: int = None,
    ) -> (int, Union[HexBytes, Exception]):
        try:
            address_from = self.address if (not address_from) else address_from
            gas_increase_gas = 1.5 if (gas_increase_gas is None) else gas_increase_gas
            gas_increase_base = 1.5 if (gas_increase_base is None) else gas_increase_base

            if (self.name_network in NETWORKS_ETH_LIST) and (gas_eth_max_gwei is not None):
                while True:
                    result, msg = await self.get_eth_gas_price(self.proxy)
                    if result == 0:
                        if msg > gas_eth_max_gwei:
                            await asyncio.sleep(random.randint(10, 20))
                        else:
                            break
                    else:
                        return -1, Exception(f'Some troubles in function get_eth_gas_price with error: {msg}')

            transaction_parameters = {
                'chainId': self.w3.eth.chain_id,
                'nonce': self.w3.eth.get_transaction_count(self.address),
                'from': Web3.to_checksum_address(address_from),
                'to': Web3.to_checksum_address(address_to),
            }
            if self.name_network in NETWORKS_LEGACY_LIST:
                transaction_parameters['gasPrice'] = self.w3.eth.gas_price
            else:
                maxPriorityFeePerGas, maxFeePerGas = await self.get_EIP_1559_gas_parameters(gas_increase_base)
                transaction_parameters['maxPriorityFeePerGas'] = maxPriorityFeePerGas
                transaction_parameters['maxFeePerGas'] = maxFeePerGas
            if data:
                transaction_parameters['data'] = data
            if value:
                transaction_parameters['value'] = value
            try:
                gas_estimated = int(self.w3.eth.estimate_gas(transaction_parameters) * gas_increase_gas)
                transaction_parameters['gas'] = gas_estimated
            except Exception as E:
                return -1, Exception(f'Transaction was failed with error: {E}')

            sign = self.w3.eth.account.sign_transaction(transaction_parameters, self.private_key)
            transaction_hash = self.w3.eth.send_raw_transaction(sign.rawTransaction)
            return 0, transaction_hash
        except Exception as E:
            return -1, Exception(f'Could not sent the transaction with error: {E}')

    ####################################################################################################################
    # VERIFY TRANSACTION # VERIFY TRANSACTION # VERIFY TRANSACTION # VERIFY TRANSACTION # VERIFY TRANSACTION # VERIFY TR
    ####################################################################################################################

    # function: verifying transaction
    async def verify_transaction(self, transaction_hash: HexBytes) -> (int, Union[bool, Exception]):
        try:
            data = self.w3.eth.wait_for_transaction_receipt(transaction_hash=transaction_hash, timeout=1000)
            if ('status' in data) and (data['status'] == 1):
                return 0, True
            else:
                return 0, False
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # GET ETH GAS PRICE # GET ETH GAS PRICE # GET ETH GAS PRICE # GET ETH GAS PRICE # GET ETH GAS PRICE # GET ETH GAS PR
    ####################################################################################################################

    # function: getting gas price for ETH chain (in gwei)
    @staticmethod
    async def get_eth_gas_price(proxy: Optional[str]) -> (int, Union[int, Exception]):
        try:
            if proxy is not None:
                w3_eth = Web3(
                    provider=Web3.HTTPProvider(
                        endpoint_uri=RPC_ETH,
                        request_kwargs={'proxies': {'http': f'http://{proxy}', 'https': f'http://{proxy}'}}
                    ),
                )
            else:
                w3_eth = Web3(provider=Web3.HTTPProvider(endpoint_uri=RPC_ETH))
            return 0, int(Web3.from_wei(int(w3_eth.eth.gas_price), 'gwei'))
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # GET EIP 1559 GAS # GET EIP 1559 GAS # GET EIP 1559 GAS # GET EIP 1559 GAS # GET EIP 1559 GAS # GET EIP 1559 GAS #
    ####################################################################################################################

    # function: getting EIP-1559 gas (transaction parameters)
    async def get_EIP_1559_gas_parameters(self, gas_increase_base: float) -> (int, int):
        w3 = await self.get_w3_with_poa_middleware()
        max_priority_fee_per_gas = int(w3.eth.max_priority_fee)
        base_fee_per_gas = w3.eth.get_block('latest')['baseFeePerGas']
        max_fee_per_gas = int(base_fee_per_gas * gas_increase_base) + max_priority_fee_per_gas
        if (self.name_network == 'Celo') and int(max_priority_fee_per_gas) == GAS_CELO_2B:
            maxPriorityFeePerGas = GAS_CELO_10B
            maxFeePerGas = max_fee_per_gas
        else:
            maxPriorityFeePerGas = max_priority_fee_per_gas
            maxFeePerGas = max_fee_per_gas

        return maxPriorityFeePerGas, maxFeePerGas

    ####################################################################################################################
    # GET W3 WITH POA MIDDLEWARE # GET W3 WITH POA MIDDLEWARE # GET W3 WITH POA MIDDLEWARE # GET W3 WITH POA MIDDLEWARE
    ####################################################################################################################

    # function: getting web3 object (with poa middleware)
    async def get_w3_with_poa_middleware(self, ) -> Web3:
        if self.proxy is not None:
            w3 = Web3(
                provider=Web3.HTTPProvider(
                    endpoint_uri=self.url_rpc,
                    request_kwargs={'proxies': {'http': f'http://{self.proxy}', 'https': f'http://{self.proxy}'}}
                ),
            )
        else:
            w3 = Web3(provider=Web3.HTTPProvider(endpoint_uri=self.url_rpc))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return w3

########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
