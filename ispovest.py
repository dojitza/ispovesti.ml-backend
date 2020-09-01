import datetime

comment = {
    'date': datetime.datetime.utcnow(),
    'text': 'A comment',
    'author': 'Ljupkica'
}
'''
Reference for ispovest definition
'''
ispovest = {
    '_id': 1,
    # 'title': 'A title',
    'text': 'Verenik i ja verili smo se pred dve sedmice, ima da ih nema',
    # 'author': 'Sample author',
    'comments': [comment for i in range(20)],
    # 'image': 'https://images.freeimages.com/images/large-previews/d5d/powerlines-5-1389930.jpg',
}
