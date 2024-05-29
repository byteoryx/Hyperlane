########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# libraries
import random
import asyncio

# dir: globals
from dir_software.sft_glob import *
from __system__.dir_logger.lg_main import LOGGER, NAME_SOFTWARE
from dir_Hyperlane.hl_glob import NETWORKS_OBJECTS_DICT

# dir: head
from dir_Hyperlane.hl_head import *
from dir_OKX.okx_class import OkxFunding, NetworkInfo

# dir: func
from dir_database import db_runs_o
from dir_software.sft_func import func_common
from dir_web3.wb3_func import get_anonymous_string
from dir_common import cmn_func as cmn


########################################################################################################################
# START SOFTWARE # START SOFTWARE # START SOFTWARE # START SOFTWARE # START SOFTWARE # START SOFTWARE # START SOFTWARE #
########################################################################################################################

# function: starting software
async def start_software(retries: int, timestamp: Optional[str] = None) -> None:
    LOGGER.info(f'SOFTWARE | {NAME_SOFTWARE} has been started!')

    if timestamp:
        runs_list = [db_runs_o.get_run_dict(timestamp)]
    else:
        runs_list = db_runs_o.get_runs_list()

    tasks = []
    for run_dict in runs_list:
        tasks.append(asyncio.create_task(execute_run(retries, run_dict[KEY_R_TIMESTAMP])))
    await asyncio.wait(tasks)
    n_accounts_executed = 0
    for task in tasks:
        n_accounts_executed += 1 if task.result() else 0

    # message
    LOGGER.info(f'SOFTWARE | Accounts ({n_accounts_executed}/{len(runs_list)}) were executed!')
    LOGGER.info(f'SOFTWARE | {NAME_SOFTWARE} has been finished!')


########################################################################################################################
# EXECUTE RUN # EXECUTE RUN # EXECUTE RUN # EXECUTE RUN # EXECUTE RUN # EXECUTE RUN # EXECUTE RUN # EXECUTE RUN # EXECUT
########################################################################################################################

# function: executing a run (timestamp)
async def execute_run(retries: int, run_timestamp: str) -> bool:
    for i in range(1, retries + 1):
        run_dict = db_runs_o.get_run_dict(run_timestamp)
        if run_dict == {}:
            LOGGER.error(f'SOFTWARE | EXECUTE | run: {run_timestamp} | Does not exist!')
            return False

        # message
        anonym_address = get_anonymous_string(run_dict[KEY_R_ACCOUNT_DICT][KEY_A_ADDRESS_CLIENT])
        LOGGER.debug(f'SOFTWARE | RETRIES | add: {anonym_address} | {i}/{retries}')

        result = await execute_run_dict(run_dict)
        if result:
            return True
        else:
            # sleep: LONG
            if i != retries:
                await asyncio.sleep(random.randint(DEFAULT_TIME_SLEEP_LONG_MIN, DEFAULT_TIME_SLEEP_LONG_MAX))

    # return
    return False


########################################################################################################################
# EXECUTE RUN DICT # EXECUTE RUN DICT # EXECUTE RUN DICT # EXECUTE RUN DICT # EXECUTE RUN DICT # EXECUTE RUN DICT # EXEC
########################################################################################################################

# function: executing a run (dict)
async def execute_run_dict(run_dict: dict) -> bool:
    run_timestamp = run_dict[KEY_R_TIMESTAMP]
    run_account_dict = run_dict[KEY_R_ACCOUNT_DICT]
    run_commands_list: list = run_dict[KEY_R_COMMANDS_LIST]
    time_sleep_start = run_account_dict[KEY_A_TIME_SLEEP_START]
    anonym_address = get_anonymous_string(run_account_dict[KEY_A_ADDRESS_CLIENT])
    main_message = f'SOFTWARE | EXECUTE | add: {anonym_address}'

    t_index = -1
    for command_dict in run_commands_list:
        if command_dict[KEY_C_STATUS] == VAL_C_DEFAULT:
            t_index = run_commands_list.index(command_dict)
            break

    # sleep: USER (START)
    if time_sleep_start != VAL_A_NAN:
        if (t_index == 0) and (run_commands_list[t_index][KEY_C_COMMAND] in [VAL_C_MINT, VAL_C_BRIDGE]):
            await asyncio.sleep(time_sleep_start)

    # message
    LOGGER.info(f'{main_message} | Running...')

    # run: start
    if t_index != -1:
        result = await start_run(main_message, run_dict, t_index)
        if not result:
            LOGGER.error(f'{main_message} | Has been stopped!')
            return False

    # run: delete
    db_runs_o.delete_run(run_timestamp)

    # message
    LOGGER.info(f'{main_message} | Done!')
    return True


