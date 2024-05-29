########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# types
from web3.types import HexBytes
from typing import Union, Optional
from web3.types import ChecksumAddress

# libraries
import dataclasses
from web3 import Web3

# dir: head
from dir_web3.wb3_head import Client

# dir: func
from dir_common.cmn_func import read_json_from_file


########################################################################################################################
# GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS # GLOBALS
########################################################################################################################

# globals: zero address
ADDRESS_ZERO = '0x0000000000000000000000000000000000000000'


########################################################################################################################
# DEFAULT PARAMETERS # DEFAULT PARAMETERS # DEFAULT PARAMETERS # DEFAULT PARAMETERS # DEFAULT PARAMETERS # DEFAULT PARAM
########################################################################################################################

# default: time_sleep (SHORT)
DEFAULT_TIME_SLEEP_SHORT_MIN = 10
DEFAULT_TIME_SLEEP_SHORT_MAX = 20


########################################################################################################################
# CLASS: NETWORK # CLASS: NETWORK # CLASS: NETWORK # CLASS: NETWORK # CLASS: NETWORK # CLASS: NETWORK # CLASS: NETWORK #
########################################################################################################################

# class: Network
@dataclasses.dataclass
class Network:
    name_network: str
    name_token: str
    domain: int
    n_decimals_native_token: int
    gas_increase_base_mint: float
    gas_increase_base_bridge: float
    deposit_bool: bool
    deposit_chain: str
    deposit_usd_min: float
    deposit_usd_max: float
    url_rpc: str
    address_contract: ChecksumAddress


########################################################################################################################
# CLASS: HYPERLANE # CLASS: HYPERLANE # CLASS: HYPERLANE # CLASS: HYPERLANE # CLASS: HYPERLANE # CLASS: HYPERLANE # CLAS
########################################################################################################################

# class: Hyperlane
class Hyperlane:
    filename_abi_hyperlane = 'dir_Hyperlane/storage/Hyperlane.json'
    abi_hyperlane = read_json_from_file(filename_abi_hyperlane)

    def __init__(self, client: Client):
        """
        Creating Hyperlane object

        :param client: a client object from the directory dir_web3
        """
        self.client = client

    ####################################################################################################################
    # CHECK NFT OWNER # CHECK NFT OWNER # CHECK NFT OWNER # CHECK NFT OWNER # CHECK NFT OWNER # CHECK NFT OWNER # CHECK
    ####################################################################################################################

    # function: checking nft owner
    async def check_nft_owner(self, address_contract: str, nft_id: int):
        try:
            contract = self.client.w3.eth.contract(
                address=Web3.to_checksum_address(address_contract), abi=Hyperlane.abi_hyperlane,
            )
            result = contract.functions.ownerOf(nft_id).call()
            return 0, result
        except Exception as E:
            if 'invalid token ID' in str(E):
                return 0, ADDRESS_ZERO
            else:
                return -1, E

    ####################################################################################################################
    # MINT NFT # MINT NFT # MINT NFT # MINT NFT # MINT NFT # MINT NFT # MINT NFT # MINT NFT # MINT NFT # MINT NFT # MINT
    ####################################################################################################################

    # function: minting NFT in native chain
    async def mint_nft(
            self, address_contract: str,
            gas_increase_gas: Optional[float], gas_increase_base: Optional[float], max_eth_gwei: Optional[int],
    ) -> (int, Union[HexBytes, Exception]):
        try:
            contract = self.client.w3.eth.contract(
                address=Web3.to_checksum_address(address_contract), abi=Hyperlane.abi_hyperlane,
            )
            mint_fee = contract.functions.fee().call()
            data = contract.encodeABI(fn_name='mint', args=[1])

            result, msg = await self.client.send_transaction(
                address_to=address_contract, data=data, value=mint_fee,
                gas_increase_gas=gas_increase_gas, gas_increase_base=gas_increase_base, gas_eth_max_gwei=max_eth_gwei
            )
            if result == 0:
                return 0, msg
            else:
                return -1, Exception(f'Some troubles in function send_transaction with error: {msg}')
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # GET NFT ID # GET NFT ID # GET NFT ID # GET NFT ID # GET NFT ID # GET NFT ID # GET NFT ID # GET NFT ID # GET NFT ID
    ####################################################################################################################

    # function: getting NFT id (by transaction hash)
    async def get_nft_id(self, transaction_hash: HexBytes) -> (int, Union[int, Exception]):
        try:
            result = self.client.w3.eth.wait_for_transaction_receipt(transaction_hash=transaction_hash, timeout=1000)
            if self.client.name_network == 'Polygon':
                nft_if_hex = result["logs"][1]["topics"][3]
            elif len(result["logs"]) == 1:
                nft_if_hex = result["logs"][0]["topics"][3]
            else:
                nft_if_hex = result["logs"][2]["topics"][3]
            nft_id = int.from_bytes(nft_if_hex, 'big')
            return 0, nft_id
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # BRIDGE NFT # BRIDGE NFT # BRIDGE NFT # BRIDGE NFT # BRIDGE NFT # BRIDGE NFT # BRIDGE NFT # BRIDGE NFT # BRIDGE NFT
    ####################################################################################################################

    # function: bridging NFT from chain to chain (by NFT id)
    async def bridge_nft(
            self, address_contract: str, domain_to: int, nft_id: int,
            gas_increase_gas: Optional[float], gas_increase_base: Optional[float], max_eth_gwei: Optional[int],
    ) -> (int, Union[HexBytes, Exception]):
        try:
            contract = self.client.w3.eth.contract(
                address=Web3.to_checksum_address(address_contract), abi=Hyperlane.abi_hyperlane,
            )
            bridge_fee = contract.functions.quoteBridge(domain_to).call()
            data = contract.encodeABI(fn_name='bridgeNFT', args=[domain_to, nft_id])

            result, msg = await self.client.send_transaction(
                address_to=address_contract, data=data, value=bridge_fee,
                gas_increase_gas=gas_increase_gas, gas_increase_base=gas_increase_base, gas_eth_max_gwei=max_eth_gwei
            )
            if result == 0:
                return 0, msg
            else:
                return -1, Exception(f'Some troubles in function send_transaction with error: {msg}')
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # GET NFT IDS # GET NFT IDS # GET NFT IDS # GET NFT IDS # GET NFT IDS # GET NFT IDS # GET NFT IDS # GET NFT IDS # GE
    ####################################################################################################################

    # function: getting all nft ids
    async def get_nft_ids(self, address_contract: str, network: Network) -> (int, Union[list, Exception]):
        try:
            contract = self.client.w3.eth.contract(
                address=Web3.to_checksum_address(address_contract), abi=Hyperlane.abi_hyperlane,
            )
            nft_ids_list = []
            balance = contract.functions.balanceOf(self.client.address).call()
            for i in range(balance):
                try:
                    nft_id = contract.functions.tokenOfOwnerByIndex(self.client.address, i).call()
                    if nft_id != 0:
                        nft_ids_list.append(nft_id)
                except Exception as E:
                    pass
            return 0, nft_ids_list
        except Exception as E:
            return -1, E


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################

