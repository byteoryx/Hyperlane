########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# libraries
import time
import random
import pandas as pd

# dir: globals
from dir_software.sft_glob import *
from __system__.dir_logger.lg_main import LOGGER, NAME_SOFTWARE
from dir_Hyperlane.hl_glob import NETWORKS_OBJECTS_DICT
from dir_Hyperlane.hl_head import ADDRESS_ZERO

# dir: head
from dir_web3.wb3_head import Client
from dir_Hyperlane.hl_head import Hyperlane
from dir_OKX.okx_class import OkxFunding
from dir_Hyperlane.hl_head import Network
from dir_Binance.bn_head import BinanceSpot

# dir: func
from dir_database import db_runs_o
from dir_common import cmn_func as cmn
from dir_software.sft_func import func_common
from dir_web3.wb3_func import get_anonymous_string
from dir_software.sft_func import func_software_nft as software_nft
from dir_software.sft_func import func_software_finder as software_finder


########################################################################################################################
# LAUNCH SOFTWARE # LAUNCH SOFTWARE # LAUNCH SOFTWARE # LAUNCH SOFTWARE # LAUNCH SOFTWARE # LAUNCH SOFTWARE # LAUNCH SOF
########################################################################################################################

# function: launching software
async def start_launcher() -> None:
    LOGGER.info(f'LAUNCHER | {NAME_SOFTWARE} has been launched!')

    # check_00: unfinished sessions
    check_00 = await check_unfinished_sessions()
    if not check_00:
        return

    # check_01: Excel file existence and correctness (settings.xlsx)
    check_01 = check_excel_file(FILENAME_SETTINGS, EXCEL_HEADERS)
    if not check_01:
        return

    # sleep: 1 sec
    time.sleep(1)

    while True:
        answer = input(
            f'What do you want to do?\n'
            f'[1] Mint + bridge NFTs (MerklyMinter)\n'
            f'[2] Find minted NFTs for every network\n'
            f'[3] Close\n'
        )
        if answer == '1':
            await start_launcher_nft()
            break
        elif answer == '2':
            await software_finder.start_software(FILENAME_SETTINGS)
            break
        elif answer == '3':
            break
        else:
            print(f'No such an answer!')

    # return
    LOGGER.info(f'LAUNCHER | {NAME_SOFTWARE} has been finished!')
    return


########################################################################################################################
# LAUNCH SOFTWARE # LAUNCH SOFTWARE # LAUNCH SOFTWARE # LAUNCH SOFTWARE # LAUNCH SOFTWARE # LAUNCH SOFTWARE # LAUNCH SOF
########################################################################################################################

# function: launching software
async def start_launcher_nft() -> None:

    # check_02: Excel file data content (settings.xlsx)
    check_02, accounts_list = check_content(FILENAME_SETTINGS)
    if not check_02:
        return

    # check_03: accounts connections (web3)
    check_03, accounts_list = await check_accounts(accounts_list)
    if not check_03:
        return

    # creating state machine (run_dict: timestamp, account_dict, commands_list)
    state_machine = func_common.create_state_machine(accounts_list)
    for run_dict in state_machine:
        account_dict = run_dict[KEY_R_ACCOUNT_DICT]
        display_path = func_common.create_display_path(account_dict)
        anonym_address = get_anonymous_string(account_dict[KEY_A_ADDRESS_CLIENT])
        LOGGER.info(f"LAUNCHER | DISPLAY | add: {anonym_address} | path: {display_path}")

    # sleep: 1 sec
    time.sleep(1)

    # message
    print(f'Software is ready to start! Do you want to start it? (yes/no)')
    while True:
        answer = input()
        if answer == 'yes':
            print(f'How many retries do you want to have? (integer number)')
            while True:
                try:
                    n_retries = int(input())
                    if n_retries > 0:
                        for run_dict in state_machine:
                            db_runs_o.add_run(run_dict)
                        await software_nft.start_software(n_retries)
                        break
                    else:
                        print(f'Retries must be greater than zero!')
                except ValueError:
                    print(f'Retries must be integer!')
            break
        elif answer == 'no':
            break
        else:
            print(f'No such an answer! (yes/no)')