########################################################################################################################
# START RUN # START RUN # START RUN # START RUN # START RUN # START RUN # START RUN # START RUN # START RUN # START RUN
########################################################################################################################

# function: starting run (from the specific command)
async def start_run(main_message: str, run_dict: dict, start_index: int) -> bool:
    run_account_dict: dict = run_dict[KEY_R_ACCOUNT_DICT]
    run_commands_list: list = run_dict[KEY_R_COMMANDS_LIST]
    time_sleep_min = run_account_dict[KEY_A_TIME_SLEEP_MIN]
    time_sleep_max = run_account_dict[KEY_A_TIME_SLEEP_MAX]
    time_sleep_min = time_sleep_min if (time_sleep_min != VAL_A_NAN) else DEFAULT_TIME_SLEEP_LONG_MIN
    time_sleep_max = time_sleep_max if (time_sleep_max != VAL_A_NAN) else DEFAULT_TIME_SLEEP_LONG_MAX

    command_index = start_index
    for command_dict in run_commands_list[start_index:]:
        if command_dict[KEY_C_COMMAND] in [VAL_C_MINT, VAL_C_MINT_VERIFY, VAL_C_MINT_RECEIPT, VAL_C_MINT_CONFIRM]:
            main_message_new = f'{main_message} | {command_dict[KEY_C_NETWORK]}[mint]'
        else:
            main_message_new = f'{main_message} | {command_dict[KEY_C_NETWORK][0]} -> {command_dict[KEY_C_NETWORK][1]}'

        # command: checks
        check_01 = command_dict[KEY_C_COMMAND] in [VAL_C_MINT, VAL_C_BRIDGE]
        check_02 = command_dict[KEY_C_COMMAND] in [VAL_C_MINT_CONFIRM, VAL_C_BRIDGE_CONFIRM]
        check_03 = command_index == len(run_commands_list) - 1
        check_04 = command_index == start_index

        # message
        if check_01 or check_04:
            LOGGER.info(f'{main_message_new} | Running...')

        # command: start
        result, msg = await start_command(main_message_new, run_dict, command_index)
        if result == -1:
            return False
        else:
            run_dict = msg

        # message
        if check_02:
            LOGGER.info(f'{main_message_new} | Done!')

        # command: count
        command_index += 1

        # sleep: USER (MIN-MAX)
        if check_02 and not check_03:
            await asyncio.sleep(random.randint(time_sleep_min, time_sleep_max))
        elif check_02 and check_03:
            break
        else:
            await asyncio.sleep(random.randint(DEFAULT_TIME_SLEEP_SHORT_MIN, DEFAULT_TIME_SLEEP_SHORT_MAX))

    # return
    return True


########################################################################################################################
# START COMMAND # START COMMAND # START COMMAND # START COMMAND # START COMMAND # START COMMAND # START COMMAND # START
########################################################################################################################

# function: starting command (specific)
async def start_command(main_message: str, run_dict: dict, command_index: int) -> (int, Optional[dict]):
    command_functions = {
        VAL_C_MINT: mint,
        VAL_C_MINT_VERIFY: mint_verify, VAL_C_MINT_RECEIPT: mint_receipt, VAL_C_MINT_CONFIRM: mint_confirm,
        VAL_C_BRIDGE: bridge,
        VAL_C_BRIDGE_VERIFY: bridge_verify, VAL_C_BRIDGE_CONFIRM: bridge_confirm,
    }
    command = run_dict[KEY_R_COMMANDS_LIST][command_index][KEY_C_COMMAND]

    if command in command_functions:
        result, msg = await command_functions[command](main_message, run_dict, command_index)
        if result == -1:
            return -1, None
        else:
            return 0, msg
    else:
        LOGGER.error(f'{main_message} | No such a command: {command}!')
        return -1, None


