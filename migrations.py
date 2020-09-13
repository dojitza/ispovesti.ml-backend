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

    sql_create_arena_ispovest_table = """ 
    CREATE TABLE IF NOT EXISTS arenaIspovest(
        id integer PRIMARY KEY,
        content text NOT NULL
    );"""

    sql_create_ispovest_table = """ 
    CREATE TABLE IF NOT EXISTS ispovest(
        id integer PRIMARY KEY,
        content text NOT NULL
    );"""

    sql_create_komentar_table = """
    CREATE TABLE IF NOT EXISTS komentar(
        id integer PRIMARY KEY,
        author text NOT NULL,
        content text NOT NULL,
        ispovestId integer NOT NULL,
        FOREIGN KEY(ispovestId) REFERENCES ispovest(id)
    );"""

    sql_create_ispovest_reaction_table = """
    CREATE TABLE IF NOT EXISTS ispovestreaction(
        id integer PRIMARY KEY,
        authorId integer NOT NULL,
        reaction integer NOT NULL,
        ispovestId integer NOT NULL,
        FOREIGN KEY(ispovestId) REFERENCES ispovest(id)
    );"""

    sql_create_komentar_reaction_table = """
    CREATE TABLE IF NOT EXISTS ispovestreaction(
        id integer PRIMARY KEY,
        authorId integer NOT NULL,
        reaction integer NOT NULL,
        komentarId integer NOT NULL,
        FOREIGN KEY(komentarId) REFERENCES komentar(id)
    );"""

    sql_create_arena_ispovest_reaction_table = """
    CREATE TABLE IF NOT EXISTS arenaispovestreaction(
        id integer PRIMARY KEY,
        authorId integer NOT NULL,
        reaction integer NOT NULL,
        arenaIspovestId integer NOT NULL,
        FOREIGN KEY(arenaIspovestId) REFERENCES arenaIspovest(id)
    );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_ispovest_table)
        create_table(conn, sql_create_komentar_table)
        create_table(conn, sql_create_ispovest_reaction_table)
        create_table(conn, sql_create_komentar_reaction_table)
        create_table(conn, sql_create_arena_ispovest_table)
        create_table(conn, sql_create_arena_ispovest_reaction_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
