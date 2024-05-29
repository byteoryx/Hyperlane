########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# libraries
from dataclasses import dataclass


########################################################################################################################
# ASSET BALANCE # ASSET BALANCE # ASSET BALANCE # ASSET BALANCE # ASSET BALANCE # ASSET BALANCE # ASSET BALANCE # ASSET
########################################################################################################################

# class: AssetBalance (funding)
@dataclass
class AssetBalance:
    ticker: str             # ticker
    balance: float          # balance
    avail_bal: float        # available balance to withdraw
    frozen_bal: float       # frozen balance

    # constructor
    def __init__(
            self, ticker: str = None, balance: float = None, avail_bal: float = None, frozen_bal: float = None,
    ) -> None:
        """
        Creating CoinFunding object

        Args:
            ticker (str, required)
            balance (str, required)
            avail_bal (str, required)
            frozen_bal (str, required)
        """

        self.ticker = ticker
        self.balance = balance
        self.avail_bal = avail_bal
        self.frozen_bal = frozen_bal


########################################################################################################################
# NETWORK INFO # NETWORK INFO # NETWORK INFO # NETWORK INFO # NETWORK INFO # NETWORK INFO # NETWORK INFO # NETWORK INFO
########################################################################################################################

# class: NetworkInfo (funding)
@dataclass
class NetworkInfo:
    ticker: str             # ticker
    chain: str              # chain name, e.g. USDT-ERC20, USDT-TRC20
    wd_bool: bool           # availability to withdraw to chain.
    min_wd: float           # minimum withdrawal amount of the currency in a single transaction
    max_wd: float           # maximum amount of currency withdrawal in a single transaction
    min_fee: float          # minimum withdrawal fee
    max_fee: float          # maximum withdrawal fee
    precision: int          # precision of a coin

    # constructor
    def __init__(
            self,
            ticker: str = None,
            chain: str = None,
            wd_bool: bool = None,
            min_wd: float = None,
            max_wd: float = None,
            min_fee: float = None,
            max_fee: float = None,
            precision: int = None,
    ) -> None:
        """
        Creating CoinFunding object

        Args:
            ticker (str, required)
            chain (str, required)
            wd_bool (bool, required)
            min_wd (float, required)
            max_wd (float, required)
            min_fee (float, required)
            max_fee (float, required)
            precision (int, required)
        """

        self.ticker = ticker
        self.chain = chain
        self.wd_bool = wd_bool
        self.min_wd = min_wd
        self.max_wd = max_wd
        self.min_fee = min_fee
        self.max_fee = max_fee
        self.precision = precision


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
