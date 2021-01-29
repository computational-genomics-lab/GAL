import logging
from .configutility import ConfigFileHandler
from .dbconnect import check_db_connection
from .dbschema import database_schema
_logger = logging.getLogger("galpy.app")


class App(ConfigFileHandler):
    def __init__(self, db_config_file, path_config_file, org_config_file):
        ConfigFileHandler.__init__(self, db_config_file, path_config_file, org_config_file)

    @property
    def check_db_status(self):
        db_status = check_db_connection(self.db_config.host, self.db_config.db_username, self.db_config.db_password)
        print(db_status)
        return db_status

    def upload_schema(self):
        if self.check_db_status:
            database_schema(self.db_config)
