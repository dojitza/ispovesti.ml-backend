
from flask import Flask, escape, request, jsonify, abort, Response, g
from flask_cors import CORS
import os
from time import time

import db
import constants
import helpers
from ispovestGeneratorClient import generateIspovestAlt as clientGenerateIspovest

app = Flask(__name__)
CORS(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/api/v1/generateIspovest', methods=['GET'])
def generateIspovest():
    prefix = request.args['prefix']
    authorId = hash(str(request.remote_addr))

    lastGenTimestamp = db.getLastGenTimestamp(authorId)
    timeDifference = int(time()) - lastGenTimestamp
    if timeDifference > constants.GENERATION_THROTTLE_THRESHOLD:
        db.markGenTimestamp(authorId)
        return jsonify(clientGenerateIspovest(prefix))
    else:
        return jsonify("You need to wait " + str(30 - timeDifference) + " more seconds before attempting another generation")


@app.route('/api/v1/ispovesti', methods=['GET'])
def getIspovesti():
    page = request.args['page']
    authorId = hash(str(request.user_agent) + str(request.remote_addr))
    ispovesti = db.getIspovesti(authorId, page)
    return jsonify(ispovesti)


@app.route('/api/v1/ispovesti/<int:ispovestId>', methods=['GET'])
def getIspovest(ispovestId):
    ispovest = db.getIspovest(ispovestId)
    return jsonify(ispovest)


@app.route('/api/v1/arenaIspovesti', methods=['GET'])
def getArenaIspovesti():
    page = request.args['page']
    authorId = hash(str(request.user_agent) + str(request.remote_addr))
    arenaIspovesti = db.getArenaIspovesti(authorId, page)
    return jsonify(arenaIspovesti)


@app.route('/api/v1/ispovesti/<int:ispovestId>/putReaction', methods=['PUT'])
def putIspovestReaction(ispovestId):
    reactionString = request.json
    reactionConstant = helpers.mapReactionStringToConstant(reactionString)
    success = db.putIspovestReaction(
        str(request.user_agent) + str(request.remote_addr), reactionConstant, ispovestId)
    if success:
        return Response(status=200, mimetype='application/json')
    else:
        abort(403)


@app.route('/api/v1/arenaIspovesti/<int:arenaIspovestId>/putReaction', methods=['PUT'])
def putArenaIspovestReaction(arenaIspovestId):
    reactionString = request.json
    reactionConstant = helpers.mapReactionStringToConstant(reactionString)
    success = db.putArenaIspovestReaction(
        str(request.user_agent) + str(request.remote_addr), reactionConstant, arenaIspovestId)
    if success:
        return Response(status=200, mimetype='application/json')
    else:
        abort(403)


@app.route('/api/v1/user', methods=['GET'])
def getUserInfo():
    userIdHash = hash(str(request.user_agent) + str(request.remote_addr))
    userInfo = db.getUserInfo(userIdHash)
    if (userInfo is None):
        userInfo = db.createUser(userIdHash)
    return jsonify(userInfo)


@ app.route('/addComment', methods=['POST'])
def addComment():

    print(request.form['ispovestId'])
    print(request.form['commentInput'])

    return index()

# todo: comments


def getKomentari(ispovestId):
    sql = """ SELECT * FROM komentar
              WHERE ispovestId = ? """
    komentariTuples = db.get_flask_db().cursor().execute(sql, (ispovestId,)).fetchall()
    return [db.dbKomentarToObject(komentarTuple) for komentarTuple in komentariTuples]


def likeKomentar(komentarId):
    pass


def dislikeKomentar(komentarId):
    pass


def postKomentar(ispovestId, komentar):
    pass
