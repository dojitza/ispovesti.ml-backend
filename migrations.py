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


def insert_rows(conn, insert_rows_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(insert_rows_sql)
        conn.commit()
    except Error as e:
        print(e)


def main():
    database = DATABASE

    sql_create_pending_ispovest_table = """
    CREATE TABLE IF NOT EXISTS pendingIspovest(
        id integer PRIMARY KEY,
        content text NOT NULL
    );"""

    sql_create_arena_ispovest_table = """
    CREATE TABLE IF NOT EXISTS arenaIspovest(
        id integer PRIMARY KEY,
        content text NOT NULL,
        authorName text NOT NULL default "Anonimus"
    );"""

    sql_create_ispovest_table = """
    CREATE TABLE IF NOT EXISTS ispovest(
        id integer PRIMARY KEY,
        content text NOT NULL
    );"""

    sql_create_rejected_ispovest_table = """
    CREATE TABLE IF NOT EXISTS rejectedispovest(
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
        authorId integer NOT NULL,
        reaction integer NOT NULL,
        ispovestId integer NOT NULL,
        PRIMARY KEY(authorId,ispovestId),
        FOREIGN KEY(ispovestId) REFERENCES ispovest(id)
    );"""

    sql_create_komentar_reaction_table = """
    CREATE TABLE IF NOT EXISTS ispovestreaction(
        authorId integer PRIMARY KEY,
        reaction integer NOT NULL,
        komentarId integer NOT NULL,
        FOREIGN KEY(komentarId) REFERENCES komentar(id)
    );"""

    sql_create_arena_ispovest_reaction_table = """
    CREATE TABLE IF NOT EXISTS arenaispovestreaction(
        authorId integer NOT NULL,
        reaction integer NOT NULL,
        arenaIspovestId integer NOT NULL,
        PRIMARY KEY(authorId, arenaIspovestId),
        FOREIGN KEY(arenaIspovestId) REFERENCES arenaIspovest(id)
    );"""

    sql_create_user_info_table = """
    CREATE TABLE IF NOT EXISTS user(
        idhash PRIMARY KEY,
        lastGenerationTime integer NOT NULL DEFAULT 0,
        lastPublishTime integer NOT NULL DEFAULT 0
    );
    """
    sql_create_queue_length_table = """
    CREATE TABLE IF NOT EXISTS queueLength(
        queueLength integer NOT NULL CHECK (queueLength >= 0),
        enforcer INT DEFAULT 0 NOT NULL CHECK(enforcer == 0),
        UNIQUE (enforcer)
    );
    """
    sql_init_queue_length_table = """ 
    INSERT INTO queueLength(queueLength) VALUES(0);
    """

    sql_create_generated_ispovest_table = """
    CREATE TABLE IF NOT EXISTS generatedispovest(
        id integer PRIMARY KEY,
        content text NOT NULL,
        authorId integer
    )
    """

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
        create_table(conn, sql_create_user_info_table)
        create_table(conn, sql_create_pending_ispovest_table)
        create_table(conn, sql_create_rejected_ispovest_table)
        create_table(conn, sql_create_generated_ispovest_table)
        create_table(conn, sql_create_queue_length_table)
        insert_rows(conn, sql_init_queue_length_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
