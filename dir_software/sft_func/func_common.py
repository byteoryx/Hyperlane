########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# types
from typing import Union, Any

# libraries
import time
import random
import pandas as pd
from datetime import datetime

# dir: head
from dir_web3.wb3_head import Client
from dir_Hyperlane.hl_head import Network

# dir: globals
from dir_software.sft_glob import *
from dir_Hyperlane.hl_glob import NETWORKS_OBJECTS_DICT

# dir: func
from dir_common import cmn_func as cmn


########################################################################################################################
# CLEAR NAN VALUES # CLEAR NAN VALUES # CLEAR NAN VALUES # CLEAR NAN VALUES # CLEAR NAN VALUES # CLEAR NAN VALUES # CLEA
########################################################################################################################

# function: clearing nan values from table
def clear_nan_values(accounts_list: list) -> list:
    new_account_list = []
    for account_dict in accounts_list:
        for key, value in account_dict.items():
            if pd.isna(value):
                account_dict[key] = VAL_A_NAN
        new_account_list.append(account_dict)
    return new_account_list


########################################################################################################################
# CREATE STATE MACHINE # CREATE STATE MACHINE # CREATE STATE MACHINE # CREATE STATE MACHINE # CREATE STATE MACHINE # CRE
########################################################################################################################

# function: creating a state machine
def create_state_machine(accounts_list: list) -> list:
    state_machine = []

    for account_dict in accounts_list:
        nft_id = account_dict[KEY_A_NFT_ID]
        return_bool = account_dict[KEY_A_RETURN_BOOL]
        network_mint = account_dict[KEY_A_NETWORK_MINT]
        n_txs_min = 0 if (account_dict[KEY_A_N_TXS_MIN] == VAL_A_NAN) else int(account_dict[KEY_A_N_TXS_MIN])
        n_txs_max = 0 if (account_dict[KEY_A_N_TXS_MAX] == VAL_A_NAN) else int(account_dict[KEY_A_N_TXS_MAX])

        networks_list = [
            key for key, value in account_dict.items() if (key in NETWORKS_NAMES_LIST) and (value == 1)
        ]
        networks_path_list = create_networks_path(network_mint, networks_list, n_txs_min, n_txs_max, return_bool)
        networks_chain_list = create_networks_chain(networks_path_list)
        account_dict[KEY_A_NETWORKS_CHAIN_LIST] = networks_chain_list
        account_dict[KEY_A_NETWORKS_PATH_LIST] = networks_path_list
        commands_list = []

        # commands: mint, mint_verify, mint_receipt, mint_confirm
        if nft_id == VAL_A_NAN:
            for command in [VAL_C_MINT, VAL_C_MINT_VERIFY, VAL_C_MINT_RECEIPT, VAL_C_MINT_CONFIRM]:
                commands_list.append(create_command(command, VAL_C_DEFAULT, VAL_C_DEFAULT, network_mint))

        # commands: bridge, bridge_verify, bridge_confirm
        for networks_tuple in networks_chain_list:
            for command in [VAL_C_BRIDGE, VAL_C_BRIDGE_VERIFY, VAL_C_BRIDGE_CONFIRM]:
                commands_list.append(create_command(command, VAL_C_DEFAULT, VAL_C_DEFAULT, networks_tuple))

        run_dict = {
            KEY_R_TIMESTAMP: str(datetime.utcnow().timestamp()),
            KEY_R_ACCOUNT_DICT: account_dict,
            KEY_R_COMMANDS_LIST: commands_list
        }
        state_machine.append(run_dict)

        # sleep: 0.1 sec
        time.sleep(0.1)

    # return
    return state_machine


########################################################################################################################
# CREATE COMMAND DICT # CREATE COMMAND DICT # CREATE COMMAND DICT # CREATE COMMAND DICT # CREATE COMMAND DICT # CREATE C
########################################################################################################################

# function: creating command_dict
def create_command(command: str, status: str, value: str, network: Union[str, tuple]) -> dict:
    command_dict = {
        KEY_C_COMMAND: command,
        KEY_C_STATUS: status,
        KEY_C_VALUE: value,
        KEY_C_NETWORK: network
    }
    return command_dict


########################################################################################################################
# CREATE NETWORKS PATH # CREATE NETWORKS PATH # CREATE NETWORKS PATH # CREATE NETWORKS PATH # CREATE NETWORKS PATH # CRE
########################################################################################################################

