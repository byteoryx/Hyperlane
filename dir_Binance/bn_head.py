########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# libraries
import requests
from typing import Union
from requests import Response

# dir: globals
from __system__.dir_logger.lg_main import LOGGER


########################################################################################################################
# CLASS: BINANCE # CLASS: BINANCE # CLASS: BINANCE # CLASS: BINANCE # CLASS: BINANCE # CLASS: BINANCE # CLASS: BINANCE #
########################################################################################################################

# class: Binance
class BinanceSpot:
    __net_com = 'https://api.binance.com'
    __net = __net_com

    def __init__(self, api_key=None, secret_key=None, futures=False):
        """
        Initializing class parameters

        :param api_key: API key
        :param secret_key: secret API key
        :param futures: boolean, true for futures
        """
        self.futures = futures
        self.api_key = api_key
        self.secret_key = secret_key
        self.header = {'X-MBX-APIKEY': self.api_key}

    ####################################################################################################################
    # HTTP REQUEST # HTTP REQUEST # HTTP REQUEST # HTTP REQUEST # HTTP REQUEST # HTTP REQUEST # HTTP REQUEST # HTTP REQU
    ####################################################################################################################

    # function: sending http requests
    def http_request(self, method, endpoint, params) -> Response:
        if method == "GET":
            response = requests.get(url=self.__net_com + endpoint, params=params, headers=self.header)
        else:
            response = Response()

        LOGGER.debug(f'RESPONSE | {response.json()}')
        return response

    ####################################################################################################################
    # GET TICKER PRICE # GET TICKER PRICE # GET TICKER PRICE # GET TICKER PRICE # GET TICKER PRICE # GET TICKER PRICE #
    ####################################################################################################################

    # function: getting price by the ticker
    def get_ticker_price(self, symbol: str) -> (int, Union[float, Exception]):
        endpoint = '/api/v3/ticker/price'
        params = {'symbol': symbol}
        method = "GET"
        try:
            response = self.http_request(method=method, endpoint=endpoint, params=params)
            price = float(response.json()['price'])
            return 0, price
        except Exception as E:
            return -1, E

########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
