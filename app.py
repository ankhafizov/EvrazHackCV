from flask import Flask, render_template
import yaml
import cv2

app = Flask(__name__)


@app.route('/')
def main_page():
    # image_classes = list(2)

    with open('images_paths.yml') as f:
        images_paths = yaml.load(f, Loader=yaml.FullLoader)
    images_classes = ['safe', 'dangerous', 'dangerous', 'safe']
    
    return render_template('main_page.html', images_paths=images_paths, image_classes=images_classes)


if __name__ == '__main__':
    app.run()
