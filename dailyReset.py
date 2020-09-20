import db
import constants
# set all user's superlikes to 1


def resetSuperlikes():
    sql = """ 
        UPDATE user
        SET superlikesLeft = 1,
      """
    cur = get_db().cursor()
    cur.execute(sql, (userIdHash,))
    get_db().commit()

# pick the best ispovesti from arena and insert them to the main list


def processArena():
    sql = """ 
            SELECT 
            ai.*,
            sum(case when air.reaction = 0 then 1 else 0 end) AS dislikes,
            sum(case when air.reaction = 1 then 1 else 0 end) AS likes,
            sum(case when air.reaction = 2 then 1 else 0 end) AS superlikes
            FROM arenaIspovest ai
            JOIN arenaIspovestReaction air on ai.id = air.arenaIspovestId
			GROUP BY ai.id
            """
    ispovesti = get_db().cursor().execute(sql, (ispovestId,)).fetchall()
    topIspovesti = []
    for i in ispovesti:
        io = db.dbIspovestToObject(i)


# send the next batch to the arena
