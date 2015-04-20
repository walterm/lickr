# -*- coding: utf-8 -*-

###########################################################
############## Adding top colors to Mongo #################
###########################################################
import sys
sys.path.append('/Users/walterm/Development/lickr/')
import glob
from pymongo import MongoClient
from scripts.tag_images import compute_colors, compute_closest

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
    top_colors = compute_colors(pic)
    most_similar = compute_closest(top_colors[0])
    obj = {
        '_id': img_num,
        'top_colors': top_colors,
        'main': most_similar
    }

    images_collection.insert(obj)