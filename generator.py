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
    except Error as e:
        print(e)

    return conn


def createIspovest(conn, ispovest):
    """
    Create a new ispovest into the ispovesti table
    :param conn:
    :param ispovest:
    :return: ispovest id
    """
    sql = ''' INSERT INTO ispovesti(content)
              VALUES(?) '''

    cur = conn.cursor()
    cur.execute(sql, ispovest)
    conn.commit()
    return cur.lastrowid


def createKomentar(conn, komentar):
    """
    Create a new komentar
    :param conn:
    :param komentar:
    :return: komentar id
    """

    sql = ''' INSERT INTO komentari(author,content,ispovestId)
              VALUES(?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, komentar)
    conn.commit()
    return cur.lastrowid


def main():
    database = DATABASE

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new ispovest
        ispovest = ('Verenik i ja smo se verili hehe',)
        ispovestId = createIspovest(conn, ispovest)

        # tasks
        komentar1 = ('Autorka', 'Mnogo dobro sestro!', ispovestId)
        komentar2 = ('Momčilo', 'Jadan li je...', ispovestId)

        # create tasks
        createKomentar(conn, komentar1)
        createKomentar(conn, komentar2)


if __name__ == '__main__':
    main()
