from flask import Flask, request
from cors import crossdomain
import PIL
app = Flask(__name__)


@app.route("/process_imgs", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def process_images():
    print request.form.getlist('imgs[]')
    return 'test'


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)
