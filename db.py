import sqlite3
import datetime
from flask import g
from flask import current_app as app
from time import time

import constants


def dbKomentarToObject(komentarTuple):
    return {
        'author': komentarTuple[1],
        'text': komentarTuple[2],
        'likes': komentarTuple[4],
        'dislikes': komentarTuple[5]
    }


def dbIspovestWithReactionsToObject(ispovestTuple):
    return {
        'id': ispovestTuple[0],
        'text': ispovestTuple[1],
        'likes': ispovestTuple[2],
        'dislikes': ispovestTuple[3],
        'timesLiked': ispovestTuple[4],
        'timesDisliked': ispovestTuple[5],
    }


def dbArenaIspovestWithReactionsToObject(ispovestTuple):
    return {
        'id': ispovestTuple[0],
        'text': ispovestTuple[1],
        'authorName': ispovestTuple[2],
        'likes': ispovestTuple[3],
        'dislikes': ispovestTuple[4],
        'timesLiked': ispovestTuple[5],
        'timesDisliked': ispovestTuple[6],
    }


def dbArenaIspovestToObject(ispovestTuple):
    return {
        'id': ispovestTuple[0],
        'text': ispovestTuple[1],
        'authorName': ispovestTuple[2]
    }


def dbArenaIspovestToObject(ispovestTuple):
    return {
        'id': ispovestTuple[0],
        'text': ispovestTuple[1],
        'authorName': ispovestTuple[2]
    }


def dbUserInfoToObject(userInfoTuple):
    return {
        'idHash': userInfoTuple[0],
        'lastGenerationTime': userInfoTuple[1],
        'lastPublishTime': userInfoTuple[2],
    }


