import os
import re
import sys

import MySQLdb


# Localhost
HOST = os.environ.get('MY_MYSQL_HOST', '127.0.0.1')
PORT = int(os.environ.get('MY_MYSQL_PORT', "3306"))
USER = os.environ.get('MY_MYSQL_USER')
PASSWORD = os.environ.get('MY_MYSQL_PASSWORD')

# re compile at first
re_eof = re.compile(r'\n')
re_space = re.compile(r'\s+')


def format_sql(sql):
    sql = re_eof.sub(' ', sql)
    sql = re_space.sub(' ', sql)
    if sys.flags.debug:
        print(sql)
    return sql


class BaseTable():
    def __enter__(self):
        try:
            self.connection = MySQLdb.connect(
                host=HOST, port=PORT, user=USER, passwd=PASSWORD, charset='utf8')
            self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        except MySQLdb.Error as e:
            print('Faild to connect MySQL Server.')
            raise e
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.cursor:
            self.cursor.close()
            self.connection.close()
        return

    def is_connect(self):
        return bool(self.cursor)

    def get_query(self, sql, args=None):
        if not self.cursor:
            return None
        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    def get_query_list(self, sql, size, args=None):
        if not self.cursor:
            return None
        self.cursor.execute(sql, args)
        return self.cursor.fetchmany(size)

    def set_query(self, sql, args=None):
        if not self.cursor:
            return False
        self.cursor.execute(sql, args)
        return True

    def commit_query(self):
        self.connection.commit()
        return


class DeviceTable(BaseTable):
    DATABASE_NAME = 'Device'
    TABLE_NAME = 'device'

    def select(self, deviceName):
        sql = f'''
            SELECT *
            FROM {self.DATABASE_NAME}.{self.TABLE_NAME}
            WHERE deviceName = '{deviceName}';
        '''
        sql = format_sql(sql)
        _dict = self.get_query(sql)
        return _dict

    def upsert(self, _dict):
        sql = f"""
            INSERT INTO {self.DATABASE_NAME}.{self.TABLE_NAME} (
                deviceName, projectSymbolFk, deviceIp, connectionStatus, os
            ) VALUES (
                '{_dict['deviceName']}', '{_dict['projectSymbolFk']}',
                '{_dict['deviceIp']}', '{_dict['connectionStatus']}', '{_dict['os']}'
            )
            ON DUPLICATE KEY UPDATE
                deviceName = '{_dict['deviceName']}',
                projectSymbolFk = '{_dict['projectSymbolFk']}',
                deviceIp = '{_dict['deviceIp']}',
                connectionStatus = '{_dict['connectionStatus']}',
                os = '{_dict['os']}';
        """
        sql = format_sql(sql)
        self.set_query(sql)
        self.commit_query()
        return

    def delete(self):
        sql = f"""
            DELETE FROM {self.DATABASE_NAME}.{self.TABLE_NAME}
        """
        sql = format_sql(sql)
        self.set_query(sql)
        self.commit_query()
        return


class PodTable(BaseTable):
    DATABASE_NAME = 'Pod'
    TABLE_NAME = 'pod'

    def upsert(self, _dict):
        # imageName
        imageName = _dict.get('imageName')
        if imageName is not None:
            imageName = f"'{imageName}'"
        else:
            imageName = 'NULL'
        # deployedAt
        if _dict['deployedAt']:
            deployedAt = f"'{_dict['deployedAt']}'"
        else:
            deployedAt = 'NULL'

        sql = f"""
            INSERT INTO {self.DATABASE_NAME}.{self.TABLE_NAME} (
                podName, deviceNameFk, imageName, currentVersion, latestVersion, deployedAt, status
            ) VALUES (
                '{_dict['podName']}', '{_dict['deviceNameFk']}', {imageName},
                '{_dict['currentVersion']}', '{_dict['latestVersion']}',
                {deployedAt}, '{_dict['status']}'
            )
            ON DUPLICATE KEY UPDATE
                podName = '{_dict['podName']}',
                deviceNameFk = '{_dict['deviceNameFk']}',
                imageName = {imageName},
                currentVersion = '{_dict['currentVersion']}',
                latestVersion = '{_dict['latestVersion']}',
                deployedAt = {deployedAt},
                status = '{_dict['status']}';
        """
        sql = format_sql(sql)
        self.set_query(sql)
        self.commit_query()
        return

    def delete(self):
        sql = f"""
            DELETE FROM {self.DATABASE_NAME}.{self.TABLE_NAME}
        """
        sql = format_sql(sql)
        self.set_query(sql)
        self.commit_query()
        return
