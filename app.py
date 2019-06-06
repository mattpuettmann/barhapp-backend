from flask import Flask, g
from resources.users import users_api
from flask_cors import CORS, cross_origin
from flask_login import current_user, LoginManager
import models

DEBUG = True
PORT = 8000

login_manager = LoginManager()
app = Flask(__name__)
app.secret_key = 'fewfrwfhu4h4gfhu4gt'
login_manager.init_app(app)

CORS(users_api, origins=["http://localhost:3000"], supports_credentials=True)
app.register_blueprint(users_api, url_prefix='/users')

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hi'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)