########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# types
from typing import Union
from requests import Response

# library
import hmac
import json
import base64
import datetime
import requests

# dir: head
from dir_OKX.okx_head import *

# dir: globals
from __system__.dir_logger.lg_main import LOGGER


########################################################################################################################
# OKX FUNDING CLASS # OKX FUNDING CLASS # OKX FUNDING CLASS # OKX FUNDING CLASS # OKX FUNDING CLASS # OKX FUNDING CLASS
########################################################################################################################

# class: Okx (funding)
class OkxFunding:
    __net_cab = 'https://www.okx.cab'
    __net_com = 'https://www.okx.com'
    __net = __net_com

    # constructor
    def __init__(self, proxy: str = '', api_key: str = None, api_secret: str = None, passphrase: str = None) -> None:
        """
        Creating OkxFunding object

        Args:
            proxy (str, not required): proxy
            api_key (str, required): API key
            api_secret (str, required): API secret
            passphrase (str, required): passphrase
        """

        self._proxy = proxy
        self._api_key = api_key
        self._api_secret = api_secret
        self._passphrase = passphrase
        self._proxy_string = proxy
        self._httpClient = requests.Session()

    ####################################################################################################################
    # GET TIME # GET TIME # GET TIME # GET TIME # GET TIME # GET TIME # GET TIME # GET TIME # GET TIME # GET TIME # GET
    ####################################################################################################################

    # function: getting time
    @staticmethod
    def _get_time() -> str:
        now = datetime.datetime.utcnow()
        time = now.isoformat('T', 'milliseconds')
        return time + 'Z'

    ####################################################################################################################
    # GENERATE SIGNATURE # GENERATE SIGNATURE # GENERATE SIGNATURE # GENERATE SIGNATURE # GENERATE SIGNATURE # GENERATE
    ####################################################################################################################

    # function: generating hashing signature
    def _generate_signature(self, timestamp, method, endpoint, body) -> bytes:
        message = str(timestamp) + str.upper(method) + endpoint + str(body)
        mac = hmac.new(bytes(self._api_secret, encoding='utf-8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        signature = base64.b64encode(mac.digest())
        return signature

    ####################################################################################################################
    # HTTP REQUEST # HTTP REQUEST # HTTP REQUEST # HTTP REQUEST # HTTP REQUEST # HTTP REQUEST # HTTP REQUEST # HTTP REQU
    ####################################################################################################################

    # functon: getting http request
    def _http_request(self, endpoint, method, body) -> Response:
        timestamp = self._get_time()
        headers = {
            'OK-ACCESS-KEY': self._api_key,
            'OK-ACCESS-PASSPHRASE': self._passphrase,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-SIGN': self._generate_signature(timestamp, method, endpoint, json.dumps(
                body)) if method == 'POST' else self._generate_signature(timestamp, method, endpoint, body),
        }
        url = self.__net + endpoint

        proxy = {
            'http': f'http://{self._proxy}',
            'https': f'http://{self._proxy}',
        } if self._proxy_string != '' else None

        if method == 'POST':
            response = self._httpClient.post(url, headers=headers, json=body, proxies=proxy)
        else:
            response = self._httpClient.request(method, url + body, headers=headers, proxies=proxy)
        return response

    ####################################################################################################################
    # CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS
    ####################################################################################################################

    # function: checking keys for working
    def check_keys(self) -> (int, Union[bool, Exception]):
        endpoint = '/api/v5/account/balance'
        method = 'GET'
        body = ''
        try:
            response = self._http_request(endpoint, method, body)
            LOGGER.debug(f'RESPONSE: {response.json()}')
            status_code = str(response.status_code)
            if status_code == '200':
                return 0, True
            else:
                return -1, False
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # GET TICKER PRICE # GET TICKER PRICE # GET TICKER PRICE # GET TICKER PRICE # GET TICKER PRICE # GET TICKER PRICE #
    ####################################################################################################################

    # function: getting ticker price
    async def get_ticker_price(self, ticker: str) -> (int, Union[float, Exception]):
        endpoint = '/api/v5/public/price-limit'
        method = 'GET'
        body = f'?instId={ticker}-USDT'
        try:
            response = self._http_request(endpoint, method, body)
            LOGGER.debug(f'RESPONSE: {response.json()}')
            data = response.json()['data'][0]
            return 0, round((float(data['buyLmt']) + float(data['sellLmt'])) / 2, 2)
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # GET NETWORK INFO # GET NETWORK INFO # GET NETWORK INFO # GET NETWORK INFO # GET NETWORK INFO # GET NETWORK INFO #
    ####################################################################################################################

    # function: getting networks
    async def get_network(self, ticker: str, chain: str) -> (int, Union[NetworkInfo, Exception]):
        endpoint = '/api/v5/asset/currencies'
        method = 'GET'
        body = f'?ccy={ticker}'
        try:
            response = self._http_request(endpoint, method, body)
            LOGGER.debug(f'RESPONSE: {response.json()}')
            data = response.json()['data']
            for ntw in data:
                if str(ntw['chain']) == chain:
                    network = NetworkInfo(
                        ticker=ticker,
                        chain=str(ntw['chain']),
                        wd_bool=bool(ntw['canWd']),
                        min_wd=float(ntw['minWd']),
                        max_wd=float(ntw['maxWd']),
                        min_fee=float(ntw['minFee']),
                        max_fee=float(ntw['maxFee']),
                        precision=int(ntw['wdTickSz']),
                    )
                    return 0, network
            return -1, Exception('No such a network on OKX!')
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # CONVERT FROM USD TO NATIVE COIN # CONVERT FROM USD TO NATIVE COIN # CONVERT FROM USD TO NATIVE COIN # CONVERT FROM
    ####################################################################################################################

    # function: converting value from USD to native coin
    async def convert_usd_to_native(self, value: float, ticker: str, network: str) -> (int, Union[float, Exception]):
        try:
            result, msg = await self.get_ticker_price(ticker=ticker)
            if result != -1:
                price: float = msg
                result, msg = await self.get_network(ticker=ticker, chain=network)
                if result != -1:
                    return 0, round(value/price, msg.precision)
                else:
                    return -1, Exception(f'Something is wrong in function get_network: {msg}')
            else:
                return -1, Exception(f'Something is wrong in function get_ticker_price: {msg}')
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # POST WITHDRAWAL ON CHAIN # POST WITHDRAWAL ON CHAIN # POST WITHDRAWAL ON CHAIN # POST WITHDRAWAL ON CHAIN # POST W
    ####################################################################################################################

    # function: withdrawal crypto
    async def post_withdrawal_on_chain(
            self, ticker: str, chain: str, address: str, amount: float, fee: float
    ) -> (int, Union[str, Exception]):
        endpoint = '/api/v5/asset/withdrawal'
        method = 'POST'
        body = {
            'ccy': ticker,
            'amt': amount,
            'dest': 4,
            'toAddr': address,
            'fee': fee,
            'chain': chain
        }
        try:
            response = self._http_request(endpoint, method, body)
            LOGGER.debug(f'RESPONSE: {response.json()}')
            status_code = str(response.status_code)
            json = response.json()
            if status_code == '200':
                data = json['data']
                if data:
                    wd_id = ''
                    for part in data:
                        wd_id = str(part['wdId'])
                    return 0, wd_id
                else:
                    return -1, Exception(json['msg'])
            else:
                if 'msg' in json:
                    return -1, Exception(json['msg'])
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # GET WITHDRAWAL HISTORY # GET WITHDRAWAL HISTORY # GET WITHDRAWAL HISTORY # GET WITHDRAWAL HISTORY # GET WITHDRAWAL
    ####################################################################################################################

    # function: getting withdrawal history (by wd_id)
    async def get_withdrawal_history(self, wd_id: str) -> (int, Union[dict, Exception]):
        endpoint = '/api/v5/asset/withdrawal-history'
        method = 'GET'
        body = f'?wdId={wd_id}'
        try:
            response = self._http_request(endpoint, method, body)
            LOGGER.debug(f'RESPONSE: {response.json()}')
            data = response.json()['data']
            if data:
                if data[0]['wdId'] == wd_id:
                    return 0, data[0]
                else:
                    return -1, Exception(f'Wrong withdrawal[{wd_id}] dictionary!')
            else:
                return -1, Exception(f'No such a withdrawal[{wd_id}] found on OKX!')
        except Exception as E:
            return -1, E

    ####################################################################################################################
    # CHECK WITHDRAWAL # CHECK WITHDRAWAL # CHECK WITHDRAWAL # CHECK WITHDRAWAL # CHECK WITHDRAWAL # CHECK WITHDRAWAL #
    ####################################################################################################################

    # function: checking withdrawal completeness (by wd_id)
    async def check_withdrawal(self, wd_id: str) -> (int, Union[bool, Exception]):
        try:
            result, msg = await self.get_withdrawal_history(wd_id=wd_id)
            if result != -1:
                state = msg['state']
                if state not in ['-3', '-2', '-1']:
                    if state == '2':
                        return 0, True
                    else:
                        return 0, False
                else:
                    return -1, Exception(f'Withdrawal has been canceled!')
            else:
                return -1, Exception(f'Some problems in function get_withdrawal_history: {msg}')
        except Exception as E:
            return -1, E

########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
