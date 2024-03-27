import pymysql
import sys
import logging
import warnings
warnings.filterwarnings("ignore", category=pymysql.Warning)
_logger = logging.getLogger("galEupy.dbconnect")


class BaseDatabase:
    def __init__(self, host, user, password, port=None):
        self.host = host
        self.user = user
        self.password = password
        self.port = 3306 if port is None else port


class DatabaseCreate(BaseDatabase):
    def __init__(self, host, user, password, port=None):
        BaseDatabase.__init__(self, host, user, password, port)
        try:
            self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port)
            self.cursor = self.connection.cursor()
        except pymysql.Error as e:
            _logger.error(f"Error in database connection.......: {e}")

            sys.exit(0)

    def db_existence(self, db_name):
        try:
            query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{db_name}'"
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            return cursor.fetchone()
        except pymysql.Error as e:
            _logger.error("Error {}".format(e))
            return None

    def create(self, db_name):
        try:
            query = "CREATE DATABASE {}".format(db_name)
            self.cursor.execute(query)
            self.connection.commit()
            _logger.debug(f"{db_name} create database: successful")
        except pymysql.Error as e:
            _logger.error(f"Failed to create database: {db_name} \n{e}")
            self.connection.rollback()
            return 1

    def drop_database(self, db_name):
        try:
            query = f"DROP DATABASE {db_name}"
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            _logger.debug(f"{db_name} deletion: successful")
        except pymysql.Error as e:
            _logger.error(f"Failed to delete  database: {db_name} \n{e}")
            self.connection.rollback()
            return None

    def rowcount(self, query):
        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            return cursor.rowcount

        except pymysql.Error:
            self.connection.rollback()

    def __del__(self):
        self.connection.close()


def check_db_connection(host, db_username, db_password, port=3306):
    _logger.debug("Checking db connection")
    db = pymysql.connect(host=host, user=db_username, password=db_password, port=port)
    cursor = db.cursor()

    try:
        cursor.execute("SELECT VERSION()")
        results = cursor.fetchone()
        if results:
            return True
        else:
            return False
    except pymysql.Error as e:
        _logger.error(f"ERROR {e.args[0]} IN CONNECTION: {e.args[1]}")


def create_db_dots_connection(db_config):
    # db_name = DbNames(db_config.db_prefix)
    db = Database(db_config.host, db_config.db_username, db_config.db_password, db_config.db_name, 0)
    return db


class Database(BaseDatabase):
    def __init__(self, host, user, password, db, infile, port=None):
        BaseDatabase.__init__(self, host, user, password, port)
        self.db = db
        self.infile = infile
        self.db_param = None
        if self.infile == 1:
            self.db_param = 1
        else:
            self.db_param = 0
        try:
            self.connection = pymysql.connect(host=self.host, user=self.user, passwd=self.password, database=self.db,
                                              local_infile=self.db_param, port=self.port)
            self.cursor = self.connection.cursor()
        except pymysql.Error as e:
            _logger.error("MySQL::Error in database connection. %s" % str(e))
            sys.exit(0)

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except pymysql.Error as e:
            _logger.error("Error {}".format(e))
            # _logger.debug("Query: {}".format(query))
            self.connection.rollback()

    def query(self, query):
        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            return cursor.fetchall()
        except pymysql.Error as e:
            _logger.error("Error {}".format(e))

    def query_one(self, query):
        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            return cursor.fetchone()
        except pymysql.Error as e:
            _logger.error("Error {}".format(e))

    def rowcount(self, query):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        return cursor.rowcount

    def __del__(self):
        self.connection.close()
