from flask import Flask, render_template
import yaml
import cv2
import requests

app = Flask(__name__)


@app.route('/')
def main_page():
    # image_classes = list(2)
    images = {}

    with open('images_paths.yml') as f:
        images_paths = yaml.load(f, Loader=yaml.FullLoader)[0]

    for i in range(len(images_paths)):
        with open(images_paths['camera{}'.format(i + 1)], 'rb') as file:
            images['camera{}'.format(i + 1)] = file.read()

    # response = requests.post()

    images_classes = ['safe', 'dangerous', 'dangerous', 'safe']

    return render_template('main_page.html', images_paths=images_paths, image_classes=images_classes)


if __name__ == '__main__':
    app.run()
