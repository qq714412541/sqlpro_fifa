import sqlite3
import os, json
class sqlitedatabase:

    def __init__(self):
        self.conn = sqlite3.connect('database.sqlite')

    def execute_sql(sql_statement, parameters, commit=True):
        record = []
        try:
            conn=sqlite3.connect('database.sqlite')
            cursor = conn.cursor()
            cursor.execute(sql_statement, parameters)
            if commit:
                conn.commit()
            else:
                record = cursor.fetchall()
        except sqlite3.Error as err :
            raise err
        finally:
            # Close database connection.
            cursor.close()
            conn.close()
            return record
    def execute_select(sql_statement, parameters, commit=True):
        record = []
        try:
            conn=sqlite3.connect('database.sqlite')
            cursor = conn.cursor()
            cursor.execute(sql_statement, parameters)
            if commit:
                conn.commit()
                record = cursor.fetchall()

        except sqlite3.Error as err :
            raise err
        finally:
            # Close database connection.
            cursor.close()
            conn.close()
            return record