########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# libraries
import asyncio
import time

# dir: globals
from __system__.dir_logger.lg_main import LOGGER, NAME_SOFTWARE

# dir: func
from dir_database import db_runs_o
from dir_software.sft_func import func_launcher as launcher


########################################################################################################################
# MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN #
########################################################################################################################

# function: main
def main():
    try:
        print(f'Welcome to {NAME_SOFTWARE}!')
        time.sleep(1)

        db_runs_o.execute_table()
        asyncio.run(launcher.start_launcher())
    except Exception as E:
        LOGGER.error(f'Exception in the main execution block: {E}')


# main execution block
if __name__ == "__main__":
    main()


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