########################################################################################################################
# MINT # MINT # MINT # MINT # MINT # MINT # MINT # MINT # MINT # MINT # MINT # MINT # MINT # MINT # MINT # MINT # MINT #
########################################################################################################################

# function: minting NFT (PAYABLE)
async def mint(main_message: str, run_dict: dict, command_index: int) -> (int, Optional[dict]):
    account_dict = run_dict[KEY_R_ACCOUNT_DICT]
    command_dict = run_dict[KEY_R_COMMANDS_LIST][command_index]
    result, msg = await func_common.get_client(account_dict=account_dict, command_dict=command_dict)

    if result == -1:
        LOGGER.error(f'{main_message} | Could not get a client! | {msg}')
        return -1, None
    else:
        client: Client = msg
        hyperlane = Hyperlane(client)
        network_name = client.name_network
        network: Network = NETWORKS_OBJECTS_DICT[network_name]
        address_contract, gas_increase_base = network.address_contract, network.gas_increase_base_mint
        max_eth_gwei = account_dict[KEY_A_MAX_ETH_GWEI] if (account_dict[KEY_A_MAX_ETH_GWEI] != VAL_A_NAN) else None

        result, msg = await hyperlane.mint_nft(
            address_contract=address_contract,
            gas_increase_gas=None, gas_increase_base=gas_increase_base, max_eth_gwei=max_eth_gwei,
        )
        if result == -1:
            if ('insufficient funds' in str(msg)) or ('gas required exceeds allowance' in str(msg)):
                if (account_dict[KEY_A_OKX_API_KEY] != VAL_A_NAN) and network.deposit_bool:
                    result, msg = await deposit_wallet_via_okx(main_message, account_dict, command_dict, network_name)
                    if result == -1:
                        LOGGER.error(f'{main_message} | Could not deposit {network.name_token} via OKX!')
                        return -1, None
                    else:
                        return await mint(main_message, run_dict, command_index)
                else:
                    LOGGER.error(f'{main_message} | Insufficient funds on {network_name}!')
                    return -1, None
            else:
                LOGGER.error(f'{main_message} | Could not mint an NFT! | {msg}')
                return -1, None
        else:
            run_dict = func_common.update_run_dict(run_dict, command_index, VAL_C_OK, msg)
            result, msg = db_runs_o.save_run_dict(run_dict)
            if result == -1:
                LOGGER.error(f'{main_message} | Could not save run_dict to database! | {msg}')
                return -1, None
            else:
                return 0, run_dict


########################################################################################################################
# MINT VERIFY # MINT VERIFY # MINT VERIFY # MINT VERIFY # MINT VERIFY # MINT VERIFY # MINT VERIFY # MINT VERIFY # MINT V
########################################################################################################################

