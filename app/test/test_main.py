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
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ADDS_PER_PAGE = 6

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
    expected = [{'ad_id': 1, 'category': 'Собака', 'category_lowercased': 'собака', 'breed': 'Овчарка',
                 'breed_lowercased': 'овчарка', 'gender': 'М', 'birthdate': '01.2000', 'name': 'Жук',
                 'name_lowercased': 'жук', 'price': 1, 'photo': None, 'description': 'Умный', 'author_id': 1},
                {'ad_id': 2, 'category': 'Собака', 'category_lowercased': 'собака', 'breed': 'Овчарка',
                 'breed_lowercased': 'овчарка', 'gender': 'М', 'birthdate': '01.2000', 'name': 'Жук',
                 'name_lowercased': 'жук', 'price': 1, 'photo': None, 'description': 'Умный', 'author_id': 1},
                {'ad_id': 3, 'category': 'Кошка', 'category_lowercased': 'кошка', 'breed': 'Перс',
                 'breed_lowercased': 'перс', 'gender': 'Ж', 'birthdate': '02.2000', 'name': 'Бука',
                 'name_lowercased': 'бука', 'price': 2, 'photo': '', 'description': 'Веселая', 'author_id': 2},
                {'ad_id': 4, 'category': 'Кошка', 'category_lowercased': 'кошка', 'breed': 'Перс',
                 'breed_lowercased': 'перс', 'gender': 'Ж', 'birthdate': '02.2000', 'name': 'Бука',
                 'name_lowercased': 'бука', 'price': 2, 'photo': '', 'description': 'Веселая', 'author_id': 2},
                {'ad_id': 5, 'category': 'Хомяк', 'category_lowercased': 'хомяк', 'breed': 'Рыжий',
                 'breed_lowercased': 'рыжий', 'gender': 'М', 'birthdate': '03.2000', 'name': 'Хома',
                 'name_lowercased': 'хома', 'price': 3, 'photo': None, 'description': 'Вредный', 'author_id': 1}]
    actual_result = db.all_pets(open_db(db_url), ADDS_PER_PAGE, pages_offset=0)
    actual = []
    for act in actual_result:
        act = dict(act)
        actual.append(act)
    assert expected == actual


def test_all_pets_list_dogs():
    expected = [{'ad_id': 1, 'category': 'Собака', 'category_lowercased': 'собака', 'breed': 'Овчарка',
                 'breed_lowercased': 'овчарка', 'gender': 'М', 'birthdate': '01.2000', 'name': 'Жук',
                 'name_lowercased': 'жук', 'price': 1, 'photo': None, 'description': 'Умный', 'author_id': 1},
                {'ad_id': 2, 'category': 'Собака', 'category_lowercased': 'собака', 'breed': 'Овчарка',
                 'breed_lowercased': 'овчарка', 'gender': 'М', 'birthdate': '01.2000', 'name': 'Жук',
                 'name_lowercased': 'жук', 'price': 1, 'photo': None, 'description': 'Умный', 'author_id': 1}]
    actual_result = db.all_pets(open_db(db_url), ADDS_PER_PAGE, pages_offset=0, category='Собака')
    actual = []
    for act in actual_result:
        act = dict(act)
        actual.append(act)
    assert expected == actual


def test_all_pets_cats():
    expected = [{'ad_id': 3, 'category': 'Кошка', 'category_lowercased': 'кошка', 'breed': 'Перс',
                 'breed_lowercased': 'перс', 'gender': 'Ж', 'birthdate': '02.2000', 'name': 'Бука',
                 'name_lowercased': 'бука', 'price': 2, 'photo': '', 'description': 'Веселая', 'author_id': 2},
                {'ad_id': 4, 'category': 'Кошка', 'category_lowercased': 'кошка', 'breed': 'Перс',
                 'breed_lowercased': 'перс', 'gender': 'Ж', 'birthdate': '02.2000', 'name': 'Бука',
                 'name_lowercased': 'бука', 'price': 2, 'photo': '', 'description': 'Веселая', 'author_id': 2}]
    actual_result = db.all_pets(open_db(db_url), ADDS_PER_PAGE, pages_offset=0, category='Кошка')
    actual = []
    for act in actual_result:
        act = dict(act)
        actual.append(act)
    assert expected == actual


