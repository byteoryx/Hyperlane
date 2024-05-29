########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# types
from typing import Union, Optional

# libraries
import json
import random
import requests


########################################################################################################################
# READ JSON FROM FILE # READ JSON FROM FILE # READ JSON FROM FILE # READ JSON FROM FILE # READ JSON FROM FILE # READ JSO
########################################################################################################################

# function: reading json from file
def read_json_from_file(path: str, encoding: Optional[str] = None) -> Union[list, dict]:
    return json.load(open(file=path, encoding=encoding))


########################################################################################################################
# FROM DECIMALS TO FLOAT # FROM DECIMALS TO FLOAT # FROM DECIMALS TO FLOAT # FROM DECIMALS TO FLOAT # FROM DECIMALS TO F
########################################################################################################################

# function: converting number written in decimals to float
def from_decimals_to_float(n_decimals: int, number: int) -> float:
    return float(number / (10 ** n_decimals))


########################################################################################################################
# PROXY # PROXY # PROXY # PROXY # PROXY # PROXY # PROXY # PROXY # PROXY # PROXY # PROXY # PROXY # PROXY # PROXY # PROXY
########################################################################################################################

# function
def get_proxy_address(proxy):
    if '@' in proxy:
        address = proxy.split('@')[-1].split(':')[0]
    else:
        address = proxy.split(':')[0]
    return address


# function: testing proxy (http)
def check_proxy_http(proxy):
    try:
        if ':' not in proxy:
            return False
        else:
            url = 'https://ipinfo.io/json'
            address = get_proxy_address(proxy)
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}',
            }
            response = requests.get(url=url, proxies=proxies)
            ip = response.json()['ip']
            if ip == address:
                return True
            else:
                return False
    except Exception:
        return False


########################################################################################################################
# GENERATE RANDOM NUMBER # GENERATE RANDOM NUMBER # GENERATE RANDOM NUMBER # GENERATE RANDOM NUMBER # GENERATE RANDOM NU
########################################################################################################################

# function: generating random floating number in range
def generate_random_float(left, right, precision):
    random_float = round(random.uniform(left, right), precision)
    return random_float


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