# function: verifying NFT mint (NON-PAYABLE)
async def mint_verify(main_message: str, run_dict: dict, command_index: int) -> (int, Optional[dict]):
    account_dict = run_dict[KEY_R_ACCOUNT_DICT]
    command_dict = run_dict[KEY_R_COMMANDS_LIST][command_index]
    result, msg = await func_common.get_client(account_dict=account_dict, command_dict=command_dict)

    if result == -1:
        LOGGER.error(f'{main_message} | Could not get a client! | {msg}')
        return -1, None
    else:
        client: Client = msg
        transaction_hash = run_dict[KEY_R_COMMANDS_LIST][command_index - 1][KEY_C_VALUE]

        if transaction_hash == VAL_C_DEFAULT:
            LOGGER.error(f'{main_message} | No transaction_hash to verify the mint!')
            return -1, None
        else:
            transaction_hash: HexBytes = transaction_hash
            result, msg = await client.verify_transaction(transaction_hash=transaction_hash)

            if result == -1:
                if 'is not in the chain after' in str(msg):
                    run_dict = func_common.update_run_dict(run_dict, command_index - 1, VAL_C_DEFAULT, VAL_C_DEFAULT)
                    result, msg_ = db_runs_o.save_run_dict(run_dict)
                    if result == -1:
                        LOGGER.error(f'{main_message} | Could not save run_dict to database! | {msg_}')
                        return -1, None
                LOGGER.error(f'{main_message} | Could not verify the mint[{transaction_hash}]! | {msg}')
                return -1, None
            else:
                if not msg:
                    LOGGER.error(f'{main_message} | The mint[{transaction_hash}] did not verified!')
                    return -1, None
                else:
                    run_dict = func_common.update_run_dict(run_dict, command_index, VAL_C_OK, VAL_C_TRUE)
                    result, msg = db_runs_o.save_run_dict(run_dict)
                    if result == -1:
                        LOGGER.error(f'{main_message} | Could not save run_dict to database! | {msg}')
                        return -1, None
                    else:
                        return 0, run_dict


########################################################################################################################
# MINT RECEIPT # MINT RECEIPT # MINT RECEIPT # MINT RECEIPT # MINT RECEIPT # MINT RECEIPT # MINT RECEIPT # MINT RECEIPT
########################################################################################################################

# function: getting NFT id (NON-PAYABLE)
async def mint_receipt(main_message: str, run_dict: dict, command_index: int) -> (int, Optional[dict]):
    account_dict = run_dict[KEY_R_ACCOUNT_DICT]
    command_dict = run_dict[KEY_R_COMMANDS_LIST][command_index]
    result, msg = await func_common.get_client(account_dict=account_dict, command_dict=command_dict)

    if result == -1:
        LOGGER.error(f'{main_message} | Could not get a client! | {msg}')
        return -1, None
    else:
        client: Client = msg
        transaction_hash = run_dict[KEY_R_COMMANDS_LIST][command_index - 2][KEY_C_VALUE]

        if transaction_hash == VAL_C_DEFAULT:
            LOGGER.error(f'{main_message} | No transaction_hash to verify mint!')
            return -1, None
        else:
            hyperlane = Hyperlane(client)
            transaction_hash: HexBytes = transaction_hash
            result, msg = await hyperlane.get_nft_id(transaction_hash=transaction_hash)

            if result == -1:
                LOGGER.error(f'{main_message} | Could not get NFT id from the blockchain! | {msg}')
                return -1, None
            else:
                run_dict = func_common.update_run_dict(run_dict, command_index, VAL_C_OK, msg)
                run_dict[KEY_R_ACCOUNT_DICT][KEY_A_NFT_ID] = msg
                result, msg = db_runs_o.save_run_dict(run_dict)
                if result == -1:
                    LOGGER.error(f'{main_message} | Could not save run_dict to database! | {msg}')
                    return -1, None
                else:
                    return 0, run_dict


########################################################################################################################
# MINT CONFIRM # MINT CONFIRM # MINT CONFIRM # MINT CONFIRM # MINT CONFIRM # MINT CONFIRM # MINT CONFIRM # MINT CONFIRM
########################################################################################################################

