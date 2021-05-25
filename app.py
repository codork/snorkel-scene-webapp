from flask import Flask

UPLOAD_FOLDER = 'static/uploads/'
DOWNLOAD_FOLDER = 'static/download/'
STATIC_FOLDER = 'static/'

app = Flask(__name__, static_url_path='/static')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

