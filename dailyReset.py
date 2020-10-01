import db
import constants
import sqlite3
from sqlite3 import Error
import itertools

# TODO: implement these as transactions / or procedures in sqlite


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

# set all user's superlikes to 1


def resetSuperlikes():
    conn = create_connection(constants.DATABASE)
    with conn:
        sql = """
            UPDATE user
            SET superlikesLeft = 1
        """
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

# pick the best ispovesti from arena and insert them to the main list
# relegate the rest to the discarded ispovesti table


def processArena():
    conn = create_connection(constants.DATABASE)
    with conn:

        sql = """
                SELECT
                ai.*,
                sum(case when air.reaction = 0 then 1 else 0 end) AS dislikes,
                sum(case when air.reaction = 1 then 1 else 0 end) AS likes,
                sum(case when air.reaction = 2 then 1 else 0 end) AS superlikes
                FROM arenaIspovest ai
                LEFT JOIN arenaIspovestReaction air on ai.id = air.arenaIspovestId
                GROUP BY ai.id
                """

        ispovesti = conn.cursor().execute(sql).fetchall()
        if len(ispovesti) == 0:
            return
        topIspovesti = []
        processedArenaIspovesti = []
        for i in ispovesti:
            ispovestId = i[0]
            tekst = i[1]
            dislikes = i[2]
            likes = i[3]
            superlikes = i[4]
            weight = likes-dislikes+superlikes*3

            processedArenaIspovesti.append((ispovestId, tekst, weight))

        topIspovesti = [max(processedArenaIspovesti, key=lambda pai: pai[2])]
        for i in topIspovesti:
            processedArenaIspovesti.remove(i)

        # TODO: optimise these queryes when there are multiple ispovesti instead of single commiting
        for i in topIspovesti:
            content = i[1]
            sql = '''   INSERT INTO
                        ispovest(content)
                        VALUES(?) '''
            cur = conn.cursor()
            cur.execute(sql, (content,))
            conn.commit()

        for i in processedArenaIspovesti:
            content = i[1]
            sql = '''   INSERT INTO
                        rejectedIspovest(content)
                        VALUES(?) '''
            cur = conn.cursor()
            cur.execute(sql, (content,))
            conn.commit()

        for i in (itertools.chain(topIspovesti, processedArenaIspovesti)):
            ispovestId = i[0]
            sql = ''' DELETE
                      FROM arenaispovest
                        WHERE id=?;'''
            cur = conn.cursor()
            cur.execute(sql, (ispovestId,))
            conn.commit()

        sql = ''' DELETE 
            FROM arenaispovestreaction
            '''
        cur = conn.cursor()
        cur.execute(sql, )
        conn.commit()


# send the next batch to the arena
def fillArena():
    conn = create_connection(constants.DATABASE)
    with conn:
        sql = '''
                SELECT id, content
                FROM pendingispovest
                ORDER BY id
                LIMIT 10
        '''
        ispovesti = conn.cursor().execute(sql).fetchall()

        for i in ispovesti:
            ispovestId = i[0]
            sql = '''
                    DELETE
                    FROM pendingispovest
                    WHERE id =?'''
            cur = conn.cursor()
            cur.execute(sql, (ispovestId,))
            conn.commit()

        for i in ispovesti:
            content = i[1]
            sql = '''   INSERT INTO
                        arenaIspovest(content)
                        VALUES(?) '''
            cur = conn.cursor()
            cur.execute(sql, (content,))
            conn.commit()


resetSuperlikes()
processArena()
fillArena()
