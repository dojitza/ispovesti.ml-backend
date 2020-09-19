
from flask import Flask, escape, request, jsonify, abort, Response, g

from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import os

import db
import constants
import helpers

app = Flask(__name__)
# CSRFProtect(app)
CORS(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


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
    ispovestiTuples = db.get_db().cursor().execute(
        sql, (authorId, authorId)).fetchall()
    return jsonify([db.dbIspovestToObject(ispovestTuple) for ispovestTuple in ispovestiTuples])


@app.route('/api/v1/ispovesti/<int:ispovestId>', methods=['GET'])
def getIspovest(ispovestId):
    ispovest = db.getIspovest(ispovestId)
    return jsonify(ispovest)


@app.route('/api/v1/arenaIspovesti', methods=['GET'])
def getArenaIspovesti():
    authorId = hash(str(request.user_agent) + str(request.remote_addr))
    arenaIspovesti = db.getArenaIspovesti(authorId)
    return jsonify(arenaIspovesti)


@app.route('/api/v1/ispovesti/<int:ispovestId>/postLike', methods=['POST'])
def likeIpovest(ispovestId):
    reaction = db.getReactionToIspovest(
        str(request.user_agent) + str(request.remote_addr), ispovestId)
    if (reaction):
        abort(403)
    else:
        reactionId = db.postIspovestReaction(
            str(request.user_agent) + str(request.remote_addr), constants.LIKE, ispovestId)
        return Response(jsonify(reactionId), status=201, mimetype='application/json')


@ app.route('/api/v1/ispovesti/<int:ispovestId>/postDislike', methods=['POST'])
def dislikeIpovest(ispovestId):
    reaction = db.getReactionToIspovest(
        str(request.user_agent) + str(request.remote_addr), ispovestId)
    if (reaction):
        abort(403)
    else:
        reactionId = db.postIspovestReaction(
            str(request.user_agent) + str(request.remote_addr), constants.DISLIKE, ispovestId)
        return Response(jsonify(reactionId), status=201, mimetype='application/json')


@ app.route('/api/v1/arenaIspovesti/<int:arenaIspovestId>/postReaction', methods=['POST'])
def postArenaIspovestReaction(arenaIspovestId):
    reactionString = request.json
    reactionConstant = helpers.mapReactionStringToConstant(reactionString)

    reaction = db.getReactionToArenaIspovest(
        str(request.user_agent) + str(request.remote_addr), arenaIspovestId)

    if (reaction):
        abort(403)
    else:
        reactionId = db.postArenaIspovestReaction(
            str(request.user_agent) + str(request.remote_addr), reactionConstant, arenaIspovestId)
        return Response(jsonify(reactionId), status=201, mimetype='application/json')


@app.route('/api/v1/user', methods=['GET'])
def getUserInfo():
    userIdHash = str(request.user_agent) + str(request.remote_addr)
    userInfo = db.getUserInfo(userIdHash)
    if (userInfo is None):
        userInfo = db.createUser(userIdHash)
    return jsonify(userInfo)


@ app.route('/')
def index():
    return jsonify('use /api/v1/ endpoint to access the rest service')


@ app.route('/addComment', methods=['POST'])
def addComment():

    print(request.form['ispovestId'])
    print(request.form['commentInput'])

    return index()


def getKomentari(ispovestId):
    sql = """ SELECT * FROM komentar
              WHERE ispovestId = ? """
    komentariTuples = db.get_db().cursor().execute(sql, (ispovestId,)).fetchall()
    return [db.dbKomentarToObject(komentarTuple) for komentarTuple in komentariTuples]


def likeKomentar(komentarId):
    return jsonify(request.remote_addr)


def dislikeKomentar(komentarId):
    pass


def postKomentar(ispovestId, komentar):
    pass
