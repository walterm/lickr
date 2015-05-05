from PIL import Image
from pymongo import MongoClient
from os import listdir, remove
from os.path import isfile, join

path = '../imgs/'
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
onlyfiles.pop(0)  # getting rid of .DS_Store

to_remove = []

# Find images to remove
for pic in onlyfiles:
    img = Image.open(path+pic)
    if img.size[0] < 100 and img.size[1] < 100:
        target = pic.split('.')[0]  # getting the photo number
        to_remove.append(target)

client = MongoClient()
db = client['lickr']
images = db['images']

images.remove({'_id': {'$in': to_remove}})
for pic in to_remove:
    remove(path + pic + '.jpg')