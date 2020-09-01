import sqlite3
from sqlite3 import Error
from constants import DATABASE


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = DATABASE

    sql_create_projects_table = """ 
    CREATE TABLE IF NOT EXISTS ispovesti(
        id integer PRIMARY KEY,
        content text NOT NULL,
        likes integer NOT NULL DEFAULT 0,
        dislikes integer NOT NULL DEFAULT 0
    );"""

    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS komentari(
        id integer PRIMARY KEY,
        author text NOT NULL,
        content text NOT NULL,
        ispovestId integer NOT NULL,
        likes integer NOT NULL DEFAULT 0,
        dislikes integer NOT NULL DEFAULT 0,
        FOREIGN KEY(ispovestId) REFERENCES ispovesti(id)
    );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
