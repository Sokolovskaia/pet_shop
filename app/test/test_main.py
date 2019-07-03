import sqlite3

import waitress

from flask import Flask, render_template, request, redirect, url_for, session, flash

from app.test import test_db
from app import main, db

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


def open_db(url):
    connection = sqlite3.connect(url)
    connection.row_factory = sqlite3.Row
    return connection


def user():
    if 'id' in session and session['id'] is not None:
        user_login = session['login']
    else:
        user_login = 0
    return user_login


def test_all_pets():
    expected = ({'ad_id': 1, 'category': 'Собака', 'category_lowercased': 'собака', 'breed': 'Овчарка',
                 'breed_lowercased': 'овчарка', 'gender': 'М', 'birthdate': '01.2000', 'name': 'Жук',
                 'name_lowercased': 'жук', 'price': 1, 'photo': None, 'description': 'Умный', 'author_id': 1})
    actual_1 = db.all_pets(open_db(db_url), ADDS_PER_PAGE, pages_offset=0)
    actual = dict(actual_1[0])
    assert expected == actual


def test_test():
    pass
