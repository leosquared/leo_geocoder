import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename


UPLOAD_FOLDER = '{0}/data'.format(os.path.dirname(os.path.realpath(__file__)))
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler('log.txt')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

@app.route('/')
def home():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