########################################################################################################################
# CHECK UNFINISHED SESSIONS # CHECK UNFINISHED SESSIONS # CHECK UNFINISHED SESSIONS # CHECK UNFINISHED SESSIONS # CHECK
########################################################################################################################

# function: checking unfinished sessions
async def check_unfinished_sessions() -> bool:
    LOGGER.info(f'LAUNCHER | CHECK_0 | Checking...')
    runs_list = db_runs_o.get_runs_list()

    if not runs_list:
        LOGGER.info(f'LAUNCHER | CHECK_0 | Ok!')
        return True
    else:
        for run_dict in runs_list:
            timestamp = run_dict[KEY_R_TIMESTAMP]
            account_dict = run_dict[KEY_R_ACCOUNT_DICT]
            display_path = func_common.create_display_path(account_dict)
            anonym_address = get_anonymous_string(account_dict[KEY_A_ADDRESS_CLIENT])
            LOGGER.info(f"LAUNCHER | CHECK_0 | add: {anonym_address} | time: {timestamp} | path: {display_path}")

        # sleep: 1 sec
        time.sleep(1)

        # message
        print('You have unfinished sessions! Do you want to finish them?                                  ')
        print('|----------------|------------------------------------------------------------------------|')
        print('| Command:       | Function:                                                              |')
        print('|----------------|------------------------------------------------------------------------|')
        print('| finish all     | finish all unfinished sessions                                         |')
        print('| delete all     | delete all unfinished sessions                                         |')
        print('| finish {time}  | finish specific one (take {time} above), e.g: finish 1706009942.130829 |')
        print('| delete {time}  | delete specific one (take {time} above), e.g: delete 1706009942.130829 |')
        print('| close          | close the software                                                     |')
        print('|----------------|------------------------------------------------------------------------|')
        while True:
            answer = input()
            if answer == 'finish all':
                print(f'How many retries do you want to have? (integer number)')
                while True:
                    try:
                        answer = int(input())
                        if answer > 0:
                            await software_nft.start_software(answer)
                            break
                        else:
                            print(f'Retries must be greater than zero!')
                    except ValueError:
                        print(f'Retries must be integer!')
                break
            elif answer == 'delete all':
                db_runs_o.clear_database()
                print(f'All sessions were deleted! Restart the software to use it!')
                time.sleep(1)
                break
            elif ('finish ' in answer) and ('finish ' != answer):
                _, timestamp = answer.split()
                if timestamp in db_runs_o.get_run_timestamps_list():
                    print(f'How many retries do you want to have? (integer number)')
                    while True:
                        try:
                            answer = int(input())
                            if answer > 0:
                                await software_nft.start_software(answer, timestamp)
                                break
                            else:
                                print(f'Retries must be greater than zero!')
                        except ValueError:
                            print(f'Retries must be integer!')
                    break
                else:
                    print(f'No such a session!')
            elif ('delete ' in answer) and ('delete ' != answer):
                _, timestamp = answer.split()
                if timestamp in db_runs_o.get_run_timestamps_list():
                    db_runs_o.delete_run(timestamp)
                    print(f'Session was deleted! Restart the software to use it!')
                    time.sleep(1)
                    break
                else:
                    print(f'No such a session!')
            elif answer == 'close':
                break
            else:
                print(f'No such an answer!')

        # message
        LOGGER.info(f'LAUNCHER | {NAME_SOFTWARE} has been finished!')
        return False


########################################################################################################################
# CHECK EXCEL FILE # CHECK EXCEL FILE # CHECK EXCEL FILE # CHECK EXCEL FILE # CHECK EXCEL FILE # CHECK EXCEL FILE # CHEC
########################################################################################################################

