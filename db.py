import sqlite3
import datetime
from ispovest import ispovest
from flask import g
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
    }


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(constants.DATABASE)
    return db


def postIspovestReaction(uniqueIdentifierString, reaction, ispovestId):
    authorId = hash(uniqueIdentifierString)
    sql = """ INSERT INTO ispovestreaction(reaction, authorId, ispovestId)
            VALUES(?,?,?) """
    cur = get_db().cursor()
    cur.execute(sql, (reaction, authorId, ispovestId))
    get_db().commit()
    return cur.lastrowid


def postArenaIspovestReaction(uniqueIdentifierString, reaction, arenaispovestId):
    authorId = hash(uniqueIdentifierString)
    sql = """ INSERT INTO arenaispovestreaction(reaction, authorId, arenaispovestId)
            VALUES(?,?,?) """
    cur = get_db().cursor()
    cur.execute(sql, (reaction, authorId, arenaispovestId))
    get_db().commit()
    return cur.lastrowid


def getReactionToIspovest(uniqueIdentifierString, ispovestId):
    authorId = hash(uniqueIdentifierString)
    sql = """SELECT reaction FROM ispovestreaction WHERE authorId=? and ispovestId=?"""
    reaction = get_db().cursor().execute(sql, (authorId, ispovestId)).fetchone()
    if (reaction):
        return reaction[0]
    else:
        return None


def getReactionToArenaIspovest(uniqueIdentifierString, ispovestId):
    authorId = hash(uniqueIdentifierString)
    sql = """SELECT reaction FROM arenaispovestreaction WHERE authorId=? and arenaispovestId=?"""
    reaction = get_db().cursor().execute(sql, (authorId, ispovestId)).fetchone()
    if (reaction):
        return reaction[0]
    else:
        return None


def getIspovest(ispovestId):
    sql = """   SELECT
                    ispovest.id,
                    ispovest.content,
                    sum(case when reaction = 1 then 1 else 0 end) AS likes,
                    sum(case when reaction = 0 then 1 else 0 end) AS dislikes
                FROM ispovest
                JOIN ispovestreaction
                ON ispovest.id = ispovestreaction.ispovestId
                WHERE ispovest.id = ?
                GROUP BY ispovest.id """
    ispovest = get_db().cursor().execute(sql, (ispovestId,)).fetchone()
    parsedIspovest = dbIspovestToObject(ispovest)
    parsedKomentari = getKomentari(ispovestId)
    parsedIspovest['comments'] = parsedKomentari
    return parsedIspovest


def getArenaIspovesti(authorId):
    sql = """   SELECT
                    arenaispovest.id,
                    arenaispovest.content
                FROM arenaispovest
                LEFT JOIN arenaIspovestReaction
                ON arenaispovest.id = arenaispovestreaction.arenaIspovestId
                GROUP BY arenaispovest.id
				HAVING (sum(arenaIspovestReaction.authorid = ?) < 1)
                OR (sum(arenaIspovestReaction.authorid = ?) is NULL)"""
    ispovestiTuples = get_db().cursor().execute(
        sql, (authorId, authorId)).fetchall()
    return [dbArenaIspovestToObject(ispovestTuple) for ispovestTuple in ispovestiTuples]
