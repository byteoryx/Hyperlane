########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# libraries
from typing import Union
from web3.types import ChecksumAddress


########################################################################################################################
# ADDRESS50 TO BYTES32 # ADDRESS50 TO BYTES32 # ADDRESS50 TO BYTES32 # ADDRESS50 TO BYTES32 # ADDRESS50 TO BYTES32 # ADD
########################################################################################################################

# function: converting address (with length 50) to bytes type
def address50_to_bytes32(address: str) -> bytes:
    address_int = int(address, 16)
    bytes32_address = address_int.to_bytes(20, 'big').rjust(32, b'\x00')
    return bytes32_address


########################################################################################################################
# GET ANONYMOUS STRING # GET ANONYMOUS STRING # GET ANONYMOUS STRING # GET ANONYMOUS STRING # GET ANONYMOUS STRING # GET
########################################################################################################################

# function: getting anonymous string (e.g. address, private_key)
def get_anonymous_string(address: Union[str, ChecksumAddress]) -> str:
    return str(address)[:5] + "..." + str(address)[-5:]


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
