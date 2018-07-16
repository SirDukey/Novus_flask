#!/opt/rh/rh-python36/root/usr/bin/python3

from flask import Flask, request, render_template, redirect, url_for, Response, flash, send_file
import thestandard_scraper
import joomag_scraper
import os
import pdf2jpg

app = Flask(__name__)

UPLOAD_FOLDER = '/Novus_flask/uploaded/'
ALLOWED_EXTENSIONS = set(['pdf'])
SECRET_KEY = 'oV8rgcvFY1YcEWo7jXmoPQi5gaeX1J'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    user = {'username': 'Mike'}
    return render_template('user.html', title='Scraper', user=user)


########################################################################################################################
# thestandard

@app.route('/downloading')
def downloading():

    url = request.args['url']
    pages = request.args['pages']

    return Response(thestandard_scraper.start_scrape(url, pages), mimetype='text/html')


@app.route('/thestandard', methods=['GET', 'POST'])
def thestandard():

    if request.method == 'POST':
        url = request.form.get('url')
        pages = request.form.get('pages')
        return redirect(url_for('downloading', title='The Standard', url=url, pages=pages))

    return render_template('thestandard.html', title='The Standard', thestandard_active='active')


########################################################################################################################
# Joomag

@app.route('/joomag_downloading')
def joomag_downloading():
    url = request.args['url']
    pages = request.args['pages']

    return Response(joomag_scraper.start_scrape(url, pages), mimetype='text/html')


@app.route('/joomag', methods=['GET', 'POST'])
def joomag():
    if request.method == 'POST':
        url = request.form.get('url')
        pages = request.form.get('pages')
        return redirect(url_for('joomag_downloading', title='Joomag', url=url, pages=pages))

    return render_template('joomag.html', title='Joomag', joomag_active='active')


########################################################################################################################
# pdf2jpg

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/pdf2jpg', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        try:
            file = request.files['file']

            if file and allowed_file(file.filename):
                # filename = secure_filename(file.filename)
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path_filename = '/Novus_flask/uploaded'
                filename = path_filename + '/' + filename
                flash(file.filename + ' converted successfully')
                pdf2jpg.convert2pdf(filename)
                return redirect(url_for('upload_file'))

            else:
                flash('only pdf file type allowed')
                return redirect(url_for('upload_file'))
        except Exception as e:
            if '400 Bad Request' in str(e):
                flash('please select a file')
                return redirect(url_for('upload_file'))

    return render_template('pdf2jpg.html', pdf2jpg_active='active')


@app.route('/pdf2jpg/converted.zip')
def download_file():

    return send_file('zip/converted.zip')


########################################################################################################################
# main application

if __name__ == '__main__':
    app.run(host='0.0.0.0')

