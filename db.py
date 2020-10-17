import sqlite3
import datetime
from flask import g
from flask import current_app as app

import constants


def dbKomentarToObject(komentarTuple):
    return {
        'author': komentarTuple[1],
        'text': komentarTuple[2],
        'likes': komentarTuple[4],
        'dislikes': komentarTuple[5]
    }


def dbIspovestToObject(ispovestTuple):
    return {
        'id': ispovestTuple[0],
        'text': ispovestTuple[1],
        'likes': ispovestTuple[2],
        'dislikes': ispovestTuple[3],
        'timesLiked': ispovestTuple[4],
        'timesDisliked': ispovestTuple[5],
    }


def dbArenaIspovestToObject(ispovestTuple):
    return {
        'id': ispovestTuple[0],
        'text': ispovestTuple[1],
        'likes': ispovestTuple[2],
        'dislikes': ispovestTuple[3],
        'timesLiked': ispovestTuple[4],
        'timesDisliked': ispovestTuple[5],
    }


def dbUserInfoToObject(userInfoTuple):
    return {
        'idHash': userInfoTuple[0],
        'lastGenerationTime': userInfoTuple[1],
    }


def get_db():
    conn = None
    try:
        conn = sqlite3.connect(constants.DATABASE)
    except Error as e:
        print(e)
    return conn


def get_flask_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(constants.DATABASE)
    return db


def getIspovesti(reactionAuthorId, page):
    sql = """ SELECT
                ispovest.id,
                ispovest.content,
                sum(case when reaction = 1 then 1 else 0 end) AS likes,
                sum(case when reaction = 0 then 1 else 0 end) AS dislikes,
                sum(case when (ispovestreaction.authorid = ? AND ispovestreaction.reaction = 1) then 1 else 0 end) AS timesLiked,
                sum(case when (ispovestreaction.authorid = ? AND ispovestreaction.reaction = 0) then 1 else 0 end) AS timesDisliked
            FROM ispovest
            LEFT JOIN ispovestreaction
            ON ispovest.id = ispovestreaction.ispovestId
            GROUP BY ispovest.id
            ORDER BY ispovest.id
            DESC
            LIMIT 10
            OFFSET ?*10"""

    ispovestiTuples = get_flask_db().cursor().execute(
        sql, (reactionAuthorId, reactionAuthorId, page)).fetchall()

    return [dbIspovestToObject(ispovestTuple) for ispovestTuple in ispovestiTuples]


def postUserCompletedArenaIntro(userIdHash):
    sql = """ UPDATE user
              SET arenaIntroCompleted = true,
              WHERE user.idHash=?;
          """
    cur = get_flask_db().cursor()
    cur.execute(sql, (userIdHash,))
    get_flask_db().commit()
    return cur.lastrowid


def postUserUsedSuperLike(userIdHash):
    sql = """ UPDATE user
              SET superlikesLeft -= 1,
              WHERE user.idHash=?;
          """
    cur = get_flask_db().cursor()
    cur.execute(sql, (userIdHash,))
    get_flask_db().commit()
    return getUserInfo(userIdHash)


def putIspovestReaction(uniqueIdentifierString, reaction, ispovestId):
    authorId = hash(uniqueIdentifierString)
    print(reaction, authorId, ispovestId, reaction)
    sql = """INSERT INTO ispovestreaction (authorId, reaction, ispovestId)
                VALUES(?, ?, ?)
                ON CONFLICT(authorId, ispovestId)
                DO UPDATE SET reaction=?;"""
    cur = get_flask_db().cursor()
    cur.execute(sql, (authorId, reaction, ispovestId, reaction))
    get_flask_db().commit()
    return cur.lastrowid + cur.rowcount


def postIspovestReaction(uniqueIdentifierString, reaction, ispovestId):
    authorId = hash(uniqueIdentifierString)
    sql = """ INSERT INTO ispovestreaction(reaction, authorId, ispovestId)
            VALUES(?, ?, ?) """
    cur = get_flask_db().cursor()
    cur.execute(sql, (reaction, authorId, ispovestId))
    get_flask_db().commit()
    return cur.lastrowid


def postArenaIspovestReaction(uniqueIdentifierString, reaction, arenaispovestId):
    authorId = hash(uniqueIdentifierString)
    sql = """ INSERT INTO arenaispovestreaction(reaction, authorId, arenaispovestId)
            VALUES(?, ?, ?) """
    cur = get_flask_db().cursor()
    cur.execute(sql, (reaction, authorId, arenaispovestId))
    get_flask_db().commit()
    return cur.lastrowid


