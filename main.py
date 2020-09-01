from flask import Flask, escape, request
from flask import render_template
import datetime
import sqlite3
from flask import g
from ispovest import ispovest

DATABASE = 'database.db'

app = Flask(__name__)


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


def getIspovesti(page):
    sql = """ SELECT * FROM ispovesti """
    return get_db().cursor().execute(sql).fetchall()


def getKomentari(ispovestId):
    sql = """ SELECT * FROM komentari
              WHERE ispovestId = ? """
    return get_db().cursor().execute(sql, (ispovestId,)).fetchall()


def postKomentar(ispovestId, komentar):
    pass


def likeKomentar(komentarId):
    pass


def dislikeKomentar(komentarId):
    pass


def likeIpovest(ispovestId):
    pass


def dislikeIpovest(ispovestId):
    pass


def parseKomentarTupleToDict(komentarTuple):
    return {
        'author': komentarTuple[1],
        'text': komentarTuple[2],
        'likes': komentarTuple[4],
        'dislikes': komentarTuple[5]
    }


def parseispovestTupleToDict(ispovestTuple):
    comments = [parseKomentarTupleToDict(k) for k in getKomentari(
        ispovestId=ispovestTuple[0])]

    return {
        'text': ispovestTuple[1],
        'likes': ispovestTuple[2],
        'dislikes': ispovestTuple[3],
        'comments': comments
    }


@ app.route('/')
def index():

    ispovesti = [parseispovestTupleToDict(
        i) for i in getIspovesti(page=0)]

    # return str(ispovestiDicts)

    return render_template('index.html', ispovesti=ispovesti)


@ app.route('/addComment', methods=['POST'])
def addComment():

    print(request.form['ispovestId'])
    print(request.form['commentInput'])

    return index()
