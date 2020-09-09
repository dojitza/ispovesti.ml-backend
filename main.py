from flask import Flask, escape, request, jsonify, abort, Response
from flask import render_template
import datetime
import sqlite3
from flask import g
from ispovest import ispovest
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import os

CONSTANTS_DATABASE = 'database.db'
CONSTANTS_LIKE = 1
CONSTANTS_DISLIKE = 0


app = Flask(__name__)
# CSRFProtect(app)
CORS(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


def parseKomentarTupleToDict(komentarTuple):
    return {
        'author': komentarTuple[1],
        'text': komentarTuple[2],
        'likes': komentarTuple[4],
        'dislikes': komentarTuple[5]
    }


def parseIspovestTupleToDict(ispovestTuple):
    return {
        'id': ispovestTuple[0],
        'text': ispovestTuple[1],
        'likes': ispovestTuple[2],
        'dislikes': ispovestTuple[3],
        'timesLiked': ispovestTuple[4],
        'timesDisliked': ispovestTuple[5],

    }


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(CONSTANTS_DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


'''
returns true if uniqueidentifier string's hash has an entry in the table
with the provided ispovestId. This means a user has previously liked
'''


def postIspovestReaction(uniqueIdentifierString, reaction, ispovestId):
    authorId = hash(uniqueIdentifierString)
    sql = """ INSERT INTO ispovestreaction(reaction, authorId, ispovestId)
            VALUES(?,?,?) """
    cur = get_db().cursor()
    cur.execute(sql, (reaction, authorId, ispovestId))
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


def getKomentari(ispovestId):
    sql = """ SELECT * FROM komentar
              WHERE ispovestId = ? """
    komentariTuples = get_db().cursor().execute(sql, (ispovestId,)).fetchall()
    return [parseKomentarTupleToDict(komentarTuple) for komentarTuple in komentariTuples]


@app.route('/api/v1/ispovesti', methods=['GET'])
def getIspovesti():
    authorId = hash(str(request.user_agent) + str(request.remote_addr))
    sql = """ SELECT
                    ispovest.id,
                    ispovest.content,
                    sum(case when reaction = 1 then 1 else 0 end) AS likes,
                    sum(case when reaction = 0 then 1 else 0 end) AS dislikes,
                    sum(case when (ispovestreaction.authorid = ? AND ispovestreaction.reaction = 1) then 1 else 0 end) AS timesLiked,
                    sum(case when (ispovestreaction.authorid = ? AND ispovestreaction.reaction = 0) then 1 else 0 end) AS timesDisliked
                FROM ispovest
                JOIN ispovestreaction
                ON ispovest.id = ispovestreaction.ispovestId
                GROUP BY ispovest.id"""
    ispovestiTuples = get_db().cursor().execute(
        sql, (authorId, authorId)).fetchall()
    return jsonify([parseIspovestTupleToDict(ispovestTuple) for ispovestTuple in ispovestiTuples])


@app.route('/api/v1/ispovesti/<int:ispovestId>', methods=['GET'])
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
    parsedIspovest = parseIspovestTupleToDict(ispovest)
    parsedKomentari = getKomentari(ispovestId)
    parsedIspovest['comments'] = parsedKomentari
    return jsonify(parsedIspovest)


def postKomentar(ispovestId, komentar):
    print(request.user_agent, request.remote_addr)
    return jsonify(request.remote_addr)


@app.route('/api/v1/ispovesti/<int:ispovestId>/postLike', methods=['POST'])
def likeIpovest(ispovestId):
    reaction = getReactionToIspovest(
        str(request.user_agent) + str(request.remote_addr), ispovestId)
    if (reaction):
        abort(403)
    else:
        reactionId = postIspovestReaction(
            str(request.user_agent) + str(request.remote_addr), CONSTANTS_LIKE, ispovestId)
        return Response(jsonify(reactionId), status=201, mimetype='application/json')


@ app.route('/api/v1/ispovesti/<int:ispovestId>/postDislike', methods=['POST'])
def dislikeIpovest(ispovestId):
    reaction = getReactionToIspovest(
        str(request.user_agent) + str(request.remote_addr), ispovestId)
    if (reaction):
        abort(403)
    else:
        reactionId = postIspovestReaction(
            str(request.user_agent) + str(request.remote_addr), CONSTANTS_DISLIKE, ispovestId)
        return Response(jsonify(reactionId), status=201, mimetype='application/json')


def likeKomentar(komentarId):
    return jsonify(request.remote_addr)


def dislikeKomentar(komentarId):
    pass


@ app.route('/')
def index():

    return 'use /api/v1/ endpoint to access the rest service'

    likeReactionTextArray = ['Too miško', 'Bravo ase', 'Svaka ti dala']
    dislikeReactionTextArray = [
        'Loše brate', 'Šta sve neču da pročitam', 'Treba da te streljamo']

    ispovesti = [parseIspovestTupleToDict(
        i) for i in getIspovesti(page=0)]

    arenaIspovesti = ispovesti

    # return str(ispovestiDicts)

    return render_template('index.html',
                           ispovesti=ispovesti,
                           likes=likeReactionTextArray,
                           dislikes=dislikeReactionTextArray,
                           arenaIspovesti=arenaIspovesti)


@ app.route('/addComment', methods=['POST'])
def addComment():

    print(request.form['ispovestId'])
    print(request.form['commentInput'])

    return index()
