import mysql.connector
from tools import config


class Data_base:

    def __init__(self):
        sql_connection = config.sql_connection
        self.connection = mysql.connector.connect(host=sql_connection["host"],
                                                  database=sql_connection["database"],
                                                  user=sql_connection["user"],
                                                  password=sql_connection["password"])
        self.cursor = self.connection.cursor()
        self.SQL_insert_command = open('python/sql/insert.sql', 'r').read()

    def insert_record_into_db(self, record_tuple):
        self.cursor.execute(self.SQL_insert_command, record_tuple)

    def commit(self):
        self.connection.commit()

    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()


def insert_into_db(record_list):
    try:
        data_base = Data_base()
        for record in record_list:
            data_base.insert_record_into_db(record)
        data_base.commit()
    finally:
        data_base.close_connection()
        

database = Data_base()