def test_all_pets_another():
    expected = [{'ad_id': 5, 'category': 'Хомяк', 'category_lowercased': 'хомяк', 'breed': 'Рыжий',
                 'breed_lowercased': 'рыжий', 'gender': 'М', 'birthdate': '03.2000', 'name': 'Хома',
                 'name_lowercased': 'хома', 'price': 3, 'photo': None, 'description': 'Вредный', 'author_id': 1}]
    actual_result = db.all_pets(open_db(db_url), ADDS_PER_PAGE, pages_offset=0, category='Прочие')
    actual = []
    for act in actual_result:
        act = dict(act)
        actual.append(act)
    assert expected == actual


def test_search_by_ad_id():
    expected = {'ad_id': 5, 'category': 'Хомяк', 'breed': 'Рыжий', 'gender': 'М', 'birthdate': '03.2000',
                'name': 'Хома', 'price': 3, 'photo': None, 'description': 'Вредный', 'author_id': 1,
                'surname': 'Иванова', 'author_name': 'Анна', 'phone_number': 55555}

    ad_id = expected['ad_id']
    actual = dict(db.search_by_ad_id(open_db(db_url), ad_id))
    assert expected == actual


def test_search_pets_category():
    expected = [{'ad_id': 1, 'category': 'Собака', 'category_lowercased': 'собака', 'breed': 'Овчарка',
                 'breed_lowercased': 'овчарка', 'gender': 'М', 'birthdate': '01.2000', 'name': 'Жук',
                 'name_lowercased': 'жук', 'price': 1, 'photo': None, 'description': 'Умный', 'author_id': 1},
                {'ad_id': 2, 'category': 'Собака', 'category_lowercased': 'собака', 'breed': 'Овчарка',
                 'breed_lowercased': 'овчарка', 'gender': 'М', 'birthdate': '01.2000', 'name': 'Жук',
                 'name_lowercased': 'жук', 'price': 1, 'photo': None, 'description': 'Умный', 'author_id': 1}]
    search = 'собака'
    actual_result = db.search_pets(open_db(db_url), search, ADDS_PER_PAGE, pages_offset=0)
    actual = []
    for act in actual_result:
        act = dict(act)
        actual.append(act)
    assert expected == actual


def test_search_pets_name():
    expected = [{'ad_id': 1, 'category': 'Собака', 'category_lowercased': 'собака', 'breed': 'Овчарка',
                 'breed_lowercased': 'овчарка', 'gender': 'М', 'birthdate': '01.2000', 'name': 'Жук',
                 'name_lowercased': 'жук', 'price': 1, 'photo': None, 'description': 'Умный', 'author_id': 1},
                {'ad_id': 2, 'category': 'Собака', 'category_lowercased': 'собака', 'breed': 'Овчарка',
                 'breed_lowercased': 'овчарка', 'gender': 'М', 'birthdate': '01.2000', 'name': 'Жук',
                 'name_lowercased': 'жук', 'price': 1, 'photo': None, 'description': 'Умный', 'author_id': 1}]
    search = 'жук'
    actual_result = db.search_pets(open_db(db_url), search, ADDS_PER_PAGE, pages_offset=0)
    actual = []
    for act in actual_result:
        act = dict(act)
        actual.append(act)
    assert expected == actual


def test_search_pets_breed():
    expected = [{'ad_id': 5, 'category': 'Хомяк', 'category_lowercased': 'хомяк', 'breed': 'Рыжий',
                 'breed_lowercased': 'рыжий', 'gender': 'М', 'birthdate': '03.2000', 'name': 'Хома',
                 'name_lowercased': 'хома', 'price': 3, 'photo': None, 'description': 'Вредный', 'author_id': 1}]
    search = 'рыжий'
    actual_result = db.search_pets(open_db(db_url), search, ADDS_PER_PAGE, pages_offset=0)
    actual = []
    for act in actual_result:
        act = dict(act)
        actual.append(act)
    assert expected == actual


def test_search_pets_breed_no_result():
    expected = []
    search = 'боксер'
    actual = db.search_pets(open_db(db_url), search, ADDS_PER_PAGE, pages_offset=0)
    assert expected == actual


def test_validate_user_success():
    expected = {'id': 1, 'login': 'anna', 'surname': 'Иванова', 'name': 'Анна', 'phone_number': 55555, 'success': True}
    login = 'anna'
    password = '1'
    actual = dict(db.validate_user(open_db(db_url), login, password))
    assert expected == actual


