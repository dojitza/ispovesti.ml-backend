import constants


def mapReactionStringToConstant(reactionString):
    if (reactionString == 'like'):
        return constants.LIKE
    elif (reactionString == 'dislike'):
        return constants.DISLIKE
    elif (reactionString == 'superlike'):
        return constants.DISLIKE
    return constants.INVALID