# function: creating networks path
def create_networks_path(network_mint: str, networks_list: list, n_txs_min: int, n_txs_max: int, return_bool: int) -> list:
    if len(networks_list) <= 1:
        return []
    else:
        n_txs = random.randint(n_txs_min, n_txs_max)
        t_networks_list = list(networks_list)
        networks_path_list = [network_mint]

        for i in range(n_txs):
            if not t_networks_list:
                t_networks_list = list(networks_list)
            random_network = random.choice(t_networks_list)

            if networks_path_list[-1] != random_network:
                networks_path_list.append(random_network)
                t_networks_list.remove(random_network)
            else:
                first_random_network = random_network
                t_networks_list.remove(first_random_network)
                second_random_network = random.choice(t_networks_list)
                networks_path_list.append(second_random_network)
                t_networks_list.remove(second_random_network)
                t_networks_list.append(first_random_network)

        if networks_path_list == [network_mint]:
            return []
        else:
            if (return_bool == 1) and (networks_path_list[-1] != network_mint):
                networks_path_list.append(network_mint)
            return networks_path_list


########################################################################################################################
# CREATE NETWORKS CHAIN # CREATE NETWORKS CHAIN # CREATE NETWORKS CHAIN # CREATE NETWORKS CHAIN # CREATE NETWORKS CHAIN
########################################################################################################################

# function: creating networks transfers
def create_networks_chain(networks_list: list) -> list:
    networks_chain_list = [(networks_list[i], networks_list[i + 1]) for i in range(len(networks_list) - 1)]
    return networks_chain_list


########################################################################################################################
# CREATE DISPLAY PATH # CREATE DISPLAY PATH # CREATE DISPLAY PATH # CREATE DISPLAY PATH # CREATE DISPLAY PATH # CREATE D
########################################################################################################################

# function: creating account's path to display
def create_display_path(account_dict: dict) -> str:
    networks_path_list = account_dict[KEY_A_NETWORKS_PATH_LIST][1:]
    network_mint = account_dict[KEY_A_NETWORK_MINT]
    nft_id = account_dict[KEY_A_NFT_ID]
    mint = f'{network_mint}[mint]' if (nft_id == VAL_A_NAN) else f'{network_mint}[{nft_id}]'
    path = f' -> ' + f' -> '.join(map(str, networks_path_list)) if (networks_path_list != []) else ''
    return mint + path


########################################################################################################################
# GET CLIENT # GET CLIENT # GET CLIENT # GET CLIENT # GET CLIENT # GET CLIENT # GET CLIENT # GET CLIENT # GET CLIENT # G
########################################################################################################################

# function: getting client object (Client)
async def get_client(account_dict: dict, command_dict: dict) -> (int, Union[Client, Exception]):
    command, private_key = command_dict[KEY_C_COMMAND], account_dict[KEY_A_PRIVATE_KEY]

    if command in [VAL_C_MINT, VAL_C_MINT_VERIFY, VAL_C_MINT_RECEIPT, VAL_C_MINT_CONFIRM]:
        network = command_dict[KEY_C_NETWORK]
    elif command in [VAL_C_BRIDGE, VAL_C_BRIDGE_VERIFY]:
        network = command_dict[KEY_C_NETWORK][0]
    else:
        network = command_dict[KEY_C_NETWORK][1]
    network_object: Network = NETWORKS_OBJECTS_DICT[network]
    network_rpc = network_object.url_rpc

    # check: proxy (workable)
    proxy = account_dict[KEY_A_PROXY] if (account_dict[KEY_A_PROXY] != VAL_A_NAN) else None
    if (proxy is not None) and (not cmn.check_proxy_http(proxy)):
        return -1, Exception('Proxy is incorrect!')

    # check: client (connection)
    client = Client(private_key=private_key, network_rpc=network_rpc, network_name=network, proxy=proxy)
    result, msg = await client.is_connected()
    if result == -1:
        return -1, Exception(f'| {network} | Could not connect to the RPC! | {msg}')
    else:
        return 0, client


########################################################################################################################
# GET UPDATED RUN DICT # GET UPDATED RUN DICT # GET UPDATED RUN DICT # GET UPDATED RUN DICT # GET UPDATED RUN DICT # GET
########################################################################################################################

# function: getting updated run_dict (with last command)
def update_run_dict(run_dict: dict, command_index: int, status: str, value: Any) -> dict:
    run_dict[KEY_R_COMMANDS_LIST][command_index][KEY_C_STATUS] = status
    run_dict[KEY_R_COMMANDS_LIST][command_index][KEY_C_VALUE] = value
    return run_dict


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
