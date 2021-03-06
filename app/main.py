import sqlite3

import waitress

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt

from app import db

import os

import math

from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'app/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ADDS_PER_PAGE = 6


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def start():
    app = Flask(__name__)
    bcrypt = Bcrypt(app)

    app.config['uploads'] = UPLOAD_FOLDER

    app.config.from_mapping(
        SECRET_KEY='Marina_secret_key',
    )
    db_url = 'db.sqlite'

    def user():
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
        else:
            user_login = 0
        return user_login

    @app.route('/search/', methods=('GET', 'POST'))
    def search():
        search = request.args.get('search')
        search_lowecased = search.strip().lower()
        user_login = user()
        number_of_ads = db.all_ads_count_search(db.open_db(db_url), search_lowecased)
        numb = number_of_ads['count_ads']
        number_of_pages = math.ceil(numb / ADDS_PER_PAGE)

        search_result = db.search_pets(db.open_db(db_url), search_lowecased, ADDS_PER_PAGE, pages_offset=0)

        if 'pages_offset' in request.args.keys():
            pages_offset = request.args.get('pages_offset')
            search = request.args.get('search')
            search_result = db.search_pets(db.open_db(db_url), search_lowecased, ADDS_PER_PAGE, pages_offset)

        return render_template('index.html', pets=search_result, search=search, active_index='search',
                               user_login=user_login, number_of_pages=number_of_pages,
                               limit=ADDS_PER_PAGE)

    @app.route('/login', methods=('GET', 'POST'))
    def login():
        user_login = user()
        if request.method == 'POST':
            result = {'success': False}
            login = request.form['login']
            password = request.form['password']
            val = db.validate_user(db.open_db(db_url), login)
            if val is None:
                result['error'] = 'Пользователь не найден'
                flash(result['error'])
            elif val is not None:
                valid_password = bcrypt.check_password_hash(val['password'], password)
                if valid_password == False:
                    result['error'] = 'Неверный пароль'
                    flash(result['error'])
                    return render_template('login.html', user_login=user_login)
                elif valid_password == True:
                    session.clear()
                    session['id'] = val['id']
                    session['login'] = val['login']
                    session['surname'] = val['surname']
                    session['name'] = val['name']
                    session['phone_number'] = val['phone_number']
                return redirect(url_for('account', username=session['id']))
        return render_template('login.html', user_login=user_login)

    @app.route('/logout')
    def logout():
        session.pop('id', None)
        return redirect(url_for('all_pets'))

    @app.route('/account', methods=('GET', 'POST'))
    def account():
        username = session['id']
        user_login = session['login']
        user_surname = session['surname']
        user_name = session['name']
        user_phone_number = session['phone_number']
        ads_for_user = db.all_ads_for_user(db.open_db(db_url), username)
        number_of_ads_for_user = db.number_of_ads(db.open_db(db_url), username)
        return render_template('account.html', ads_for_user=ads_for_user, number_of_ads_for_user=number_of_ads_for_user,
                               user_id=username, user_login=user_login, user_surname=user_surname,
                               user_name=user_name, user_phone_number=user_phone_number, active_index='account')

    @app.route('/', methods=('GET', 'POST'))
    def all_pets():
        user_login = user()
        all_ads_count_result = db.all_ads_count(db.open_db(db_url))
        number_of_ads = all_ads_count_result['count_ads']
        number_of_pages = math.ceil(number_of_ads / ADDS_PER_PAGE)
        all_pets_result = db.all_pets(db.open_db(db_url), ADDS_PER_PAGE, pages_offset=0)
        if 'pages_offset' in request.args.keys():
            pages_offset = request.args.get('pages_offset')
            all_pets_result = db.all_pets(db.open_db(db_url), ADDS_PER_PAGE, pages_offset)

        return render_template('index.html', pets=all_pets_result, active_index='all_pets', user_login=user_login,
                               number_of_pages=number_of_pages, limit=ADDS_PER_PAGE)

    @app.route('/dogs', methods=('GET', 'POST'))
    def dogs():
        user_login = user()
        all_ads_count_result = db.all_ads_count(db.open_db(db_url), category='Собака')
        number_of_ads = all_ads_count_result['count_ads']
        number_of_pages = math.ceil(number_of_ads / ADDS_PER_PAGE)
        dogs_result = db.all_pets(db.open_db(db_url), ADDS_PER_PAGE, pages_offset=0, category='Собака')
        if 'pages_offset' in request.args.keys():
            pages_offset = request.args.get('pages_offset')
            dogs_result = db.all_pets(db.open_db(db_url), ADDS_PER_PAGE, pages_offset, category='Собака')
        return render_template('index.html', pets=dogs_result, active_index='dogs', user_login=user_login,
                               number_of_pages=number_of_pages, limit=ADDS_PER_PAGE)

    @app.route('/cats', methods=('GET', 'POST'))
    def cats():
        user_login = user()
        all_ads_count_result = db.all_ads_count(db.open_db(db_url), category='Кошка')
        number_of_ads = all_ads_count_result['count_ads']
        number_of_pages = math.ceil(number_of_ads / ADDS_PER_PAGE)
        cats_result = db.all_pets(db.open_db(db_url), ADDS_PER_PAGE, pages_offset=0, category='Кошка')
        if 'pages_offset' in request.args.keys():
            pages_offset = request.args.get('pages_offset')
            cats_result = db.all_pets(db.open_db(db_url), ADDS_PER_PAGE, pages_offset, category='Кошка')
        return render_template('index.html', pets=cats_result, active_index='cats', user_login=user_login,
                               number_of_pages=number_of_pages, limit=ADDS_PER_PAGE)

    @app.route('/another_pets', methods=('GET', 'POST'))
    def another_pets():
        user_login = user()
        all_ads_count_result = db.all_ads_count(db.open_db(db_url), category='Прочие')
        number_of_ads = all_ads_count_result['count_ads']
        number_of_pages = math.ceil(number_of_ads / ADDS_PER_PAGE)
        another_pets_result = db.all_pets(db.open_db(db_url), ADDS_PER_PAGE, pages_offset=0, category='Прочие')
        if 'pages_offset' in request.args.keys():
            pages_offset = request.args.get('pages_offset')
            another_pets_result = db.all_pets(db.open_db(db_url), ADDS_PER_PAGE, pages_offset, category='Прочие')
        return render_template('index.html', pets=another_pets_result, active_index='another_pets',
                               user_login=user_login,
                               number_of_pages=number_of_pages, limit=ADDS_PER_PAGE)

    @app.route("/details/<ad_id>", methods=('GET', 'POST'))
    def details(ad_id):
        favor = -1
        counting_favor = db.counting_favorites(db.open_db(db_url), ad_id)
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
            user = session['id']
            is_favor = db.is_favorites(db.open_db(db_url), ad_id, user)
            empty = []
            if is_favor == empty:
                favor = 0
            else:
                favor = 1
        else:
            user_login = 0
        search_by_ad_id_result = db.search_by_ad_id(db.open_db(db_url), ad_id)
        return render_template('details.html', pet=search_by_ad_id_result, user_login=user_login, favor=favor,
                               counting_favor=counting_favor)

    @app.route('/new_pet', methods=('GET', 'POST'))
    def new_pet():
        user_login = user()
        if 'id' in session and session['id'] is not None:
            if request.method == 'GET':
                return render_template('new_pet.html', user_login=user_login)

            if request.method == 'POST':
                category = request.form['category']
                category_lowercased = category.strip().lower()
                breed = request.form['breed']
                breed_lowercased = breed.strip().lower()
                gender = request.form['gender']
                birthdate = request.form['birthdate']
                name = request.form['name']
                name_lowercased = name.strip().lower()
                price = int(request.form['price'])
                photo = None
                file = request.files['file']
                if file and allowed_file(file.filename):
                    photo = secure_filename(file.filename)
                    file.save(os.path.join(app.config['uploads'], photo))
                description = request.form['description']
                author_id = session['id']
                db.create_new_pet(db.open_db(db_url), category, category_lowercased, breed, breed_lowercased, gender, birthdate, name, name_lowercased, price, photo,
                                  description, author_id)
                return redirect(url_for('all_pets'))

            return render_template('new_pet.html')

        else:
            return redirect(url_for('login'))

    @app.route("/remove/<ad_id>", methods=['GET', 'POST'])
    def remove(ad_id):
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
            if request.method == 'GET':
                search_by_ad_id_result = db.search_by_ad_id(db.open_db(db_url), ad_id)
                return render_template('remove.html', pet=search_by_ad_id_result, user_login=user_login)
            if request.method == 'POST':
                search_by_ad_id_result = db.search_by_ad_id(db.open_db(db_url), ad_id)
                photo_name_1 = search_by_ad_id_result['photo']
                if photo_name_1:
                    photo_name = os.path.join(app.config['uploads'], photo_name_1)
                    if os.path.isfile(photo_name):
                        os.remove(photo_name)
                db.remove_by_ad_id(db.open_db(db_url), ad_id)
                return redirect(url_for('all_pets'))
        else:
            return redirect(url_for('login'))

    @app.route("/edit/<ad_id>", methods=['GET', 'POST'])
    def edit(ad_id):
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
            if request.method == 'GET':
                search_by_ad_id_result = db.search_by_ad_id(db.open_db(db_url), ad_id)
                return render_template('edit.html', pet=search_by_ad_id_result, user_login=user_login)

            if request.method == 'POST':
                category = request.form['category']
                category_lowercased = category.strip().lower()
                breed = request.form['breed']
                breed_lowercased = category.strip().lower()
                gender = request.form['gender']
                birthdate = request.form['birthdate']
                name = request.form['name']
                name_lowercased = name.strip().lower()
                price = int(request.form['price'])
                file = request.files['file']
                photo = None
                if file and allowed_file(file.filename):
                    photo = secure_filename(file.filename)
                    file.save(os.path.join(app.config['uploads'], photo))
                description = request.form['description']
                db.edit_by_ad_id(db.open_db(db_url), ad_id, category, category_lowercased, breed, breed_lowercased, gender, birthdate, name, name_lowercased, price, photo,
                                 description)
                return redirect(url_for('all_pets', ad_id=ad_id))
        else:
            return redirect(url_for('login'))

    @app.route('/about', methods=('GET', 'POST'))
    def about():
        user_login = user()
        return render_template('about.html', user_login=user_login)

    @app.route('/registration', methods=('GET', 'POST'))
    def registration():
        user_login = user()

        if 'id' in session and session['id'] is not None:
            return redirect(url_for('account'))

        else:
            if request.method == 'GET':
                return render_template('registration.html', user_login=user_login)

            if request.method == 'POST':
                login_verification = {'success': False}
                login = request.form['login']
                password_n = request.form['password']
                password = bcrypt.generate_password_hash(password_n)
                surname = request.form['surname']
                name = request.form['name']
                phone_number = request.form['phone_number']
                try:
                    db.create_new_user(db.open_db(db_url), login, password, surname, name, phone_number)
                except sqlite3.IntegrityError:
                    login_verification['error'] = 'Пользователь c таким логином уже существует'
                    flash(login_verification['error'])
                    return render_template('registration.html')
            return redirect(url_for('login'))

    @app.route('/fav/<ad_id>', methods=['GET', 'POST'])
    def fav(ad_id):
        if 'id' in session and session['id'] is not None:
            user = session['id']
            if request.method == 'POST':
                is_favor = db.is_favorites(db.open_db(db_url), ad_id, user)
                empty = []
                if is_favor == empty:
                    db.add_to_favorites(db.open_db(db_url), ad_id, user)
                    favor = 1
                    return redirect(url_for('details', ad_id=ad_id, favor=favor))
                else:
                    for res in is_favor:
                        id = res['id']
                        db.remove_from_favorites(db.open_db(db_url), id)
                        favor = 0
                        return redirect(url_for('details', ad_id=ad_id, favor=favor))
        else:
            return redirect(url_for('login'))

    @app.route('/favourites', methods=('GET', 'POST'))
    def favourites():
        if 'id' in session and session['id'] is not None:
            username = session['id']
            user_login = session['login']
            favorites_ads = db.favorites_for_user(db.open_db(db_url), username)
            counting = db.counting_favorites_for_user(db.open_db(db_url), username)
            counting_favorites = counting['number_favor_ads']

            return render_template('favourites.html', user_id=username, user_login=user_login,
                                   favorites_ads=favorites_ads, counting_favorites=counting_favorites)
        else:
            return redirect(url_for('login'))

    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9879, debug=True)


if __name__ == '__main__':
    start()
