########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# types
from typing import Optional
from web3.types import HexBytes

# globals
from dir_software.sft_glob import *
from dir_database.db_main import *
from __system__.dir_logger.lg_main import LOGGER


########################################################################################################################
# GLOBAL # GLOBAL # GLOBAL # GLOBAL # GLOBAL # GLOBAL # GLOBAL # GLOBAL # GLOBAL # GLOBAL # GLOBAL # GLOBAL # GLOBAL # G
########################################################################################################################

# table name
TABLENAME = 'runs_o'


########################################################################################################################
# EXECUTE TABLE # EXECUTE TABLE # EXECUTE TABLE # EXECUTE TABLE # EXECUTE TABLE # EXECUTE TABLE # EXECUTE TABLE # EXECUT
########################################################################################################################

# function: executing database with table
def execute_table() -> None:
    if DATABASE:
        LOGGER.debug(f'Database: table "{TABLENAME}" has connected!')
    headers = f'(' \
              f'{KEY_R_TIMESTAMP} TEXT PRIMARY KEY,' \
              f'{KEY_R_ACCOUNT_DICT} TEXT,' \
              f'{KEY_R_COMMANDS_LIST} TEXT' \
              f')'
    DATABASE.execute(f'CREATE TABLE IF NOT EXISTS {TABLENAME} {headers}')
    DATABASE.commit()


########################################################################################################################
# CLEAR DATABASE # CLEAR DATABASE # CLEAR DATABASE # CLEAR DATABASE # CLEAR DATABASE # CLEAR DATABASE # CLEAR DATABASE #
########################################################################################################################

# function: clearing database
def clear_database() -> None:
    DATABASE.execute(f'DROP TABLE IF EXISTS {TABLENAME}')
    execute_table()
    DATABASE.commit()


########################################################################################################################
# ADD RUN # ADD RUN # ADD RUN # ADD RUN # ADD RUN # ADD RUN # ADD RUN # ADD RUN # ADD RUN # ADD RUN # ADD RUN # ADD RUN
########################################################################################################################

# function: adding run
def add_run(run_dict: dict) -> None:
    val_01 = str(run_dict[KEY_R_TIMESTAMP])
    val_02 = str(run_dict[KEY_R_ACCOUNT_DICT])
    val_03 = str(run_dict[KEY_R_COMMANDS_LIST])
    CUR.execute('INSERT INTO ' + TABLENAME + ' VALUES (?, ?, ?)', (val_01, val_02, val_03))
    DATABASE.commit()


########################################################################################################################
# DELETE RUN # DELETE RUN # DELETE RUN # DELETE RUN # DELETE RUN # DELETE RUN # DELETE RUN # DELETE RUN # DELETE RUN # D
########################################################################################################################

# function: deleting run
def delete_run(run_timestamp: str) -> None:
    CUR.execute(f'DELETE FROM {TABLENAME} WHERE {KEY_R_TIMESTAMP} = ?', (run_timestamp,))
    DATABASE.commit()


########################################################################################################################
# GET RUN TIMESTAMPS LIST # GET RUN TIMESTAMPS LIST # GET RUN TIMESTAMPS LIST # GET RUN TIMESTAMPS LIST # GET RUN TIMEST
########################################################################################################################

# function: getting all run_timestamps as a list
def get_run_timestamps_list() -> list:
    CUR.execute(f'SELECT {KEY_R_TIMESTAMP} FROM {TABLENAME}')
    rows = CUR.fetchall()
    timestamps_list = [row[0] for row in rows]
    return timestamps_list


########################################################################################################################
# GET RUN DICT # GET RUN DICT # GET RUN DICT # GET RUN DICT # GET RUN DICT # GET RUN DICT # GET RUN DICT # GET RUN DICT
########################################################################################################################

# function: getting run_dict by its timestamp
def get_run_dict(timestamp: str) -> dict:
    runs_list = get_runs_list()
    run_dict = {}

    for t_run_dict in runs_list:
        if t_run_dict[KEY_R_TIMESTAMP] == timestamp:
            run_dict = t_run_dict
    return run_dict


########################################################################################################################
# GET RUNS LIST # GET RUNS LIST # GET RUNS LIST # GET RUNS LIST # GET RUNS LIST # GET RUNS LIST # GET RUNS LIST # GET RU
########################################################################################################################

# function: getting runs as a list
def get_runs_list() -> list:
    CUR.execute(f'SELECT * FROM {TABLENAME}')
    rows = CUR.fetchall()
    runs_list = []

    for row in rows:
        run_dict = {
            KEY_R_TIMESTAMP: row[0],
            KEY_R_ACCOUNT_DICT: eval(row[1]),
            KEY_R_COMMANDS_LIST: eval(row[2]),
        }
        runs_list.append(run_dict)
    return runs_list


########################################################################################################################
# SAVE RUN DICT # SAVE RUN DICT # SAVE RUN DICT # SAVE RUN DICT # SAVE RUN DICT # SAVE RUN DICT # SAVE RUN DICT # SAVE R
########################################################################################################################

# function: saving run_dict to database
def save_run_dict(run_dict: dict) -> (int, Optional[Exception]):
    try:
        run_timestamp = run_dict[KEY_R_TIMESTAMP]
        run_account_dict = run_dict[KEY_R_ACCOUNT_DICT]
        run_commands_list = run_dict[KEY_R_COMMANDS_LIST]

        CUR.execute(
            f'SELECT COUNT(*) FROM {TABLENAME} WHERE {KEY_R_TIMESTAMP} = ?', (run_timestamp,)
        )
        count = CUR.fetchone()[0]

        if count > 0:
            CUR.execute(
                f'UPDATE {TABLENAME} SET {KEY_R_ACCOUNT_DICT} = ? WHERE {KEY_R_TIMESTAMP} = ?',
                (str(run_account_dict), run_timestamp)
            )
            CUR.execute(
                f'UPDATE {TABLENAME} SET {KEY_R_COMMANDS_LIST} = ? WHERE {KEY_R_TIMESTAMP} = ?',
                (str(run_commands_list), run_timestamp)
            )
            DATABASE.commit()
            return 0, None
        else:
            return -1, Exception('No such a run_dict in database!')
    except Exception as E:
        return -1, E


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
