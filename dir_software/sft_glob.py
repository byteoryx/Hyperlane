########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# dir: globals
from dir_Hyperlane.hl_glob import NETWORKS_NAMES_LIST


########################################################################################################################
# DEFAULT PARAMETERS # DEFAULT PARAMETERS # DEFAULT PARAMETERS # DEFAULT PARAMETERS # DEFAULT PARAMETERS # DEFAULT PARAM
########################################################################################################################

# default: time_sleep (lONG)
DEFAULT_TIME_SLEEP_LONG_MIN = 100
DEFAULT_TIME_SLEEP_LONG_MAX = 200


########################################################################################################################
# FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES
########################################################################################################################

# filenames: settings
FILENAME_SETTINGS = 'soft_settings.xlsx'


########################################################################################################################
# KEYS # KEYS # KEYS # KEYS # KEYS # KEYS # KEYS # KEYS # KEYS # KEYS # KEYS # KEYS # KEYS # KEYS # KEYS # KEYS # KEYS #
########################################################################################################################

# dictionary keys: account (file)
KEY_A_PRIVATE_KEY = 'private_key'
KEY_A_ADDRESS_FILE = 'address'
KEY_A_OKX_API_KEY = 'okx_api_key'
KEY_A_OKX_SECRET_KEY = 'okx_secret_key'
KEY_A_OKX_PASSPHRASE = 'okx_passphrase'
KEY_A_PROXY = 'proxy'
KEY_A_NFT_ID = 'nft_id'
KEY_A_NETWORK_MINT = 'network_mint'
KEY_A_MAX_ETH_GWEI = 'max_eth_gwei'
KEY_A_N_TXS_MIN = 'n_txs_min'
KEY_A_N_TXS_MAX = 'n_txs_max'
KEY_A_RANDOM_BOOL = 'random_bool'
KEY_A_TIME_SLEEP_MIN = 'time_sleep_min'
KEY_A_TIME_SLEEP_MAX = 'time_sleep_max'
KEY_A_TIME_SLEEP_START = 'time_sleep_start'
KEY_A_RETURN_BOOL = 'return_bool'

# dictionary keys: account (code)
KEY_A_ADDRESS_CLIENT = 'address_client'
KEY_A_NETWORKS_PATH_LIST = 'networks_path_list'
KEY_A_NETWORKS_CHAIN_LIST = 'networks_chain_list'

# dictionary keys: run
KEY_R_TIMESTAMP = 'timestamp'
KEY_R_ACCOUNT_DICT = 'account_dict'
KEY_R_COMMANDS_LIST = 'commands_list'

# dictionary keys: command
KEY_C_COMMAND = 'command'
KEY_C_STATUS = 'status'
KEY_C_VALUE = 'value'
KEY_C_NETWORK = 'network'


########################################################################################################################
# VALUES # VALUES # VALUES # VALUES # VALUES # VALUES # VALUES # VALUES # VALUES # VALUES # VALUES # VALUES # VALUES # V
########################################################################################################################

# dictionary values: account
VAL_A_NAN = 'NAN'
VAL_A_RANDOM = 'RANDOM'

# dictionary values: state
VAL_C_DEFAULT = ''
VAL_C_OK = 'OK'
VAL_C_TRUE = 'True'
VAL_C_FALSE = 'False'

# dictionary keys: command (commands)
VAL_C_MINT = 'mint'
VAL_C_MINT_VERIFY = 'mint_verify'
VAL_C_MINT_RECEIPT = 'mint_receipt'
VAL_C_MINT_CONFIRM = 'mint_confirm'
VAL_C_BRIDGE = 'bridge'
VAL_C_BRIDGE_VERIFY = 'bridge_verify'
VAL_C_BRIDGE_CONFIRM = 'bridge_confirm'


########################################################################################################################
# DEFAULT DICTS # DEFAULT DICTS # DEFAULT DICTS # DEFAULT DICTS # DEFAULT DICTS # DEFAULT DICTS # DEFAULT DICTS # DEFAUL
########################################################################################################################

# default dicts: command
DEFAULT_COMMAND_DICT = {
    KEY_C_COMMAND: VAL_C_DEFAULT,
    KEY_C_STATUS: VAL_C_DEFAULT,
    KEY_C_VALUE: VAL_C_DEFAULT,
}


########################################################################################################################
# EXCEL # EXCEL # EXCEL # EXCEL # EXCEL # EXCEL # EXCEL # EXCEL # EXCEL # EXCEL # EXCEL # EXCEL # EXCEL # EXCEL # EXCEL
########################################################################################################################

# excel: filenames
SETTINGS_MAIN = [
    KEY_A_PRIVATE_KEY, KEY_A_ADDRESS_FILE, KEY_A_OKX_API_KEY, KEY_A_OKX_SECRET_KEY, KEY_A_OKX_PASSPHRASE, KEY_A_PROXY,
    KEY_A_NFT_ID, KEY_A_NETWORK_MINT,
]
SETTINGS_PARAMETERS = [
    KEY_A_MAX_ETH_GWEI, KEY_A_N_TXS_MIN, KEY_A_N_TXS_MAX, KEY_A_RANDOM_BOOL, KEY_A_TIME_SLEEP_MIN, KEY_A_TIME_SLEEP_MAX,
    KEY_A_TIME_SLEEP_START, KEY_A_RETURN_BOOL,
]
EXCEL_HEADERS = SETTINGS_MAIN + NETWORKS_NAMES_LIST + SETTINGS_PARAMETERS


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
