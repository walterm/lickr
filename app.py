# -*- coding: utf-8 -*-
from flask import Flask, request
# from cors import crossdomain
from PIL import Image
from collections import defaultdict
from pymongo import MongoClient
import scripts.tag_images as tag_images
import json
import ast


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


@app.route("/api/questions/<int:q_id>")
def read_question(q_id):
    obj = questions_collection.find_one({"_id": q_id})
    obj = {"question": obj}
    return json.dumps(obj)


@app.route("/process_imgs", methods=['POST', 'OPTIONS'])
def process_images():
    colors = defaultdict(int)
    # getting img names from post request
    imgs = request.form['imgs']
    imgs = [item.encode('ascii') for item in ast.literal_eval(imgs)]
    filepath = "./img/%s"
    imgs = [filepath % (img) for img in imgs]

    for img in imgs:
        pixel_dict = compute_pixel_dict(img)
        for color, count in pixel_dict.iteritems():
            if type(color) is tuple:
                colors[color] += count
    color_keys = sorted(colors, key=colors.get, reverse=True)[:4]
    converted = [tohex(key) for key in color_keys]
    return json.dumps({'colors': converted}), 200


# TODO: this route might not make sense if we can do it from Ember
@app.route("/favorite", methods=["POST"])
def set_favorite():
    cs.favorite = str(request.form['favorite'])
    return json.dumps({})


@app.route("/palette", methods=["GET"])
def return_palette():
    return json.dumps(cs.cd)


@app.route("/get_imgs", methods=["GET"])
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

    print imgs
    return json.dumps({"imgs": img_objs})

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)
