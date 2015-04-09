import os
from flask import Flask, request, redirect, url_for, \
                    render_template, send_from_directory, session, flash
from werkzeug import secure_filename
from Geocoder import Geocoder, csvLoader, DataMapping
from tasks import hello # Celery task file and test function


# Flask config
UPLOAD_FOLDER = '{0}/data'.format(os.path.dirname(os.path.realpath(__file__)))
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Error Log
if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler('log.txt')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)



@app.route('/')
def home():
    session.clear()
    hello.delay(os.path.join(app.config['UPLOAD_FOLDER'], 'test.txt')) # Testing Celery process
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
            myCSV = csvLoader(filename=os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['uploaded_file'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            options = ['Address', 'City', 'State', 'Zip', 'Full Address']
            return render_template('upload-show.html', display=myCSV.show_columns(), options=options)
    return render_template('upload.html')

@app.route('/upload-process', methods=['GET', 'POST'])
def upload_process():
    if request.method == 'POST':
        myCSV = csvLoader(session['uploaded_file'])
        session['mapping_file'] = session['uploaded_file'] + '_mapping.csv'
        session['geocoded_file'] = session['uploaded_file'] + '_geocoded.csv'
        myMapping = DataMapping(filename=session['mapping_file'])
        mapping = []
        for i in range(myCSV.count_columns()):
            form_value = request.form.get(str(i))
            mapping.append([i, form_value])
        myMapping.dump_mapping(mapping)
        myCSV.geocode_csv(mapping=myMapping.lu_index(), outfilename=session['geocoded_file'])
        filename = session['geocoded_file'].split('/')[-1]

        return render_template('upload-process.html', count=myCSV.counter, filename=filename)
    flash('Please Upload a File')
    return redirect(url_for('upload_file'))

@app.route('/upload-result/<filename>', methods=['POST', 'GET'])
def upload_result(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Error Handling
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500