def test_validate_user_error_login():
    expected = {'error': 'Пользователь не найден', 'success': False}
    login = 'ana'
    password = '1'
    actual = dict(db.validate_user(open_db(db_url), login, password))
    assert expected == actual


def test_validate_user_error_password():
    expected = {'error': 'Неверный пароль', 'success': False}
    login = 'anna'
    password = '2'
    actual = dict(db.validate_user(open_db(db_url), login, password))
    assert expected == actual


def test_all_ads_count():
    expected = 5
    actual_1 = db.all_ads_count(open_db(db_url), category=None)
    actual = actual_1['count_ads']
    assert expected == actual


def test_all_ads_count_dogs():
    expected = 2
    actual_1 = db.all_ads_count(open_db(db_url), category='Собака')
    actual = actual_1['count_ads']
    assert expected == actual


def test_all_ads_count_cats():
    expected = 2
    actual_1 = db.all_ads_count(open_db(db_url), category='Кошка')
    actual = actual_1['count_ads']
    assert expected == actual


def test_all_ads_count_another():
    expected = 1
    actual_1 = db.all_ads_count(open_db(db_url), category='Прочие')
    actual = actual_1['count_ads']
    assert expected == actual


def test_all_ads_count_search_by_id():
    expected = 1
    search = 1
    actual_1 = db.all_ads_count_search(open_db(db_url), search)
    actual = actual_1['count_ads']
    assert expected == actual


def test_all_ads_count_search_by_breed():
    expected = 2
    search = 'Овчарка'
    actual_1 = db.all_ads_count_search(open_db(db_url), search)
    actual = actual_1['count_ads']
    assert expected == actual


def test_all_ads_count_search_by_category():
    expected = 2
    search = 'Кошка'
    actual_1 = db.all_ads_count_search(open_db(db_url), search)
    actual = actual_1['count_ads']
    assert expected == actual


def test_all_ads_count_search_by_name():
    expected = 1
    search = 'Хома'
    actual_1 = db.all_ads_count_search(open_db(db_url), search)
    actual = actual_1['count_ads']
    assert expected == actual


def test_all_ads_for_user():
    expected = [{'ad_id': 3, 'category': 'Кошка', 'category_lowercased': 'кошка', 'breed': 'Перс',
                 'breed_lowercased': 'перс', 'gender': 'Ж', 'birthdate': '02.2000', 'name': 'Бука',
                 'name_lowercased': 'бука', 'price': 2, 'photo': '', 'description': 'Веселая', 'author_id': 2},
                {'ad_id': 4, 'category': 'Кошка', 'category_lowercased': 'кошка', 'breed': 'Перс',
                 'breed_lowercased': 'перс', 'gender': 'Ж', 'birthdate': '02.2000', 'name': 'Бука',
                 'name_lowercased': 'бука', 'price': 2, 'photo': '', 'description': 'Веселая', 'author_id': 2}]
    username = 2
    actual_result = db.all_ads_for_user(open_db(db_url), username)
    actual = []
    for act in actual_result:
        act = dict(act)
        actual.append(act)
    assert expected == actual


def test_all_ads_for_user_empty():
    expected = []
    username = 10
    actual = db.all_ads_for_user(open_db(db_url), username)
    assert expected == actual


def test_number_of_ads():
    expected = 3
    username = 1
    actual_1 = db.number_of_ads(open_db(db_url), username)
    actual = actual_1['ads']
    assert expected == actual


def test_is_favorites():
    expected = [{'id': 1, 'ad': 1, 'user': 1}]
    ad = 1
    user = 1
    actual_result = db.is_favorites(open_db(db_url), ad, user)
    actual = []
    for act in actual_result:
        act = dict(act)
        actual.append(act)
    assert expected == actual


def test_is_favorites_no():
    expected = []
    ad = 3
    user = 2
    actual = db.is_favorites(open_db(db_url), ad, user)
    assert expected == actual


def test_counting_favorites():
    expected = 3
    ad = 1
    actual = db.counting_favorites(open_db(db_url), ad)['number_users']
    assert expected == actual

def test_favorites_for_user():
    user_id = 3
    expected = [{'ad_id': 1, 'category': 'Собака', 'breed': 'Овчарка', 'name': 'Жук', 'price': 1, 'photo': None}]
    actual_result = db.favorites_for_user(open_db(db_url), user_id)
    actual = []
    for act in actual_result:
        act = dict(act)
        actual.append(act)
    assert expected == actual


