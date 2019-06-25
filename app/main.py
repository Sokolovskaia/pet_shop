import sqlite3

import waitress

from flask import Flask, render_template, request, redirect, url_for, session, flash

from app import db

import os

from werkzeug.utils import secure_filename


from app.db import validate_user, validate_registration

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

        return render_template('login.html')

    @app.route('/account', methods=('GET', 'POST'))
    def account():
        username = session['id']
        user_login = session['login']
        user_surname = session['surname']
        user_name = session['name']
        user_phone_number = session['phone_number']
        ads_for_user = db.all_ads_for_user(db.open_db(db_url), username)
        number_of_ads_for_user = db.number_of_ads(db.open_db(db_url), username)
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
            return render_template('index.html', pets=search_result, search=search, active_index='all_pets')
        all_pets_result = db.all_pets(db.open_db(db_url))
        return render_template('index.html', pets=all_pets_result, active_index='all_pets', user_login=user_login)

    @app.route('/dogs', methods=('GET', 'POST'))
    def dogs():
        dogs_result = db.dogs(db.open_db(db_url))
        return render_template('index.html', pets=dogs_result, active_index='dogs')

    @app.route('/cats', methods=('GET', 'POST'))
    def cats():
        cats_result = db.cats(db.open_db(db_url))
        return render_template('index.html', pets=cats_result, active_index='cats')

    @app.route('/another_pets', methods=('GET', 'POST'))
    def another_pets():
        another_pets_result = db.another_pets(db.open_db(db_url))
        return render_template('index.html', pets=another_pets_result, active_index='another_pets')

    @app.route("/details/<vendor_code>", methods=('GET', 'POST'))
    def details(vendor_code):
        search_by_vendor_code_result = db.search_by_vendor_code(db.open_db(db_url), vendor_code)
        return render_template('details.html', pet=search_by_vendor_code_result)

    @app.route('/new_pet', methods=('GET', 'POST'))
    def new_pet():
        if 'id' in session and session['id'] is not None:
            if request.method == 'GET':
                return render_template('new_pet.html')

            if request.method == 'POST':

                vendor_code = request.form['vendor_code']
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
                db.create_new_pet(db.open_db(db_url), vendor_code, category, breed, gender, birthdate, name, price, photo,
                                  description, author_id)
                return redirect(url_for('all_pets'))

            return render_template('new_pet.html')

        else:
            return redirect(url_for('login'))





    @app.route("/remove/<vendor_code>", methods=['GET', 'POST'])
    def remove(vendor_code):
        if request.method == 'GET':
            search_by_vendor_code_result = db.search_by_vendor_code(db.open_db(db_url), vendor_code)
            return render_template('remove.html', pet=search_by_vendor_code_result)
        if request.method == 'POST':
            db.remove_by_vendor_code(db.open_db(db_url), vendor_code)
            return redirect(url_for('all_pets'))

    @app.route("/edit/<vendor_code>", methods=['GET', 'POST'])
    def edit(vendor_code):
        if request.method == 'GET':
            search_by_vendor_code_result = db.search_by_vendor_code(db.open_db(db_url), vendor_code)
            return render_template('edit.html', pet=search_by_vendor_code_result)

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
            db.edit_by_vendor_code(db.open_db(db_url), vendor_code, category, breed, gender, birthdate, name, price, photo,
                                   description)
            return redirect(url_for('all_pets', vendor_code=vendor_code))

    @app.route('/about', methods=('GET', 'POST'))
    def about():
        return render_template('about.html')


    @app.route('/error', methods=('GET', 'POST'))
    def error():
        return render_template('error.html')


    @app.route('/registration', methods=('GET', 'POST'))
    def registration():
        if 'id' in session and session['id'] is not None:

            return redirect(url_for('account'))

        else:
            if request.method == 'GET':
                return render_template('registration.html')

            if request.method == 'POST':
                login = request.form['login']
                password = request.form['password']
                surname = request.form['surname']
                name = request.form['name']
                phone_number = request.form['phone_number']
                try:
                   db.create_new_user(db.open_db(db_url), login, password, surname, name, phone_number)
                except sqlite3.IntegrityError:
                    return redirect(url_for('error'))


            return redirect(url_for('login'))



    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9873, debug=True)


if __name__ == '__main__':
    start()
