
from flask import Flask, escape, request, jsonify, abort, Response, g
from flask_cors import CORS
import os
from time import time
from threading import Timer

import db
import constants
import helpers
import ispovestGeneratorClient


app = Flask(__name__)
CORS(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/api/v1/generateIspovest', methods=['POST'])
def generateIspovest():
    prefix = request.json['prefix']
    authorIdHash = hash(str(request.user_agent) + str(request.remote_addr))
    lastGenTimestamp = db.getLastGenTimestamp(authorIdHash)
    timeDifference = int(time()) - lastGenTimestamp

    if timeDifference > constants.GENERATION_THROTTLE_THRESHOLD:
        db.markGenTimestamp(authorIdHash)
        print('received: ' + prefix)

        started = ispovestGeneratorClient.generateIspovest(
            prefix, authorIdHash)

        if started:
            return Response(status=200)
        else:
            # todo if and when started is returned as False, change this to reflect the reason of it being false
            abort(500)

    else:
        return jsonify({'id': None, 'text': "You need to wait " + str(30 - timeDifference) + " more seconds before attempting another generation"})


@app.route('/api/v1/generateIspovest', methods=['GET'])
def getGeneratedIspovest():
    authorIdHash = hash(str(request.user_agent) + str(request.remote_addr))
    ispovestText = ispovestGeneratorClient.pollGeneratedIspovest(authorIdHash)
    if ispovestText is not None:
        print('sending: ' + ispovestText)
        ispovestRecord = db.addGeneratedIspovest(ispovestText, authorIdHash)
        ispovestRecord.pop('authorIdHash', None)
        return jsonify(ispovestRecord)
    else:
        return jsonify({'queuePosition': ispovestGeneratorClient.getQueuePosition(authorIdHash)})


@ app.route('/api/v1/publishIspovest', methods=['POST'])
def publishIspovest():
    ispovestId = request.json['ispovestId']
    authorName = request.json['authorName']
    authorName = authorName if authorName != "" else "Anonimus"
    authorIdHash = hash(str(request.user_agent) + str(request.remote_addr))
    published = db.publishGeneratedIspovest(
        ispovestId, authorName, authorIdHash)
    if (published):
        return Response(status=201, mimetype='application/json')
    else:
        abort(403)


@ app.route('/api/v1/queueLength', methods=['GET'])
def getQueueLength():
    return jsonify(ispovestGeneratorClient.getQueueLength())


@ app.route('/api/v1/queuePosition/', methods=['GET'])
def getQueuePosition():
    authorIdHash = hash(str(request.user_agent) + str(request.remote_addr))
    return jsonify(ispovestGeneratorClient.getQueuePosition(authorIdHash))


@ app.route('/api/v1/ispovesti', methods=['GET'])
def getIspovesti():
    page = request.args['page']
    authorIdHash = hash(str(request.user_agent) + str(request.remote_addr))
    ispovesti = db.getIspovesti(authorIdHash, page)
    return jsonify(ispovesti)


@ app.route('/api/v1/ispovesti/<int:ispovestId>', methods=['GET'])
def getIspovest(ispovestId):
    ispovest = db.getIspovest(ispovestId)
    return jsonify(ispovest)


@ app.route('/api/v1/arenaIspovesti', methods=['GET'])
def getArenaIspovesti():
    page = request.args['page']
    authorIdHash = hash(str(request.user_agent) + str(request.remote_addr))
    arenaIspovesti = db.getArenaIspovesti(authorIdHash, page)
    return jsonify(arenaIspovesti)


@ app.route('/api/v1/ispovesti/<int:ispovestId>/putReaction', methods=['PUT'])
def putIspovestReaction(ispovestId):
    reactionString = request.json
    reactionConstant = helpers.mapReactionStringToConstant(reactionString)
    success = db.putIspovestReaction(
        str(request.user_agent) + str(request.remote_addr), reactionConstant, ispovestId)
    if success:
        return Response(status=200, mimetype='application/json')
    else:
        abort(403)


@ app.route('/api/v1/arenaIspovesti/<int:arenaIspovestId>/putReaction', methods=['PUT'])
def putArenaIspovestReaction(arenaIspovestId):
    reactionString = request.json
    reactionConstant = helpers.mapReactionStringToConstant(reactionString)
    success = db.putArenaIspovestReaction(
        str(request.user_agent) + str(request.remote_addr), reactionConstant, arenaIspovestId)
    if success:
        return Response(status=200, mimetype='application/json')
    else:
        abort(403)


@ app.route('/api/v1/user', methods=['GET'])
def getUserInfo():
    userIdHash = hash(str(request.remote_addr))
    userInfo = db.getUserInfo(userIdHash)
    if (userInfo is None):
        userInfo = db.createUser(userIdHash)
    return jsonify(userInfo)


@ app.route('/addComment', methods=['POST'])
def addComment():

    print(request.json['ispovestId'])
    print(request.json['commentInput'])

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
