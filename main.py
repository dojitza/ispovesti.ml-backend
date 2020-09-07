from flask import Flask, escape, request, jsonify
from flask import render_template
import datetime
import sqlite3
from flask import g
from ispovest import ispovest
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import os


DATABASE = 'database.db'

app = Flask(__name__)
CSRFProtect(app)
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
    }


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def getKomentari(ispovestId):
    sql = """ SELECT * FROM komentari
              WHERE ispovestId = ? """
    komentariTuples = get_db().cursor().execute(sql, (ispovestId,)).fetchall()
    return [parseKomentarTupleToDict(komentarTuple) for komentarTuple in komentariTuples]


@app.route('/api/v1/ispovesti', methods=['GET'])
def getIspovesti():
    sql = """ SELECT * FROM ispovesti """
    ispovestiTuples = get_db().cursor().execute(sql).fetchall()
    return jsonify([parseIspovestTupleToDict(ispovestTuple) for ispovestTuple in ispovestiTuples])


@app.route('/api/v1/ispovesti/<int:ispovestId>', methods=['GET'])
def getIspovest(ispovestId):
    sql = """ SELECT * FROM ispovesti
              WHERE id = ? """
    ispovest = get_db().cursor().execute(sql, (ispovestId,)).fetchone()
    parsedIspovest = parseIspovestTupleToDict(ispovest)
    parsedKomentari = getKomentari(ispovestId)
    parsedIspovest['comments'] = parsedKomentari
    return jsonify(parsedIspovest)


def postKomentar(ispovestId, komentar):
    print(request.user_agent, request.remote_addr)
    return jsonify(request.remote_addr)


@app.route('/api/v1/ispovesti/<int:ispovestId>/postLike', methods=['POST'])
def likeKomentar(komentarId):
    return jsonify('lajk')


@app.route('/api/v1/ispovesti/<int:ispovestId>/postDislike')
def dislikeKomentar(komentarId):
    pass


def likeIpovest(ispovestId):
    pass


def dislikeIpovest(ispovestId):
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
