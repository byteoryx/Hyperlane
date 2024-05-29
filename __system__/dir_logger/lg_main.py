########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# libraries
import logging
import os
import datetime


########################################################################################################################
# NAMES # NAMES # NAMES # NAMES # NAMES # NAMES # NAMES # NAMES # NAMES # NAMES # NAMES # NAMES # NAMES # NAMES # NAMES
########################################################################################################################

# names: software
NAME_SOFTWARE = 'HyperlaneSoft'


########################################################################################################################
# PARAMETERS # PARAMETERS # PARAMETERS # PARAMETERS # PARAMETERS # PARAMETERS # PARAMETERS # PARAMETERS # PARAMETERS # P
########################################################################################################################

# parameters: config
LOG_FORMAT = '%(asctime).19s | %(levelname).3s | %(message)s'
LOG_DATE_TIME = '%Y-%m-%d %H:%M:%S'


########################################################################################################################
# FILENAME # FILENAME # FILENAME # FILENAME # FILENAME # FILENAME # FILENAME # FILENAME # FILENAME # FILENAME # FILENAME
########################################################################################################################

# filename: config
LOG_DIRECTORY = '__system__/dir_logger/storage'
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)
LOG_FILENAME = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log')
LOG_FILEPATH = os.path.join(LOG_DIRECTORY, LOG_FILENAME)


########################################################################################################################
# CONFIG # CONFIG # CONFIG # CONFIG # CONFIG # CONFIG # CONFIG # CONFIG # CONFIG # CONFIG # CONFIG # CONFIG # CONFIG # C
########################################################################################################################

# setting config
logging.basicConfig(
    level=logging.DEBUG, format=LOG_FORMAT, datefmt=LOG_DATE_TIME, filename=LOG_FILEPATH
)

# creating a stream handler and setting its level to DEBUG
console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.INFO)

# creating formatter and adding it to the handler
console_formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(console_formatter)


########################################################################################################################
# SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION
########################################################################################################################

# creating logger session
LOGGER = logging.getLogger(NAME_SOFTWARE)

# adding the handler to the logger
LOGGER.addHandler(console_handler)


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
