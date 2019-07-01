import sqlite3

import waitress

from flask import Flask, render_template, request, redirect, url_for, session, flash

from app.test import test_db

import os

import math

from werkzeug.utils import secure_filename

from app.db import validate_user

UPLOAD_FOLDER = 'app/test/test_static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ADDS_PER_PAGE = 3




def test_test():
    pass