# function: confirming NFT mint (NON-PAYABLE)
async def mint_confirm(main_message: str, run_dict: dict, command_index: int) -> (int, Optional[dict]):
    command_dict = run_dict[KEY_R_COMMANDS_LIST][command_index]
    account_dict = run_dict[KEY_R_ACCOUNT_DICT]
    nft_id = account_dict[KEY_A_NFT_ID]

    if nft_id == VAL_A_NAN:
        LOGGER.error(f'{main_message} | No NFT id found in account_dict!')
        return -1, None
    else:
        while True:
            result, msg = await func_common.get_client(account_dict=account_dict, command_dict=command_dict)

            if result == -1:
                LOGGER.error(f'{main_message} | Could not get a client! | {msg}')
                return -1, None
            else:
                client: Client = msg
                hyperlane = Hyperlane(client)
                network: Network = NETWORKS_OBJECTS_DICT[client.name_network]
                result, msg = await hyperlane.check_nft_owner(address_contract=network.address_contract, nft_id=nft_id)

                if result == -1:
                    LOGGER.error(f'{main_message} | Could not check NFT owner! | {msg}')
                    return -1, None
                else:
                    if msg == ADDRESS_ZERO:
                        LOGGER.debug(f'{main_message} | Could not find NFT[{nft_id}] in the chain!')
                    else:
                        if msg != client.address:
                            LOGGER.error(f'{main_message} | NFT[{nft_id}] is not yours! | NFT belongs to: {msg}')
                            return -1, None
                        else:
                            run_dict = func_common.update_run_dict(run_dict, command_index, VAL_C_OK, VAL_C_TRUE)
                            result, msg = db_runs_o.save_run_dict(run_dict)
                            if result == -1:
                                LOGGER.error(f'{main_message} | Could not save run_dict to database! | {msg}')
                                return -1, None
                            else:
                                return 0, run_dict

            # sleep: LONG
            await asyncio.sleep(random.randint(DEFAULT_TIME_SLEEP_LONG_MIN, DEFAULT_TIME_SLEEP_LONG_MAX))


########################################################################################################################
# BRIDGE # BRIDGE # BRIDGE # BRIDGE # BRIDGE # BRIDGE # BRIDGE # BRIDGE # BRIDGE # BRIDGE # BRIDGE # BRIDGE # BRIDGE # B
########################################################################################################################

# function: bridging NFT (PAYABLE)
async def bridge(main_message: str, run_dict: dict, command_index: int) -> (int, Optional[dict]):
    account_dict = run_dict[KEY_R_ACCOUNT_DICT]
    nft_id = account_dict[KEY_A_NFT_ID]

    if nft_id == VAL_A_NAN:
        LOGGER.error(f'{main_message} | No NFT id found in account_dict!')
        return -1, None
    else:
        command_dict = run_dict[KEY_R_COMMANDS_LIST][command_index]
        domain_to = NETWORKS_OBJECTS_DICT[command_dict[KEY_C_NETWORK][1]].domain
        result, msg = await func_common.get_client(account_dict=account_dict, command_dict=command_dict)

        if result == -1:
            LOGGER.error(f'{main_message} | Could not get a client! | {msg}')
            return -1, None
        else:
            client: Client = msg
            hyperlane = Hyperlane(client)
            network_name = client.name_network
            network: Network = NETWORKS_OBJECTS_DICT[network_name]
            address_contract, gas_increase_base = network.address_contract, network.gas_increase_base_mint
            max_eth_gwei = account_dict[KEY_A_MAX_ETH_GWEI] if (account_dict[KEY_A_MAX_ETH_GWEI] != VAL_A_NAN) else None

            result, msg = await hyperlane.bridge_nft(
                address_contract=address_contract, domain_to=domain_to, nft_id=nft_id,
                gas_increase_gas=None, gas_increase_base=gas_increase_base, max_eth_gwei=max_eth_gwei,
            )
            if result == -1:
                if ('insufficient funds' in str(msg)) or ('gas required exceeds allowance' in str(msg)):
                    if (account_dict[KEY_A_OKX_API_KEY] != VAL_A_NAN) and network.deposit_bool:
                        result, msg = await deposit_wallet_via_okx(
                            main_message, account_dict, command_dict, network_name
                        )
                        if result == -1:
                            LOGGER.error(f'{main_message} | Could not deposit {network.name_token} via OKX!')
                            return -1, None
                        else:
                            return await bridge(main_message, run_dict, command_index)
                    else:
                        LOGGER.error(f'{main_message} | Insufficient funds on {network_name}!')
                        return -1, None
                else:
                    LOGGER.error(f'{main_message} | Could not bridge an NFT! | {msg}')
                    return -1, None
            else:
                run_dict = func_common.update_run_dict(run_dict, command_index, VAL_C_OK, msg)
                result, msg = db_runs_o.save_run_dict(run_dict)
                if result == -1:
                    LOGGER.error(f'{main_message} | Could not save run_dict to database! | {msg}')
                    return -1, None
                else:
                    return 0, run_dict


