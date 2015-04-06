from flask import Flask, request
from cors import crossdomain
from PIL import Image
from collections import defaultdict
app = Flask(__name__)

def compute_pixel_dict(path):
    colors = defaultdict(int)
    img = Image.open(path)
    pixels = img.load()
    w, h = img.size
    for x in range(w):
        for y in range(h):
            colors[pixels[x, y]] += 1

    return colors

@app.route("/process_imgs", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def process_images():
    # getting img names from post request
    imgs = request.form.getlist('imgs[]')
    #converting from unicode
    imgs = [str(img) for img in imgs]

    filepath = "./img/%s.jpg"
    imgs = [filepath % (img) for img in imgs]

    for img in imgs:
        print img
        compute_pixel_dict(img)

    return '', 200

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)