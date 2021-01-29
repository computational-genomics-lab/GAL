import pymysql
import sys
import logging
import warnings
warnings.filterwarnings("ignore", category=pymysql.Warning)
_logger = logging.getLogger("galpy.dbconnect")


class DatabaseCreate:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        try:
            self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password)
            self.cursor = self.connection.cursor()
        except pymysql.Error:
            _logger.error("Error in database connection.......")
            sys.exit(0)

    def create(self, db_name):
        try:
            query = 'CREATE DATABASE  ' + db_name
            self.cursor.execute(query)
            self.connection.commit()
        except pymysql.Error:
            self.connection.rollback()
            return 1

    def rowcount(self, query):
        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            return cursor.rowcount

        except pymysql.Error:
            self.connection.rollback()


def check_db_connection(host, db_username, db_password):
    db = pymysql.connect(host=host, user=db_username, password=db_password)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT VERSION()")
        results = cursor.fetchone()
        if results:
            return True
        else:
            return False
    except pymysql.Error as e:
        _logger.error("ERROR %d IN CONNECTION: %s" % (e.args[0], e.args[1]))
    return False


def create_db_dots_connection(db_config):
    db_name = DbNames(db_config.db_prefix)
    db = Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 0)
    return db


class DbNames:
    def __init__(self, db_prefix):
        self.core = db_prefix + "_core"
        self.dots = db_prefix + "_dots"
        self.sres = db_prefix + "_sres"


class Database:
    def __init__(self, host, user, password, db, infile):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.infile = infile
        self.db_param = None

        if self.infile == 1:
            self.db_param = 1
        else:
            self.db_param = 0
        try:
            self.connection = pymysql.connect(host=self.host, user=self.user, passwd=self.password, database=self.db,
                                              local_infile=self.db_param)
            self.cursor = self.connection.cursor()
        except pymysql.Error as e:
            _logger.error("MySQL::Error in database connection. %s" % str(e))
            sys.exit(0)

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except pymysql.Error as e:
            _logger.error("Error Test {}".format(e))
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
