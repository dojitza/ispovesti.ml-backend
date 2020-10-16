import db
import constants
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


f = open('noveIspovesti.txt', 'r')
conn = create_connection(constants.DATABASE)
with conn:
    for line in f:
        strippedLine = line.strip()

        if strippedLine != '====================' and strippedLine != '':
            sql = '''INSERT INTO
                    pendingIspovest(content)
                    VALUES(?) '''
            cur = conn.cursor()
            cur.execute(sql, (strippedLine,))
            conn.commit()
