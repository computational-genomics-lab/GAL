from __future__ import print_function
import os
import sys
from pathlib import Path, PurePosixPath
from galpy import data_schedule_utility
from galpy import logging_utility, command_argument, gal_function
import main


CurrDir = Path(__file__).parent.absolute()
arg = command_argument.ProcessArguments(CurrDir)

logger = logging_utility.logger_function(__name__, arg.log_file)
logger.info('GAL Upload started \n')

# configuration file existence check and configuration parser.
config = gal_function.ConfigFileHandler(arg.db_config_file, arg.path_config_file, arg.org_config_file, logger)

db_config = config.db_config
path_config = config.path_config
org_config = config.org_config

# check database connection, upload schema and common data upload
main.process_schema_common_data(db_config, arg, CurrDir)

if arg.new_upload:
    status_log = data_schedule_utility.StatusLog(db_config)
    status_log.submit_log(org_config.organism, org_config.version, arg.org_config_file)

main.main(arg, db_config, logger, CurrDir)