# function: checking Excel file (existence and correctness)
def check_excel_file(filename: str, headers_list: list) -> bool:
    LOGGER.info(f'LAUNCHER | CHECK_1 | Checking...')
    try:
        df = pd.read_excel(filename)
    except Exception as E:
        LOGGER.error(f'LAUNCHER | CHECK_1 | Could not read the file with error: {E}')
        LOGGER.debug(f'LAUNCHER | CHECK_1 | Creating file...')
        df = pd.DataFrame(columns=headers_list)
        df.to_excel(filename, index=False)
        LOGGER.debug(f'LAUNCHER | CHECK_1 | File was created!')
        return True
    if list(df.columns) != headers_list:
        LOGGER.error(f'LAUNCHER | CHECK_1 | Table data is not correct!')
        return False

    # message
    LOGGER.info(f'LAUNCHER | CHECK_1 | Ok!')
    return True


########################################################################################################################
# CHECK CONTENT # CHECK CONTENT # CHECK CONTENT # CHECK CONTENT # CHECK CONTENT # CHECK CONTENT # CHECK CONTENT # CHECK
########################################################################################################################

# function: checking file content
def check_content(filename: str) -> (bool, list):
    LOGGER.info(f'LAUNCHER | CHECK_2 | Checking...')
    try:
        df = pd.read_excel(filename)
    except Exception as E:
        LOGGER.error(f'LAUNCHER | CHECK_2 | Could not read an excel file {filename} with error: {E}')
        return False, []
    if df.empty:
        LOGGER.error(f'LAUNCHER | CHECK_2 | File {filename} is empty!')
        return False, []
    accounts_list = func_common.clear_nan_values(df.to_dict(orient='records'))
    n_accounts = len(accounts_list)

    account_number = 1
    for account_dict in accounts_list:
        main_message = f'LAUNCHER | CHECK_2 | {account_number}/{n_accounts}'

        # check_01: required settings
        check_01 = check_required_settings(main_message, account_dict)
        if not check_01:
            return False, []

        # check_02: mint network
        check_02 = check_mint_network(main_message, account_dict)
        if not check_02:
            return False, []

        # check_03: time sleep parameters
        check_03 = check_time_sleep_parameters(main_message, account_dict)
        if not check_03:
            return False, []

        # check_04: OKX settings
        check_04 = check_okx_settings(main_message, account_dict)
        if not check_04:
            return False, []

        # check_05: proxy
        check_05 = check_proxy(main_message, account_dict)
        if not check_05:
            return False, []

        # check_06: number transactions parameters
        check_06 = check_n_txs_parameters(main_message, account_dict)
        if not check_06:
            return False, []

        # check_07: time_sleep_start
        check_07 = check_time_sleep_start(main_message, account_dict)
        if not check_07:
            return False, []

        # check_08: max_eth_gwei
        check_08 = check_max_eth_gwei(main_message, account_dict)
        if not check_08:
            return False, []

        # check_09: nft_id
        check_09 = check_nft_id(main_message, account_dict)
        if not check_09:
            return False, []

        # check_10: deposit range
        check_10 = check_deposit_range(main_message, account_dict)
        if not check_10:
            return False, []

        # account: counting
        account_number += 1

    # message
    LOGGER.info(f'LAUNCHER | CHECK_2 | Ok!')
    return True, accounts_list


########################################################################################################################
# CHECK REQUIRED SETTINGS # CHECK REQUIRED SETTINGS # CHECK REQUIRED SETTINGS # CHECK REQUIRED SETTINGS # CHECK REQUIRED
########################################################################################################################

# function: checking required parameters
def check_required_settings(main_message: str, account_dict: dict) -> bool:
    private_key, network_mint = account_dict[KEY_A_PRIVATE_KEY], account_dict[KEY_A_NETWORK_MINT]

    if (private_key == VAL_A_NAN) or (network_mint == VAL_A_NAN):
        LOGGER.error(f'{main_message} | Not all required settings!')
        return False
    else:
        return True


