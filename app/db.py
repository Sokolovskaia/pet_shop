
import sqlite3


def open_db(url):
    connection = sqlite3.connect(url)
    connection.row_factory = sqlite3.Row
    return connection


def create_table_goods(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS goods (
            vendor_code INTEGER PRIMARY KEY,
            category TEXT NOT NULL,
            breed TEXT,
            gender TEXT,
            birthdate NUMERIC,
            name TEXT,
            price INTEGER NOT NULL,
            presence INTEGER DEFAULT 0 CHECK (presence IN (1, 0)),
            photo TEXT DEFAULT '7.jpg',
            description TEXT,
            author_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES users (id)
        );
        """)
        connection.commit()


def create_table_users(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT
          , login TEXT NOT NULL UNIQUE 
          , password TEXT NOT NULL
          , surname TEXT NOT NULL
          , name TEXT NOT NULL
          , phone_number INTEGER NOT NULL UNIQUE 
        );
        """)
        connection.commit()


def validate_user(connection, login, password):
    with connection:
        cursor = connection.cursor()
        result = {'success': False}
        user = cursor.execute('SELECT * FROM users WHERE login = :login', {'login': login}).fetchone()

        if user is None:
            result['error'] = 'Пользователь не найден'
        elif not user['password'] == password:
            result['error'] = 'Неверный пароль'
        else:
            result['id'] = user['id']
            result['login'] = user['login']
            result['surname'] = user['surname']
            result['name'] = user['name']
            result['phone_number'] = user['phone_number']
            result['success'] = True

        return result




def get_all(connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * FROM goods LIMIT 20""").fetchall()
        return result

def all_pets(connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * FROM goods WHERE category IN ('Собака', 'Кошка', 'Хомяк') LIMIT 20""").fetchall()
        return result


def dogs(connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * FROM goods WHERE category =='Собака' LIMIT 20""").fetchall()
        return result


def cats(connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * FROM goods WHERE category =='Кошка' LIMIT 20""").fetchall()
        return result

def another_pets(connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * FROM goods WHERE category NOT IN ('Собака', 'Кошка') LIMIT 20""").fetchall()
        return result


def search_by_vendor_code(connection, vendor_code):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""SELECT * 
                 FROM goods 
                WHERE vendor_code = :vendor_code""",
            {'vendor_code': vendor_code}).fetchone()
        return result


def search_goods(connection, search):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT *
          FROM goods
         WHERE :search=vendor_code OR :search=breed OR :search=category OR :search=name LIMIT 20""", {'search': search}).fetchall()
        return result


def create_new_pet(connection, vendor_code, category, breed, gender, birthdate, name, price, photo, description, author_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO goods (vendor_code, category, breed, gender, birthdate, name, price, photo, description, author_id) 
               VALUES (:vendor_code, :category, :breed, :gender, :birthdate, :name, :price, :photo, :description, :author_id)''',
            {'vendor_code': vendor_code, 'category': category, 'breed': breed, 'gender': gender, 'birthdate': birthdate,
             'name': name, 'price': price, 'photo': photo, 'description': description, 'author_id': author_id})
        connection.commit()

def remove_by_vendor_code(connection, vendor_code):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM goods
              WHERE vendor_code = :vendor_code
        """, {'vendor_code': vendor_code})
        connection.commit()


def edit_by_vendor_code(connection, vendor_code, category, breed, gender, birthdate, name, price, description):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE goods 
           SET category = :category
             , breed = :breed
             , gender = :gender
             , birthdate = :birthdate
             , name = :name
             , price = :price
             , description = :description
         WHERE vendor_code = :vendor_code
        """, {'vendor_code': vendor_code, 'category': category, 'breed': breed, 'gender': gender, 'birthdate': birthdate,
             'name': name, 'price': price, 'description': description})
        connection.commit()

def all_ads_for_user(connection, username):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * FROM goods WHERE author_id = :username LIMIT 20""", {'username': username}).fetchall()
        return result
