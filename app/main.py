import waitress

from flask import Flask, render_template, request, redirect, url_for, flash

from app import db

import os


def start():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='Marina_secret_key',
    )
    db_url = 'db.sqlite'

    @app.route('/', methods=('GET', 'POST'))
    def all_pets():
        search = request.args.get('search')
        if search:
            search_result = db.search_goods(db.open_db(db_url), search)
            return render_template('index.html', goods=search_result, search=search, active_index='all_pets')
        all_pets_result = db.all_pets(db.open_db(db_url))
        return render_template('index.html', goods=all_pets_result, active_index='all_pets')

    @app.route('/dogs', methods=('GET', 'POST'))
    def dogs():
        dogs_result = db.dogs(db.open_db(db_url))
        return render_template('index.html', goods=dogs_result, active_index='dogs')

    @app.route('/cats', methods=('GET', 'POST'))
    def cats():
        cats_result = db.cats(db.open_db(db_url))
        return render_template('index.html', goods=cats_result, active_index='cats')

    @app.route('/another_pets', methods=('GET', 'POST'))
    def another_pets():
        another_pets_result = db.another_pets(db.open_db(db_url))
        return render_template('index.html', goods=another_pets_result, active_index='another_pets')

    @app.route("/details/<vendor_code>", methods=('GET', 'POST'))
    def details(vendor_code):
        search_by_vendor_code_result = db.search_by_vendor_code(db.open_db(db_url), vendor_code)
        return render_template('details.html', good=search_by_vendor_code_result)

    @app.route('/new_pet', methods=('GET', 'POST'))
    def new_pet():
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
            description = request.form['description']

            db.create_new_pet(db.open_db(db_url), vendor_code, category, breed, gender, birthdate, name, price,
                              description)
            return redirect(url_for('all_pets'))

        return render_template('new_pet.html')

    @app.route("/remove/<vendor_code>", methods=['GET', 'POST'])
    def remove(vendor_code):
        if request.method == 'GET':
            search_by_vendor_code_result = db.search_by_vendor_code(db.open_db(db_url), vendor_code)
            return render_template('remove.html', good=search_by_vendor_code_result)
        if request.method == 'POST':
            db.remove_by_vendor_code(db.open_db(db_url), vendor_code)
            return redirect(url_for('all_pets'))




    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9873, debug=True)


if __name__ == '__main__':
    start()