########################################################################################################################
# CHECK MINT NETWORK # CHECK MINT NETWORK # CHECK MINT NETWORK # CHECK MINT NETWORK # CHECK MINT NETWORK # CHECK MINT NE
########################################################################################################################

# function: checking mint network
def check_mint_network(main_message: str, account_dict: dict) -> bool:
    network_mint = account_dict[KEY_A_NETWORK_MINT]

    if network_mint != VAL_A_RANDOM:
        if network_mint not in NETWORKS_NAMES_LIST:
            LOGGER.error(f'{main_message} | No such a mint network in the list! Must be a network or a command[RANDOM]!')
            return False
        else:
            selected_networks_list = [k for k, value in account_dict.items() if
                                      (k in NETWORKS_NAMES_LIST) and (value == 1)]

            if network_mint not in selected_networks_list:
                LOGGER.error(f'{main_message} | Mint network is not selected!')
                return False
            else:
                return True
    else:
        return True


########################################################################################################################
# CHECK TIME SLEEP PARAMETERS # CHECK TIME SLEEP PARAMETERS # CHECK TIME SLEEP PARAMETERS # CHECK TIME SLEEP PARAMETERS
########################################################################################################################

# function: checking time sleep parameters
def check_time_sleep_parameters(main_message: str, account_dict: dict) -> bool:
    time_sleep_min, time_sleep_max = account_dict[KEY_A_TIME_SLEEP_MIN], account_dict[KEY_A_TIME_SLEEP_MAX]

    if (time_sleep_min != VAL_A_NAN) and (time_sleep_max != VAL_A_NAN):
        if (not isinstance(time_sleep_min, int)) or (not isinstance(time_sleep_max, int)):
            LOGGER.error(f'{main_message} | Time sleep parameters must be integers!')
            return False
        else:
            if (time_sleep_min < 0) or (time_sleep_max < 0):
                LOGGER.error(f'{main_message} | Time sleep parameters must be positive!')
                return False
            else:
                if time_sleep_min >= time_sleep_max:
                    LOGGER.error(f'{main_message} | Time sleep max must be greater than min!')
                    return False
                else:
                    return True
    else:
        if not ((time_sleep_min == VAL_A_NAN) and (time_sleep_max == VAL_A_NAN)):
            LOGGER.error(f'{main_message} | Time sleep parameters must be initialized together!')
            return False
        else:
            return True


########################################################################################################################
# CHECK OKX SETTINGS # CHECK OKX SETTINGS # CHECK OKX SETTINGS # CHECK OKX SETTINGS # CHECK OKX SETTINGS # CHECK OKX SET
########################################################################################################################

# function: checking OKX settings (api_key, secret_key, passphrase)
def check_okx_settings(main_message: str, account_dict: dict) -> bool:
    api_key, secret_key = account_dict[KEY_A_OKX_API_KEY], account_dict[KEY_A_OKX_SECRET_KEY]
    passphrase = account_dict[KEY_A_OKX_PASSPHRASE]

    if not (api_key == VAL_A_NAN and secret_key == VAL_A_NAN and passphrase == VAL_A_NAN):
        if not (api_key != VAL_A_NAN and secret_key != VAL_A_NAN and passphrase != VAL_A_NAN):
            LOGGER.error(f'{main_message} | Not all required settings for OKX exchange!')
            return False
        else:
            okx = OkxFunding(api_key=api_key, api_secret=secret_key, passphrase=passphrase, proxy='')
            result, msg = okx.check_keys()

            if result == -1:
                LOGGER.error(f'{main_message} | Could not connect to the OKX! | {msg}')
                return False
            else:
                return True
    else:
        return True


########################################################################################################################
# CHECK PROXY # CHECK PROXY # CHECK PROXY # CHECK PROXY # CHECK PROXY # CHECK PROXY # CHECK PROXY # CHECK PROXY # CHECK
########################################################################################################################

