import sqlite3

import waitress

from flask import Flask, render_template, request, redirect, url_for, session, flash

from app.test import test_db
from app import main

import os

import math

from werkzeug.utils import secure_filename

from app.db import validate_user

UPLOAD_FOLDER = 'app/test/test_static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ADDS_PER_PAGE = 3



app = Flask(__name__)
app.config['uploads'] = UPLOAD_FOLDER

app.config.from_mapping(
    SECRET_KEY='Marina_secret_key_test',
)
db_url = 'test_db.sqlite'


def user():
    if 'id' in session and session['id'] is not None:
        user_login = session['login']
    else:
        user_login = 0
    return user_login

def test_search():
    pass