########################################################################################################################
# BRIDGE VERIFY # BRIDGE VERIFY # BRIDGE VERIFY # BRIDGE VERIFY # BRIDGE VERIFY # BRIDGE VERIFY # BRIDGE VERIFY # BRIDGE
########################################################################################################################

# function: verifying NFT bridge (NON-PAYABLE)
async def bridge_verify(main_message: str, run_dict: dict, command_index: int) -> (int, Optional[dict]):
    account_dict = run_dict[KEY_R_ACCOUNT_DICT]
    command_dict = run_dict[KEY_R_COMMANDS_LIST][command_index]
    result, msg = await func_common.get_client(account_dict=account_dict, command_dict=command_dict)

    if result == -1:
        LOGGER.error(f'{main_message} | Could not get a client! | {msg}')
        return -1, None
    else:
        client: Client = msg
        transaction_hash = run_dict[KEY_R_COMMANDS_LIST][command_index - 1][KEY_C_VALUE]

        if transaction_hash == VAL_C_DEFAULT:
            LOGGER.error(f'{main_message} | No transaction_hash to verify the bridge!')
            return -1, None
        else:
            transaction_hash: HexBytes = transaction_hash
            result, msg = await client.verify_transaction(transaction_hash=transaction_hash)

            if result == -1:
                if 'is not in the chain after' in str(msg):
                    run_dict = func_common.update_run_dict(run_dict, command_index - 1, VAL_C_DEFAULT, VAL_C_DEFAULT)
                    result, msg_ = db_runs_o.save_run_dict(run_dict)
                    if result == -1:
                        LOGGER.error(f'{main_message} | Could not save run_dict to database! | {msg_}')
                        return -1, None
                LOGGER.error(f'{main_message} | Could not verify the bridge[{transaction_hash}]! | {msg}')
                return -1, None
            else:
                if not msg:
                    LOGGER.error(f'{main_message} | The bridge[{transaction_hash}] did not verified!')
                    return -1, None
                else:
                    run_dict = func_common.update_run_dict(run_dict, command_index, VAL_C_OK, VAL_C_TRUE)
                    result, msg = db_runs_o.save_run_dict(run_dict)
                    if result == -1:
                        LOGGER.error(f'{main_message} | Could not save run_dict to database! | {msg}')
                        return -1, None
                    else:
                        return 0, run_dict


########################################################################################################################
# BRIDGE CONFIRM # BRIDGE CONFIRM # BRIDGE CONFIRM # BRIDGE CONFIRM # BRIDGE CONFIRM # BRIDGE CONFIRM # BRIDGE CONFIRM #
########################################################################################################################

# function: confirming NFT bridge (NON-PAYABLE)
async def bridge_confirm(main_message: str, run_dict: dict, command_index: int) -> (int, Optional[dict]):
    command_dict = run_dict[KEY_R_COMMANDS_LIST][command_index]
    account_dict = run_dict[KEY_R_ACCOUNT_DICT]
    nft_id = account_dict[KEY_A_NFT_ID]

    if nft_id == VAL_A_NAN:
        LOGGER.error(f'{main_message} | No NFT id found in account_dict!')
        return -1, None
    else:
        while True:
            result, msg = await func_common.get_client(account_dict=account_dict, command_dict=command_dict)

            if result == -1:
                LOGGER.error(f'{main_message} | Could not get a client! | {msg}')
                return -1, None
            else:
                client: Client = msg
                hyperlane = Hyperlane(client)
                network: Network = NETWORKS_OBJECTS_DICT[client.name_network]
                result, msg = await hyperlane.check_nft_owner(address_contract=network.address_contract, nft_id=nft_id)

                if result == -1:
                    LOGGER.error(f'{main_message} | Could not check NFT owner! | {msg}')
                    return -1, None
                else:
                    if msg == ADDRESS_ZERO:
                        LOGGER.debug(f'{main_message} | Could not find NFT[{nft_id}] in the chain!')
                    else:
                        if msg != client.address:
                            LOGGER.error(f'{main_message} | NFT[{nft_id}] is not yours! | NFT belongs to: {msg}')
                            return -1, None
                        else:
                            run_dict = func_common.update_run_dict(run_dict, command_index, VAL_C_OK, VAL_C_TRUE)
                            result, msg = db_runs_o.save_run_dict(run_dict)
                            if result == -1:
                                LOGGER.error(f'{main_message} | Could not save run_dict to database! | {msg}')
                                return -1, None
                            else:
                                return 0, run_dict

            # sleep: LONG
            await asyncio.sleep(random.randint(DEFAULT_TIME_SLEEP_LONG_MIN, DEFAULT_TIME_SLEEP_LONG_MAX))