# function: checking proxy
def check_proxy(main_message: str, account_dict: dict) -> bool:
    proxy = account_dict[KEY_A_PROXY]

    if (proxy != VAL_A_NAN) and (not cmn.check_proxy_http(proxy)):
        LOGGER.error(f'{main_message} | Proxy is incorrect!')
        return False
    else:
        return True


########################################################################################################################
# CHECK NUMBER TRANSACTIONS PARAMETERS # CHECK NUMBER TRANSACTIONS PARAMETERS # CHECK NUMBER TRANSACTIONS PARAMETERS # C
########################################################################################################################

# function: checking number transactions parameters
def check_n_txs_parameters(main_message: str, account_dict: dict) -> bool:
    n_txs_min, n_txs_max = account_dict[KEY_A_N_TXS_MIN], account_dict[KEY_A_N_TXS_MAX]

    if (n_txs_min != VAL_A_NAN) and (n_txs_max != VAL_A_NAN):
        if (not isinstance(n_txs_min, int)) or (not isinstance(n_txs_max, int)):
            LOGGER.error(f'{main_message} | N_txs parameters must be integers!')
            return False
        else:
            if (n_txs_min <= 0) or (n_txs_max <= 0):
                LOGGER.error(f'{main_message} | N_txs parameters must be positive!')
                return False
            else:
                if n_txs_min > n_txs_max:
                    LOGGER.error(f'{main_message} | N_txs_max must be greater (or equal) than min!')
                    return False
                else:
                    return True
    else:
        if not ((n_txs_min == VAL_A_NAN) and (n_txs_max == VAL_A_NAN)):
            LOGGER.error(f'{main_message} | N_txs parameters must be initialized together!')
            return False
        else:
            return True


########################################################################################################################
# CHECK TIME SLEEP START # CHECK TIME SLEEP START # CHECK TIME SLEEP START # CHECK TIME SLEEP START # CHECK TIME SLEEP S
########################################################################################################################

# function: checking time_sleep_start parameter
def check_time_sleep_start(main_message: str, account_dict: dict) -> bool:
    time_sleep_start = account_dict[KEY_A_TIME_SLEEP_START]

    if time_sleep_start != VAL_A_NAN:
        if not isinstance(time_sleep_start, int):
            LOGGER.error(f'{main_message} | The entered time_sleep_start is incorrect!')
            return False
        else:
            time_sleep_start = int(time_sleep_start)

            if time_sleep_start < 0:
                LOGGER.error(f'{main_message} | Time_sleep_start must be positive!')
                return False
            else:
                return True
    else:
        return True


########################################################################################################################
# CHECK MAX ETH GWEI # CHECK MAX ETH GWEI # CHECK MAX ETH GWEI # CHECK MAX ETH GWEI # CHECK MAX ETH GWEI # CHECK MAX ETH
########################################################################################################################

# function: checking max_eth_gwei parameter
def check_max_eth_gwei(main_message: str, account_dict: dict) -> bool:
    max_eth_gwei = account_dict[KEY_A_MAX_ETH_GWEI]

    if max_eth_gwei != VAL_A_NAN:
        if not isinstance(max_eth_gwei, int):
            LOGGER.error(f'{main_message} | Max_eth_gwei must be integer!')
            return False
        else:
            max_eth_gwei = int(max_eth_gwei)

            if max_eth_gwei <= 0:
                LOGGER.error(f'{main_message} | Max_eth_gwei must be greater than zero!')
                return False
            else:
                return True
    else:
        return True


########################################################################################################################
# CHECK NFT ID # CHECK NFT ID # CHECK NFT ID # CHECK NFT ID # CHECK NFT ID # CHECK NFT ID # CHECK NFT ID # CHECK NFT ID
########################################################################################################################

