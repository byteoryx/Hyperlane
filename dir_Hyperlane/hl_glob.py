########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# libraries
from web3 import Web3

# dir: head
from dir_Hyperlane.hl_head import Network


########################################################################################################################
# NETWORKS # NETWORKS # NETWORKS # NETWORKS # NETWORKS # NETWORKS # NETWORKS # NETWORKS # NETWORKS # NETWORKS # NETWORKS
########################################################################################################################

# networks: objects dictionary
NETWORKS_OBJECTS_DICT = {
    'Arbitrum One': Network(
        name_network='Arbitrum One',
        name_token='ETH',
        domain=42161,
        n_decimals_native_token=18,
        gas_increase_base_mint=1.35,
        gas_increase_base_bridge=1.35,
        deposit_bool=True,
        deposit_chain='ETH-Arbitrum One',
        deposit_usd_min=3.0,
        deposit_usd_max=3.0,
        url_rpc='https://rpc.ankr.com/arbitrum',
        address_contract=Web3.to_checksum_address('0x7daC480d20f322D2ef108A59A465CCb5749371c4'),
    ),
    'Avalanche C-Chain': Network(
        name_network='Avalanche C-Chain',
        name_token='AVAX',
        domain=43114,
        n_decimals_native_token=18,
        gas_increase_base_mint=1.5,
        gas_increase_base_bridge=1.5,
        deposit_bool=True,
        deposit_chain='AVAX-Avalanche C-Chain',
        deposit_usd_min=7.0,
        deposit_usd_max=7.0,
        url_rpc='https://rpc.ankr.com/avalanche',
        address_contract=Web3.to_checksum_address('0x7daC480d20f322D2ef108A59A465CCb5749371c4'),
    ),
    'Base': Network(
        name_network='Base',
        name_token='ETH',
        domain=8453,
        n_decimals_native_token=18,
        gas_increase_base_mint=3.0,
        gas_increase_base_bridge=3.0,
        deposit_bool=True,
        deposit_chain='ETH-Base',
        deposit_usd_min=7.0,
        deposit_usd_max=7.0,
        url_rpc='https://rpc.ankr.com/base',
        address_contract=Web3.to_checksum_address('0x7dac480d20f322d2ef108a59a465ccb5749371c4'),
    ),
    'Binance Smart Chain': Network(
        name_network='Binance Smart Chain',
        name_token='BNB',
        domain=56,
        n_decimals_native_token=18,
        gas_increase_base_mint=1.5,
        gas_increase_base_bridge=1.5,
        deposit_bool=True,
        deposit_chain='BNB-BSC',
        deposit_usd_min=3.0,
        deposit_usd_max=3.0,
        url_rpc='https://rpc.ankr.com/bsc',
        address_contract=Web3.to_checksum_address('0xf3D41b377c93fA5C3b0071966f1811c5063fAD40'),
    ),
    'Celo': Network(
        name_network='Celo',
        name_token='CELO',
        domain=42220,
        n_decimals_native_token=18,
        gas_increase_base_mint=1.6,
        gas_increase_base_bridge=1.6,
        deposit_bool=True,
        deposit_chain='CELO-CELO',
        deposit_usd_min=3.0,
        deposit_usd_max=3.0,
        url_rpc='https://rpc.ankr.com/celo',
        address_contract=Web3.to_checksum_address('0x7f4CFDf669d7a5d4Adb05917081634875E21Df47'),
    ),
    'Moonbeam': Network(
        name_network='Moonbeam',
        name_token='GLMR',
        domain=1284,
        n_decimals_native_token=18,
        gas_increase_base_mint=1.0,
        gas_increase_base_bridge=1.0,
        deposit_bool=True,
        deposit_chain='GLMR-Moonbeam',
        deposit_usd_min=3.0,
        deposit_usd_max=3.0,
        url_rpc='https://rpc.ankr.com/moonbeam',
        address_contract=Web3.to_checksum_address('0x7daC480d20f322D2ef108A59A465CCb5749371c4'),
    ),
    'Optimism': Network(
        name_network='Optimism',
        name_token='ETH',
        domain=10,
        n_decimals_native_token=18,
        gas_increase_base_mint=1.2,
        gas_increase_base_bridge=1.2,
        deposit_bool=True,
        deposit_chain='ETH-Optimism',
        deposit_usd_min=3.0,
        deposit_usd_max=3.0,
        url_rpc='https://rpc.ankr.com/optimism',
        address_contract=Web3.to_checksum_address('0x2a5c54c625220cb2166C94DD9329be1F8785977D'),
    ),
    'Polygon': Network(
        name_network='Polygon',
        name_token='MATIC',
        domain=137,
        n_decimals_native_token=18,
        gas_increase_base_mint=1.5,
        gas_increase_base_bridge=1.5,
        deposit_bool=True,
        deposit_chain='MATIC-Polygon',
        deposit_usd_min=3.0,
        deposit_usd_max=3.0,
        url_rpc='https://rpc.ankr.com/polygon',
        address_contract=Web3.to_checksum_address('0x7daC480d20f322D2ef108A59A465CCb5749371c4'),
    ),
    'Scroll': Network(
        name_network='Scroll',
        name_token='ETH',
        domain=534352,
        n_decimals_native_token=18,
        gas_increase_base_mint=1.5,
        gas_increase_base_bridge=1.5,
        deposit_bool=False,
        deposit_chain='',
        deposit_usd_min=3.0,
        deposit_usd_max=3.0,
        url_rpc='https://rpc.ankr.com/scroll',
        address_contract=Web3.to_checksum_address('0x7daC480d20f322D2ef108A59A465CCb5749371c4'),
    ),
}

# networks: names list
NETWORKS_NAMES_LIST = list(NETWORKS_OBJECTS_DICT.keys())


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
