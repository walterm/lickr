# -*- coding: utf-8 -*-
from flask import Flask, request
# from cors import crossdomain
from PIL import Image
from collections import defaultdict
from pymongo import MongoClient
import scripts.tag_images as tag_images
import json
from scripts.cors import crossdomain


class ColorState():
    def __init__(self):
        self.cd = defaultdict(float)
        self.favorite = ''

cs = ColorState()
app = Flask(__name__)
client = MongoClient()
db = client["lickr"]
questions_collection = db["questions"]
images_collection = db["images"]
results = db["results"]


def tohex(color):
    r, g, b = color
    hexchars = "0123456789ABCDEF"
    return "#" \
        + hexchars[r / 16] \
        + hexchars[r % 16] \
        + hexchars[g / 16] \
        + hexchars[g % 16] \
        + hexchars[b / 16] \
        + hexchars[b % 16]


def convert_args_dict(args):
    def convert_key(string):
        start = string.index('[') + 3
        return string[start:-1]
    return {convert_key(key): float(args[key]) for key in args.keys()}


def compute_pixel_dict(path):
    colors = defaultdict(int)
    img = Image.open(path)
    for count, color in img.getcolors(img.size[0] * img.size[1]):
        colors[color] += count
    return colors


@app.route("/results", methods=["POST"])
@crossdomain(origin='*')
def save_results():
    colors = request.form.getlist('colors[]')
    colors = [str(color) for color in colors]
    results.insert({'colors': colors})
    return json.dumps({})


@app.route("/get_imgs", methods=["GET"])
@crossdomain(origin='*')
def get_imgs():
    similarity = defaultdict(float)
    colors = convert_args_dict(request.args)
    colors = [tag_images.compute_closest(color) for color in colors]
    img_results = images_collection.find({"main": {"$in": colors}})
    for img in img_results:
        img_id = img['_id']
        similarity[img_id] = tag_images.compute_conf_img_similarity(cs.cd, img)
    imgs = sorted(similarity.keys(), key=similarity.get, reverse=True)[:4]
    img_objs = []
    img_results.rewind()
    for img in img_results:
        if img['_id'] in imgs:
            img_objs.append(img)
    return json.dumps({"imgs": img_objs})

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)
