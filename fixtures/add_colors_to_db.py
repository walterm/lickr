# -*- coding: utf-8 -*-

###########################################################
############## Adding top colors to Mongo #################
###########################################################
import sys
sys.path.append('/Users/walterm/Development/lickr/')
import glob
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from scripts.tag_images import compute_colors, compute_closest, average

# Setting up the Mongo connection
client = MongoClient()

# The collection for the questions
db = client["lickr"]
images_collection = db["images"]

# List of all of the pictures to enter
pictures = glob.glob('../imgs/*.jpg')

for pic in pictures:
    print pic
    img_num = pic.split('/')[2].split('.')[0]
    top_colors, most = compute_colors(pic)
    most_similar = compute_closest(most)
    obj = None
    try:
        obj = {
            '_id': img_num,
            'top_colors': top_colors,
            'main': most_similar
        }
        if len(obj['top_colors']) != 4:
            continue
    except:
        continue

    try:
        images_collection.insert(obj)
    except DuplicateKeyError:
        continue