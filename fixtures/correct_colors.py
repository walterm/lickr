from pymongo import MongoClient

client = MongoClient()
db = client['lickr']
images = db['images']

red = [1, 72, 97, 104, 112, 128, 132, 138]
red = [str(i) for i in red]
orange = [4, 24, 35, 40, 65, 82, 84, 99, 114, 119, 121, 155]
orange = [str(i) for i in orange]
yellow = [11, 64, 86]
yellow = [str(i) for i in yellow]
green = [44, 63, 68, 74, 90, 135]
green = [str(i) for i in green]
blue = [7, 23, 25, 28, 54, 73, 80, 85, 100, 116, 125, 131, 147, 150]
blue = [str(i) for i in blue]
purple = [14, 71, 123, 127, 145]
purple = [str(i) for i in purple]

print images.update_many({'_id':{'$in':red}}, {'$set':{'main': 'ff0000'}})
print images.update_many({'_id':{'$in':orange}}, {'$set':{'main': 'ffa500'}})
print images.update_many({'_id':{'$in':yellow}}, {'$set':{'main': 'ffff00'}})
print images.update_many({'_id':{'$in':green}}, {'$set':{'main': '008000'}})
print images.update_many({'_id':{'$in':blue}}, {'$set':{'main': '0000ff'}})
print images.update_many({'_id':{'$in':purple}}, {'$set':{'main': '800080'}})