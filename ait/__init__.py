from flask import Flask, send_from_directory
from flask_login import LoginManager
from flask_socketio import SocketIO, send
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
import pyrebase

import os
import json
from datetime import datetime

with open(os.path.join(os.path.dirname(__file__), 'configs/admin_config.json')) as f:
    admin_config = json.load(f)

with open(os.path.join(os.path.dirname(__file__), 'configs/firebase_config.json')) as f:
    firebaseConfig =  json.load(f)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

cred = credentials.Certificate(admin_config)
firebase_admin.initialize_app(cred,{
    'storageBucket':'day-planner-5165f.appspot.com'
})

pyrebase = pyrebase.initialize_app(firebaseConfig)

db_fire = firestore.client()
login_manager = LoginManager(app)
login_manager.login_view = 'authentication.login'
login_manager.login_message_category = 'info'


from ait.views import authentication, chat, connection, error_handling, home, post, profile

app.register_blueprint(authentication.authentication)
app.register_blueprint(chat.chat)
app.register_blueprint(connection.connect)
app.register_blueprint(error_handling.error_handling)
app.register_blueprint(home.home)
app.register_blueprint(post.post)
app.register_blueprint(profile.profile)