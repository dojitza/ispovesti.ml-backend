import datetime

comment = {
    'date' = datetime.datetime.utcnow(),
    'text': 'A comment',
}
'''
Reference for article definition
'''
article = {
    '_id': ObjectId()
    'title': 'A title',
    'text': 'Lorem ipsum sid dolor amet bla bla bla bla bla',
    'author': 'Sample author',
    'comments': [comment for i in range(5)],
    'image': 'https://images.freeimages.com/images/large-previews/d5d/powerlines-5-1389930.jpg',
}