def putArenaIspovestReaction(uniqueIdentifierString, reaction, arenaIspovestId):
    authorId = hash(uniqueIdentifierString)
    sql = """INSERT INTO arenaispovestreaction (authorId, reaction, arenaIspovestId)
                VALUES(?, ?, ?)
                ON CONFLICT(authorId, arenaIspovestId)
                DO UPDATE SET reaction=?;"""
    cur = get_flask_db().cursor()
    cur.execute(sql, (authorId, reaction, arenaIspovestId, reaction))
    get_flask_db().commit()
    print(cur.lastrowid + cur.rowcount)
    return cur.lastrowid + cur.rowcount


def getReactionToIspovest(uniqueIdentifierString, ispovestId):
    authorId = hash(uniqueIdentifierString)
    sql = """SELECT reaction FROM ispovestreaction WHERE authorId =? and ispovestId =?"""
    reaction = get_flask_db().cursor().execute(
        sql, (authorId, ispovestId)).fetchone()
    if (reaction):
        return reaction[0]
    else:
        return None


def getReactionToArenaIspovest(uniqueIdentifierString, ispovestId):
    authorId = hash(uniqueIdentifierString)
    sql = """SELECT reaction FROM arenaispovestreaction WHERE authorId =? and arenaispovestId =?"""
    reaction = get_flask_db().cursor().execute(
        sql, (authorId, ispovestId)).fetchone()
    if (reaction):
        return reaction[0]
    else:
        return None


def getIspovest(ispovestId):
    sql = """   SELECT
                    ispovest.id,
                    ispovest.content,
                    sum(case when reaction=1 then 1 else 0 end) AS likes,
                    sum(case when reaction=0 then 1 else 0 end) AS dislikes
                FROM ispovest
                JOIN ispovestreaction
                ON ispovest.id = ispovestreaction.ispovestId
                WHERE ispovest.id = ?
                GROUP BY ispovest.id """
    ispovest = get_flask_db().cursor().execute(sql, (ispovestId,)).fetchone()
    parsedIspovest = dbIspovestToObject(ispovest)
    parsedKomentari = getKomentari(ispovestId)
    parsedIspovest['comments'] = parsedKomentari
    return parsedIspovest


def getArenaIspovesti(reactionAuthorId, page):

    sql = """   SELECT
                    arenaispovest.id,
                    arenaispovest.content,
                    sum(case when reaction = 1 then 1 else 0 end) AS likes,
                    sum(case when reaction = 0 then 1 else 0 end) AS dislikes,
                    sum(case when (arenaispovestreaction.authorid = ? AND arenaispovestreaction.reaction = 1) then 1 else 0 end) AS timesLiked,
                    sum(case when (arenaispovestreaction.authorid = ? AND arenaispovestreaction.reaction = 0) then 1 else 0 end) AS timesDisliked
                FROM arenaispovest
                LEFT JOIN arenaIspovestReaction
                ON arenaispovest.id = arenaispovestreaction.arenaIspovestId
                GROUP BY arenaispovest.id
                ORDER BY arenaispovest.id
                DESC
                LIMIT 10
                OFFSET ?*10
				"""

    ispovestiTuples = get_flask_db().cursor().execute(
        sql, (reactionAuthorId, reactionAuthorId, page)).fetchall()
    return [dbArenaIspovestToObject(ispovestTuple) for ispovestTuple in ispovestiTuples]


def getUserInfo(userIdHash):
    sql = """   SELECT *
                FROM user
                WHERE user.idhash = ?
          """
    userInfo = get_flask_db().cursor().execute(sql, (userIdHash,)).fetchone()
    if userInfo is not None:
        return dbUserInfoToObject(userInfo)
    else:
        return None


def createUser(userIdHash):
    sql = """ INSERT INTO user(idHash)
              VALUES(?)
          """
    cur = get_flask_db().cursor()
    cur.execute(sql, (userIdHash,))
    get_flask_db().commit()
    return getUserInfo(userIdHash)


def getLastGenTimestamp(userIdHash):
    userInfo = getUserInfo(userIdHash)
    if userInfo is not None:
        return userInfo['lastGenerationTime']
    else:
        return 0


def markGenTimestamp(userIdHash):
    sql = """INSERT INTO user (idhash,lastGenerationTime)
            VALUES(?, strftime('%s','now'))
            ON CONFLICT(idhash)
            DO UPDATE SET lastGenerationTime=strftime('%s','now');"""
    cur = get_flask_db().cursor()
    cur.execute(sql, (userIdHash,))
    get_flask_db().commit()
    return cur.lastrowid + cur.rowcount
