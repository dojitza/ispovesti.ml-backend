import constants


def mapReactionStringToConstant(reactionString):
    if (reactionString == 'like'):
        return constants.LIKE
    elif (reactionString == 'dislike'):
        return constants.DISLIKE
    elif (reactionString == 'superlike'):
        return constants.SUPERLIKE
    return constants.INVALID


def decreaseGenerationQueueLength():
    sql = """UPDATE queueLength SET queueLength=queueLength-1"""
    cur = get_flask_db().cursor()
    cur.execute(sql)
    get_flask_db().commit()
    print('decreasing')
    return cur.lastrowid + cur.rowcount