# function: checking NFT ID (correctness)
def check_nft_id(main_message: str, account_dict: dict) -> bool:
    nft_id = account_dict[KEY_A_NFT_ID]
    network_mint = account_dict[KEY_A_NETWORK_MINT]
    n_txs_min, n_txs_max = account_dict[KEY_A_N_TXS_MIN], account_dict[KEY_A_N_TXS_MAX]

    if nft_id != VAL_A_NAN:
        if network_mint == VAL_A_RANDOM:
            LOGGER.error(f'{main_message} | NFT_id must be in a specific chain, not RANDOM!')
            return False
        else:
            if not isinstance(nft_id, int):
                LOGGER.error(f'{main_message} | Nft_id must be integer!')
                return False
            else:
                selected_networks_list = [
                    key for key, value in account_dict.items() if (key in NETWORKS_NAMES_LIST) and (value == 1)
                ]
                if (len(selected_networks_list) <= 1) or ((n_txs_min == VAL_A_NAN) and (n_txs_max == VAL_A_NAN)):
                    LOGGER.error(f'{main_message} | Cannot mint an NFT if the nft_id is chosen!')
                    return False
                else:
                    return True
    else:
        return True


########################################################################################################################
# CHECK DEPOSIT RANGE # CHECK DEPOSIT RANGE # CHECK DEPOSIT RANGE # CHECK DEPOSIT RANGE # CHECK DEPOSIT RANGE # CHECK DE
########################################################################################################################

# function: checking deposit range (correctness)
def check_deposit_range(main_message: str, account_dict: dict) -> bool:
    for network_name, network_object in NETWORKS_OBJECTS_DICT.items():
        if network_object.deposit_usd_min > network_object.deposit_usd_max:
            LOGGER.error(f'{main_message} | Deposit_usd_max must be greater than deposit_usd_min!')
            return False
    return True


########################################################################################################################
# CHECK ACCOUNTS # CHECK ACCOUNTS # CHECK ACCOUNTS # CHECK ACCOUNTS # CHECK ACCOUNTS # CHECK ACCOUNTS # CHECK ACCOUNTS #
########################################################################################################################

# function: checking accounts for connection and balances
async def check_accounts(accounts_list: list) -> (bool, list):
    LOGGER.info(f'LAUNCHER | CHECK_3 | Checking...')

    new_accounts_list = []
    i = 1
    for account_dict in accounts_list:
        check, account_dict = await check_account(account_dict, i, len(accounts_list))
        if not check:
            return False, []
        else:
            new_accounts_list.append(account_dict)
        i += 1

    # message
    LOGGER.info(f'LAUNCHER | CHECK_3 | Ok!')
    return True, new_accounts_list


########################################################################################################################
# CHECK ACCOUNT # CHECK ACCOUNT # CHECK ACCOUNT # CHECK ACCOUNT # CHECK ACCOUNT # CHECK ACCOUNT # CHECK ACCOUNT # CHECK
########################################################################################################################

# function: checking account for connection and balances
async def check_account(account_dict: dict, n_account: int, n_accounts: int) -> (bool, dict):
    LOGGER.info(f'LAUNCHER | CHECK_3 | {n_account}/{n_accounts} | Checking...')

    selected_networks_list = [
        key for key, value in account_dict.items() if (key in NETWORKS_NAMES_LIST) and (value == 1)
    ]
    proxy = account_dict[KEY_A_PROXY] if (account_dict[KEY_A_PROXY] != VAL_A_NAN) else None
    mm_private_key = account_dict[KEY_A_PRIVATE_KEY]
    nft_id = account_dict[KEY_A_NFT_ID]
    address = ''

    if account_dict[KEY_A_NETWORK_MINT] == VAL_A_RANDOM:
        network_mint = random.choice(selected_networks_list)
    else:
        network_mint = account_dict[KEY_A_NETWORK_MINT]

    for network_name in selected_networks_list:
        network_object: Network = NETWORKS_OBJECTS_DICT[network_name]
        client = Client(mm_private_key, network_object.url_rpc, network_name, proxy)
        anonym_address = get_anonymous_string(client.address)
        main_message = f'LAUNCHER | CHECK_3 | {n_account}/{n_accounts} | add: {anonym_address} | {network_name}'

        # check_01: account connection
        check_01 = await check_network_connection(main_message, client)
        if not check_01:
            return False, {}

        # check_02: account balances in native tokens
        if (not network_object.deposit_bool) or (account_dict[KEY_A_OKX_API_KEY] == VAL_A_NAN):
            check_02 = await check_network_balance_native_token(main_message, client, network_object)
            if not check_02:
                return False, {}

        # check_03: nft owner
        if (network_name == network_mint) and (nft_id != VAL_A_NAN):
            check_03 = await check_nft_owner(main_message, client, nft_id)
            if not check_03:
                return False, {}

        # getting address
        address = str(client.address)

    # saving account_dict
    account_dict[KEY_A_ADDRESS_CLIENT] = address
    account_dict[KEY_A_NETWORK_MINT] = network_mint

    # message
    LOGGER.info(f'LAUNCHER | CHECK_3 | {n_account}/{n_accounts} | Ok!')
    return True, account_dict


