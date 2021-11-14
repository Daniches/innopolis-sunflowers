import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import yolo
import calc
import kml

import cv2


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        name = request.headers['name']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sunflowers_count = request.headers['sunflowers_count']
            sunflowers_weight = request.headers['sunflowers_weight']
            seeds = yolo.count_seeds(filename)
            productivity = calc.get_productivity(sunflowers_weight, seeds, sunflowers_count)
            coordh = request.headers['coordh']
            coordw = request.headers['coordw']
            kml.update_file('pole', coordw, coordh, '1', productivity, sunflowers_count, sunflowers_weight, '1', name, '1', '1')
            
            return redirect(request.url)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

app.run()