########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# libraries
import time
import pandas as pd

# globals
from __system__.dir_logger.lg_main import LOGGER, NAME_SOFTWARE
from dir_Hyperlane.hl_glob import NETWORKS_OBJECTS_DICT
from dir_software.sft_glob import *

# dir: head
from dir_web3.wb3_head import Client
from dir_Hyperlane.hl_head import Hyperlane

# dir: func
from dir_software.sft_func import func_common
from dir_web3.wb3_func import get_anonymous_string


########################################################################################################################
# START SOFTWARE # START SOFTWARE # START SOFTWARE # START SOFTWARE # START SOFTWARE # START SOFTWARE # START SOFTWARE #
########################################################################################################################

# function: starting software (nft finder)
async def start_software(filename: str) -> None:
    LOGGER.info(f'SOFTWARE | {NAME_SOFTWARE} has been launched!')

    try:
        df = pd.read_excel(filename)
    except Exception as E:
        LOGGER.error(f'SOFTWARE | Could not read an excel file {filename} with error: {E}')
        return
    if df.empty:
        LOGGER.error(f'SOFTWARE | File {filename} is empty!')
        return
    accounts_list = func_common.clear_nan_values(df.to_dict(orient='records'))
    n_accounts = len(accounts_list)

    # message: headers
    print('|---------------|--------------------------|---------------|')
    print('| Address:      | Network:                 | NFT:          |')
    print('|---------------|--------------------------|---------------|')

    i = 1
    for account_dict in accounts_list:
        for network_name, network in NETWORKS_OBJECTS_DICT.items():
            proxy = account_dict[KEY_A_PROXY] if (account_dict[KEY_A_PROXY] != VAL_A_NAN) else None
            client = Client(account_dict[KEY_A_PRIVATE_KEY], network.url_rpc, network_name, proxy)
            result, msg = await Hyperlane(client).get_nft_ids(network.address_contract, network)

            if result == -1:
                LOGGER.error(f'SOFTWARE | {i}/{n_accounts} | {network.name_network} | Could not find NFTs! | {msg}')
            else:
                if msg:
                    for nft_id in msg:
                        nft_id = str(nft_id).ljust(13)
                        network = str(network_name).ljust(24)
                        anonym_address = str(get_anonymous_string(client.address)).ljust(13)
                        print(f'| {anonym_address} | {network} | {nft_id} |')
        print('|---------------|--------------------------|---------------|')
        i += 1

    # message
    time.sleep(1)
    LOGGER.info(f'SOFTWARE | {NAME_SOFTWARE} has been finished!')


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