########################################################################################################################
# DEPOSIT WALLET VIA OKX # DEPOSIT WALLET VIA OKX # DEPOSIT WALLET VIA OKX # DEPOSIT WALLET VIA OKX # DEPOSIT WALLET VIA
########################################################################################################################

# function: depositing metamask wallet via OKX
async def deposit_wallet_via_okx(
        main_message: str, account_dict: dict, command_dict: dict, network: str
) -> (int, Optional[Exception]):

    # message
    main_message = f'{main_message} | {network}'
    LOGGER.info(f'{main_message} | Depositing...')

    # OKX: check
    okx = OkxFunding(
        api_key=account_dict[KEY_A_OKX_API_KEY], api_secret=account_dict[KEY_A_OKX_SECRET_KEY],
        passphrase=account_dict[KEY_A_OKX_PASSPHRASE], proxy=''
    )
    result, msg = okx.check_keys()
    if result == -1:
        LOGGER.error(f'{main_message} | Could not connect to the OKX! | {msg}')
        return -1, None

    # OKX: converting USD to native chain
    network: Network = NETWORKS_OBJECTS_DICT[network]
    deposit_ticker, deposit_chain = network.name_token, network.deposit_chain
    deposit_usd_min, deposit_usd_max = network.deposit_usd_min, network.deposit_usd_max
    deposit_usd = cmn.generate_random_float(round(deposit_usd_min, 5), round(deposit_usd_max, 5), 5)
    result, msg = await okx.convert_usd_to_native(value=deposit_usd, ticker=deposit_ticker, network=deposit_chain)
    if result == -1:
        LOGGER.error(f'{main_message} | Could not convert USD to {network.name_token} via OKX! | {msg}')
        return -1, None

    # OKX: getting network information
    deposit_amount: float = msg
    result, msg = await okx.get_network(ticker=network.name_token, chain=network.deposit_chain)
    if result == -1:
        LOGGER.error(f'{main_message} | Could not get network information via OKX! | {msg}')
        return -1, None

    # OKX: checking minimum amount to withdraw
    network_info: NetworkInfo = msg
    if deposit_amount < network_info.min_wd:
        LOGGER.error(f'{main_message} | Withdrawal amount is less than a minimal withdrawal amount!')
        return -1, None

    # OKX: posting withdrawal (on-chain)
    deposit_fee = network_info.min_fee
    result, msg = await okx.post_withdrawal_on_chain(
        ticker=deposit_ticker, chain=deposit_chain, address=account_dict[KEY_A_ADDRESS_CLIENT], amount=deposit_amount,
        fee=deposit_fee
    )
    if result == -1:
        LOGGER.error(f'{main_message} | Could not post withdrawal on-chain via OKX! | {msg}')
        return -1, None

    # OKX: waiting for withdrawal completeness
    deposit_withdrawal_id = msg
    while True:
        result, msg = await okx.check_withdrawal(deposit_withdrawal_id)
        if result == -1:
            LOGGER.error(f'{main_message} | Could not check withdrawal via OKX! | {msg}')
            return -1, None
        else:
            if not msg:
                LOGGER.debug(f'{main_message} | Not deposited yet!')
            else:
                break

        # sleep: LONG
        await asyncio.sleep(random.randint(DEFAULT_TIME_SLEEP_LONG_MIN, DEFAULT_TIME_SLEEP_LONG_MAX))

    # message
    LOGGER.info(f'{main_message} | Done!')
    return 0, None


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
