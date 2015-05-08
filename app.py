# -*- coding: utf-8 -*-
from flask import Flask, request
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
selections = db["selections"]

IMAGE_DICT = {
    'ff0000': ['1', '104', '132', '138'],
    'ffa500': ['4', '84', '114', '137'],
    'ffff00': ['86',  '103', '110', '140'],
    '008000': ['32', '63', '91', '108'],
    '0000ff': ['23', '85', '100', '130'],
    '800080': ['30', '71', '98', '105']
}


def convert_args_dict(args):
    def convert_key(string):
        start = string.index('[') + 3
        return string[start:-1]
    return {convert_key(key): float(args[key]) for key in args.keys()}


@app.route("/get_favorites/<favorite>", methods=['GET'])
@crossdomain(origin='*')
def get_favorite_color_imgs(favorite):
    ids = IMAGE_DICT[favorite]
    img_objs = images_collection.find({'_id': {'$in': ids}})
    return json.dumps({"imgs": list(img_objs)})


@app.route("/palette", methods=["POST"])
@crossdomain(origin='*')
def process_palette():
    colors = request.form.getlist('colors[]')
    colors = [str(color) for color in colors]
    try:
        print "success"
        palette = tag_images.palette_cluster(colors)
        results_id = results.insert({'colors': palette})
        selections.insert({'palette_id': results_id, 'colors': colors})
    except:
        print "error"
        palette = tag_images.random_palette(colors)
        results_id = results.insert({'colors': palette, 'error': True})
    return json.dumps({'palette': palette})


@app.route("/get_imgs", methods=["GET"])
@crossdomain(origin='*')
def get_imgs():
    try:
        similarity = defaultdict(float)
        colors_dict = convert_args_dict(request.args)
        colors = [tag_images.compute_closest(color) for color in colors_dict.keys()]
        img_results = images_collection.find({"main": {"$in": colors}})
        for img in img_results:
            img_id = img['_id']
            similarity[img_id] = tag_images.compute_conf_img_similarity(colors_dict, img)
        imgs = sorted(similarity.keys(), key=similarity.get, reverse=True)[:4]
        img_objs = []
        img_results.rewind()
        for img in img_results:
            if img['_id'] in imgs:
                img_objs.append(img)
        img_results.close()
        return json.dumps({"imgs": img_objs})
    except:
        imgs = tag_images.random_images(images_collection)
        return json.dumps({"imgs": img_objs})

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)
