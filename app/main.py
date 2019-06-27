import sqlite3

import waitress

from flask import Flask, render_template, request, redirect, url_for, session, flash

from app import db

import os

import math

from werkzeug.utils import secure_filename


from app.db import validate_user

UPLOAD_FOLDER = 'app/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def start():
    app = Flask(__name__)
    app.config['uploads'] = UPLOAD_FOLDER

    app.config.from_mapping(
        SECRET_KEY='Marina_secret_key',
    )
    db_url = 'db.sqlite'

    @app.route('/login', methods=('GET', 'POST'))
    def login():
        search = request.args.get('search')
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
        else:
            user_login = 0

        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets',
                                   user_login=user_login)

        if request.method == 'POST':
            login = request.form['login']
            password = request.form['password']
            val = validate_user(db.open_db(db_url), login, password)

            if val['success']:
                session.clear()
                session['id'] = val['id']
                session['login'] = val['login']
                session['surname'] = val['surname']
                session['name'] = val['name']
                session['phone_number'] = val['phone_number']

                return redirect(url_for('account', username=session['id']))

            flash(val['error'])

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

        search = request.args.get('search')
        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets',
                                   user_login=user_login)

        return render_template('account.html', ads_for_user=ads_for_user, number_of_ads_for_user=number_of_ads_for_user, user_id=username, user_login=user_login, user_surname=user_surname,
                           user_name=user_name, user_phone_number=user_phone_number, active_index='account')

    @app.route('/', methods=('GET', 'POST'))
    def all_pets():
        search = request.args.get('search')
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
        else:
            user_login = 0

        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets', user_login=user_login)
        all_pets_result = db.all_pets(db.open_db(db_url))

        return render_template('index.html', pets=all_pets_result, active_index='all_pets', user_login=user_login)

    @app.route('/dogs', methods=('GET', 'POST'))
    def dogs():
        search = request.args.get('search')
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
        else:
            user_login = 0

        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets', user_login=user_login)
        dogs_result = db.dogs(db.open_db(db_url))
        return render_template('index.html', pets=dogs_result, active_index='dogs', user_login=user_login)

    @app.route('/cats', methods=('GET', 'POST'))
    def cats():
        search = request.args.get('search')
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
        else:
            user_login = 0

        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets', user_login=user_login)
        cats_result = db.cats(db.open_db(db_url))
        return render_template('index.html', pets=cats_result, active_index='cats', user_login=user_login)

    @app.route('/another_pets', methods=('GET', 'POST'))
    def another_pets():
        search = request.args.get('search')
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
        else:
            user_login = 0

        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets', user_login=user_login)
        another_pets_result = db.another_pets(db.open_db(db_url))
        return render_template('index.html', pets=another_pets_result, active_index='another_pets', user_login=user_login)

    @app.route("/details/<ad_id>", methods=('GET', 'POST'))
    def details(ad_id):
        favor = -1
        counting_favor = db.counting_favorites(db.open_db(db_url), ad_id)
        search = request.args.get('search')
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

        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets', user_login=user_login)
        search_by_ad_id_result = db.search_by_ad_id(db.open_db(db_url), ad_id)

        return render_template('details.html', pet=search_by_ad_id_result, user_login=user_login, favor=favor, counting_favor=counting_favor)

    @app.route('/new_pet', methods=('GET', 'POST'))
    def new_pet():
        search = request.args.get('search')
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
        else:
            user_login = 0

        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets', user_login=user_login)

        if 'id' in session and session['id'] is not None:
            if request.method == 'GET':
                return render_template('new_pet.html', user_login=user_login)

            if request.method == 'POST':
                category = request.form['category']
                breed = request.form['breed']
                gender = request.form['gender']
                birthdate = request.form['birthdate']
                name = request.form['name']
                price = int(request.form['price'])
                file = request.files['file']
                if file and allowed_file(file.filename):
                    photo = secure_filename(file.filename)
                    file.save(os.path.join(app.config['uploads'], photo))
                description = request.form['description']
                author_id = session['id']
                db.create_new_pet(db.open_db(db_url), category, breed, gender, birthdate, name, price, photo,
                                  description, author_id)
                return redirect(url_for('all_pets'))

            return render_template('new_pet.html')

        else:
            return redirect(url_for('login'))

    @app.route("/remove/<ad_id>", methods=['GET', 'POST'])
    def remove(ad_id):
        search = request.args.get('search')
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
        else:
            user_login = 0

        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets',
                                   user_login=user_login)

        if request.method == 'GET':
            search_by_ad_id_result = db.search_by_ad_id(db.open_db(db_url), ad_id)
            return render_template('remove.html', pet=search_by_ad_id_result, user_login=user_login)
        if request.method == 'POST':
            db.remove_by_ad_id(db.open_db(db_url), ad_id)
            return redirect(url_for('all_pets'))

    @app.route("/edit/<ad_id>", methods=['GET', 'POST'])
    def edit(ad_id):
        search = request.args.get('search')
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
        else:
            user_login = 0

        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets', user_login=user_login)

        if request.method == 'GET':
            search_by_ad_id_result = db.search_by_ad_id(db.open_db(db_url), ad_id)
            return render_template('edit.html', pet=search_by_ad_id_result, user_login=user_login)

        if request.method == 'POST':
            category = request.form['category']
            breed = request.form['breed']
            gender = request.form['gender']
            birthdate = request.form['birthdate']
            name = request.form['name']
            price = int(request.form['price'])
            file = request.files['file']
            if file and allowed_file(file.filename):
                photo = secure_filename(file.filename)
                file.save(os.path.join(app.config['uploads'], photo))
            description = request.form['description']
            db.edit_by_ad_id(db.open_db(db_url), ad_id, category, breed, gender, birthdate, name, price, photo,
                                   description)
            return redirect(url_for('all_pets', ad_id=ad_id))

    @app.route('/about', methods=('GET', 'POST'))
    def about():
        search = request.args.get('search')
        if 'id' in session and session['id'] is not None:
            user_login = session['login']
        else:
            user_login = 0

        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets',
                                   user_login=user_login)

        return render_template('about.html', user_login=user_login)

    @app.route('/registration', methods=('GET', 'POST'))
    def registration():
        search = request.args.get('search')
        user_login = 0
        if search:
            search_result = db.search_pets(db.open_db(db_url), search)
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets',
                                   user_login=user_login)

        if 'id' in session and session['id'] is not None:
            return redirect(url_for('account'))

        else:
            if request.method == 'GET':
                return render_template('registration.html', user_login=user_login)

            if request.method == 'POST':
                login_verification = {'success': False}
                login = request.form['login']
                password = request.form['password']
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

    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9873, debug=True)


if __name__ == '__main__':
    start()
