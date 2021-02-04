import pymysql
import sys


class DatabaseCreate:
    def __init__(self, host, user, password, port=None):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        try:
            if port is None:
                self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password)
            else:
                self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port)
            self.cursor = self.connection.cursor()
        except pymysql.Error as e:
            print("Error in database connection.......: {}".format(e))
            sys.exit(0)


if __name__ == '__main__':
    print("hi")
    # host = "127.0.0.1"
    # host = "172.17.0.1"
    host = "localhost"
    # host = "127.17.0.2"
    # port = 3306
    port = 8083
    db_1 = DatabaseCreate(host, 'root', 'test', port=port)
