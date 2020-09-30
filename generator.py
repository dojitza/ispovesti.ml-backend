import sqlite3
from sqlite3 import Error
from constants import DATABASE
import db


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


def createArenaIspovest(conn, arenaIspovest):
    sql = ''' INSERT INTO arenaIspovest(content)
              VALUES(?) '''

    cur = conn.cursor()
    cur.execute(sql, arenaIspovest)
    conn.commit()
    return cur.lastrowid


def createIspovest(conn, ispovest):
    """
    Create a new ispovest into the ispovest table
    :param conn:
    :param ispovest:
    :return: ispovest id
    """
    sql = ''' INSERT INTO ispovest(content)
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

    sql = ''' INSERT INTO komentar(author,content,ispovestId)
              VALUES(?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, komentar)
    conn.commit()
    return cur.lastrowid


def createIspovestReaction(conn, reaction):
    """
    Create a new reaction
    :param conn:
    :param komentar:
    :return: komentar id
    """

    sql = ''' INSERT INTO ispovestreaction(reaction,authorId,ispovestId)
              VALUES(?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, reaction)
    conn.commit()
    return cur.lastrowid


def createKomentarReaction(conn, reaction):
    """
    Create a new reaction
    :param conn:
    :param komentar:
    :return: komentar id
    """

    sql = ''' INSERT INTO komentarreaction(reaction,authorId,komentarId)
              VALUES(?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, reaction)
    conn.commit()
    return cur.lastrowid


def createPendingIspovest(conn, ispovestText):
    sql = ''' INSERT INTO pendingispovest(content)
            VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (ispovestText,))
    conn.commit()
    return cur.lastrowid


def main():
    database = DATABASE

    # create a database connection
    conn = create_connection(database)
    with conn:

        '''
        ispovest = ('Verenik i ja smo se verili hehe 5',)
        ispovestId = createIspovest(conn, ispovest)

        komentar1 = ('Autorka', 'Mnogo dobro sestro!', ispovestId)
        komentar2 = ('Momčilo', 'Jadan li je...', ispovestId)

        createKomentar(conn, komentar1)
        createKomentar(conn, komentar2)

        reaction1 = (0, 121, ispovestId)
        reaction2 = (0, 122, ispovestId)

        createIspovestReaction(conn, reaction1)
        createIspovestReaction(conn, reaction2)

        arenaIspovest = ('Bleko haram gereeeeeeeee 1',)
        createArenaIspovest(conn, arenaIspovest)

        for i in range(50):
            ispovest = ('Verenik je verio mene i jos '+str(i) +
                        ' devojki, nisam mogla da verujem!',)
            ispovestId = createIspovest(conn, ispovest)

        '''

        f = open('stareIspovesti.txt', 'r')

        for line in f:
            if line != '====================\n':
                createIspovest(conn, (line.strip(),))


if __name__ == '__main__':
    main()