def dbGeneratedIspovestToObject(generatedIspovestTuple):
    return {
        'id': generatedIspovestTuple[0],
        'text': generatedIspovestTuple[1],
        'authorIdHash': generatedIspovestTuple[2]
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

    return [dbIspovestWithReactionsToObject(ispovestTuple) for ispovestTuple in ispovestiTuples]


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
    authorIdHash = hash(uniqueIdentifierString)
    sql = """INSERT INTO ispovestreaction (authorId, reaction, ispovestId)
                VALUES(?, ?, ?)
                ON CONFLICT(authorId, ispovestId)
                DO UPDATE SET reaction=?;"""
    cur = get_flask_db().cursor()
    cur.execute(sql, (authorIdHash, reaction, ispovestId, reaction))
    get_flask_db().commit()
    return cur.lastrowid + cur.rowcount


def postIspovestReaction(uniqueIdentifierString, reaction, ispovestId):
    authorIdHash = hash(uniqueIdentifierString)
    sql = """ INSERT INTO ispovestreaction(reaction, authorId, ispovestId)
            VALUES(?, ?, ?) """
    cur = get_flask_db().cursor()
    cur.execute(sql, (reaction, authorIdHash, ispovestId))
    get_flask_db().commit()
    return cur.lastrowid


def postArenaIspovestReaction(uniqueIdentifierString, reaction, arenaispovestId):
    authorIdHash = hash(uniqueIdentifierString)
    sql = """ INSERT INTO arenaispovestreaction(reaction, authorId, arenaispovestId)
            VALUES(?, ?, ?) """
    cur = get_flask_db().cursor()
    cur.execute(sql, (reaction, authorIdHash, arenaispovestId))
    get_flask_db().commit()
    return cur.lastrowid


def putArenaIspovestReaction(uniqueIdentifierString, reaction, arenaIspovestId):
    authorIdHash = hash(uniqueIdentifierString)
    sql = """INSERT INTO arenaispovestreaction (authorId, reaction, arenaIspovestId)
                VALUES(?, ?, ?)
                ON CONFLICT(authorId, arenaIspovestId)
                DO UPDATE SET reaction=?;"""
    cur = get_flask_db().cursor()
    cur.execute(sql, (authorIdHash, reaction, arenaIspovestId, reaction))
    get_flask_db().commit()
    print(cur.lastrowid + cur.rowcount)
    return cur.lastrowid + cur.rowcount


def getReactionToIspovest(uniqueIdentifierString, ispovestId):
    authorIdHash = hash(uniqueIdentifierString)
    sql = """SELECT reaction FROM ispovestreaction WHERE authorId =? and ispovestId =?"""
    reaction = get_flask_db().cursor().execute(
        sql, (authorIdHash, ispovestId)).fetchone()
    if (reaction):
        return reaction[0]
    else:
        return None


def getReactionToArenaIspovest(uniqueIdentifierString, ispovestId):
    authorIdHash = hash(uniqueIdentifierString)
    sql = """SELECT reaction FROM arenaispovestreaction WHERE authorId =? and arenaispovestId =?"""
    reaction = get_flask_db().cursor().execute(
        sql, (authorIdHash, ispovestId)).fetchone()
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
    parsedIspovest = dbIspovestWithReactionsToObject(ispovest)
    parsedKomentari = getKomentari(ispovestId)
    parsedIspovest['comments'] = parsedKomentari
    return parsedIspovest


def getArenaIspovesti(reactionAuthorId, page):

    sql = """   SELECT
                    arenaispovest.id,
                    arenaispovest.content,
                    arenaispovest.authorName,
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
    return [dbArenaIspovestWithReactionsToObject(ispovestTuple) for ispovestTuple in ispovestiTuples]


def getUserInfo(userIdHash):
    sql = """   SELECT idhash, lastgenerationtime, lastpublishtime
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


def addGeneratedIspovest(ispovestText, authorIdHash):
    sql = """INSERT INTO generatedispovest (content, authorId)
             VALUES(?,?)"""
    cur = get_flask_db().cursor()
    cur.execute(sql, (ispovestText, authorIdHash))
    get_flask_db().commit()
    lastRowId = cur.lastrowid
    sql = """SELECT *
             FROM generatedispovest
             WHERE id=?;
          """
    ispovestTuple = get_flask_db().cursor().execute(sql, (lastRowId,)).fetchone()
    return dbGeneratedIspovestToObject(ispovestTuple)


def getLastPubTimestamp(userIdHash):
    userInfo = getUserInfo(userIdHash)
    if userInfo is not None:
        if userInfo['lastPublishTime'] is not None:
            return userInfo['lastPublishTime']
        else:
            return 0
    else:
        return 0


def markPubTimestamp(userIdHash):
    sql = """INSERT INTO user (idhash,lastPublishTime)
            VALUES(?, strftime('%s','now'))
            ON CONFLICT(idhash)
            DO UPDATE SET lastPublishTime=strftime('%s','now');"""
    cur = get_flask_db().cursor()
    cur.execute(sql, (userIdHash,))
    get_flask_db().commit()
    return cur.lastrowid + cur.rowcount


'''
checks if authorIdHash generated the ispovestId provided
If true, checks if the author already published an ispovest in the last 12 hours,
if he has, returns None, othervise it publishes the generated
ispovest as arenaispovest In the case the author did not generate that ispovest,
returns None
'''


def publishGeneratedIspovest(ispovestId, authorName, authorIdHash):
    sql = """SELECT *
             FROM generatedispovest
             WHERE id=?;
          """
    generatedIspovestiTuple = get_flask_db().cursor().execute(
        sql, (ispovestId,)).fetchone()
    generatedIspovest = dbGeneratedIspovestToObject(generatedIspovestiTuple)
    if generatedIspovest['authorIdHash'] != authorIdHash:
        print('nije generirao')
        return False

    if int(time()) - getLastPubTimestamp(authorIdHash) < constants.SUBMISSION_THROTTLE_THRESHOLD:
        print('prerano, proslo je tek' +
              str(int(time()) - getLastPubTimestamp(authorIdHash)))
        return False

    sql = """INSERT INTO arenaispovest (content,authorName)
            VALUES(?, ?)"""
    cur = get_flask_db().cursor()
    cur.execute(sql, (generatedIspovest['text'], authorName))
    get_flask_db().commit()
    markPubTimestamp(authorIdHash)
    return True


def getGenerationQueueLength():
    sql = """SELECT queueLength
            FROM queueLength
        """
    queueLength = get_flask_db().cursor().execute(sql).fetchone()
    return queueLength


def increseGenerationQueueLength():
    try:
        sql = """UPDATE queueLength SET queueLength=queueLength+1"""
        cur = get_flask_db().cursor()
        cur.execute(sql)
        get_flask_db().commit()
        print('increasing')
        return cur.lastrowid + cur.rowcount
    except sqlite3.IntegrityError:
        print('Queue length below zero check failed')


def decreaseGenerationQueueLength():
    try:
        sql = """UPDATE queueLength SET queueLength=queueLength-1"""
        cur = get_flask_db().cursor()
        cur.execute(sql)
        get_flask_db().commit()
        print('decreasing')
        return cur.lastrowid + cur.rowcount
    except sqlite3.IntegrityError:
        print('Queue length below zero check failed')