########################################################################################################################
# CHECK NETWORK CONNECTION # CHECK NETWORK CONNECTION # CHECK NETWORK CONNECTION # CHECK NETWORK CONNECTION # CHECK NETW
########################################################################################################################

# function: checking network connection
async def check_network_connection(main_message: str, client: Client) -> bool:
    result, msg = await client.is_connected()

    if result == -1:
        LOGGER.error(f'{main_message} | Could not connect to the RPC! | {msg}')
        return False
    else:
        LOGGER.debug(f'{main_message} | Successfully connected!')
        return True


########################################################################################################################
# CHECK NETWORK BALANCE NATIVE TOKEN # CHECK NETWORK BALANCE NATIVE TOKEN # CHECK NETWORK BALANCE NATIVE TOKEN # CHECK N
########################################################################################################################

# function: checking network balance in native token
async def check_network_balance_native_token(main_message: str, client: Client, network_object: Network) -> bool:
    token_ticker = network_object.name_token
    result, msg = await client.get_balance_native()

    if result == -1:
        LOGGER.error(f'{main_message} | {token_ticker} | Could not get balance! | {msg}')
        return False
    else:
        balance_float = cmn.from_decimals_to_float(network_object.n_decimals_native_token, msg)
        result, msg = BinanceSpot().get_ticker_price(symbol=token_ticker+'USDT')

        if result == -1:
            LOGGER.error(f'{main_message} | {token_ticker} | Could not get price! | {msg}')
            return False
        else:
            balance_usdt = balance_float * msg
            deposit_usd = network_object.deposit_usd_min

            if balance_usdt < deposit_usd:
                LOGGER.error(f'{main_message} | {token_ticker} | Not enough! | Must be at least ${deposit_usd}...')
                return False
            else:
                return True


########################################################################################################################
# CHECK NFT OWNER # CHECK NFT OWNER # CHECK NFT OWNER # CHECK NFT OWNER # CHECK NFT OWNER # CHECK NFT OWNER # CHECK NFT
########################################################################################################################

# function: checking nft owner
async def check_nft_owner(main_message: str, client: Client, nft_id: int) -> bool:
    hyperlane = Hyperlane(client)
    network: Network = NETWORKS_OBJECTS_DICT[client.name_network]
    result, msg = await hyperlane.check_nft_owner(address_contract=network.address_contract, nft_id=nft_id)

    if result == -1:
        LOGGER.error(f'{main_message} | Could not check NFT owner! | {msg}')
        return False
    else:
        if msg == ADDRESS_ZERO:
            LOGGER.error(f'{main_message} | Could not find NFT[{nft_id}] in the chain!')
            return False
        else:
            if msg != client.address:
                LOGGER.error(f'{main_message} | NFT[{nft_id}] is not yours! | NFT belongs to: {msg}')
                return False
            else:
                return True


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
