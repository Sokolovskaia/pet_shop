
import sqlite3


def open_db(url):
    connection = sqlite3.connect(url)
    connection.row_factory = sqlite3.Row
    return connection


def create_table_pets(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            vendor_code INTEGER PRIMARY KEY
          , category TEXT NOT NULL
          , breed TEXT
          , gender TEXT
          , birthdate NUMERIC
          , name TEXT
          , price INTEGER NOT NULL
          , presence INTEGER DEFAULT 0 CHECK (presence IN (1, 0))
          , photo TEXT
          , description TEXT
          , author_id INTEGER NOT NULL
          , FOREIGN KEY (author_id) REFERENCES users (id)
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
          , phone_number INTEGER NOT NULL
        );
        """)
        connection.commit()


def validate_user(connection, login, password):
    with connection:
        cursor = connection.cursor()
        result = {'success': False}
        user = cursor.execute("""
            SELECT * 
              FROM users 
             WHERE login = :login""", {'login': login}).fetchone()

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
        SELECT * 
          FROM pets 
         LIMIT 20""").fetchall()
        return result

def all_pets(connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * 
          FROM pets 
         WHERE category IN ('Собака', 'Кошка', 'Хомяк') 
         LIMIT 20""").fetchall()
        return result


def dogs(connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * 
          FROM pets 
         WHERE category =='Собака' 
         LIMIT 20""").fetchall()
        return result


def cats(connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * 
          FROM pets 
         WHERE category =='Кошка' 
         LIMIT 20""").fetchall()
        return result

def another_pets(connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * 
          FROM pets 
         WHERE category NOT IN ('Собака', 'Кошка') 
         LIMIT 20""").fetchall()
        return result


def search_by_vendor_code(connection, vendor_code):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT p.vendor_code
             , p.category
             , p.breed
             , p.gender
             , p.birthdate
             , p.name
             , p.price
             , p.photo
             , p.description
             , p.author_id
             , u.surname
             , u.name author_name
             , u.phone_number
          FROM pets p 
     LEFT JOIN users u 
            ON p.author_id = u.id
         WHERE p.vendor_code = :vendor_code""", {'vendor_code': vendor_code}).fetchone()
        return result


def search_pets(connection, search):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT *
          FROM pets
         WHERE :search=vendor_code 
            OR :search=breed 
            OR :search=category 
            OR :search=name 
         LIMIT 20""", {'search': search}).fetchall()
        return result


def create_new_pet(connection, vendor_code, category, breed, gender, birthdate, name, price, photo, description, author_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO pets (
              vendor_code
            , category
            , breed
            , gender
            , birthdate
            , name
            , price
            , photo
            , description
            , author_id) 
               VALUES (
                 :vendor_code
               , :category
               , :breed
               , :gender
               , :birthdate
               , :name
               , :price
               , :photo
               , :description
               , :author_id)''',
            {'vendor_code': vendor_code, 'category': category, 'breed': breed, 'gender': gender, 'birthdate': birthdate,
             'name': name, 'price': price, 'photo': photo, 'description': description, 'author_id': author_id})
        connection.commit()

def remove_by_vendor_code(connection, vendor_code):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM pets
              WHERE vendor_code = :vendor_code
        """, {'vendor_code': vendor_code})
        connection.commit()


def edit_by_vendor_code(connection, vendor_code, category, breed, gender, birthdate, name, price, photo, description):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE pets 
           SET category = :category
             , breed = :breed
             , gender = :gender
             , birthdate = :birthdate
             , name = :name
             , price = :price
             , photo = :photo
             , description = :description
         WHERE vendor_code = :vendor_code
        """, {'vendor_code': vendor_code, 'category': category, 'breed': breed, 'gender': gender, 'birthdate': birthdate,
             'name': name, 'price': price, 'photo': photo, 'description': description})
        connection.commit()

def all_ads_for_user(connection, username):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * 
          FROM pets 
         WHERE author_id = :username 
         LIMIT 20""", {'username': username}).fetchall()
        return result

def number_of_ads(connection, username):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
           SELECT COUNT(vendor_code) ads
             FROM pets 
            WHERE author_id = :username""", {'username': username}).fetchone()
        return result


def create_new_user(connection, login, password, surname, name, phone_number):
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO users (
              login
            , password
            , surname
            , name
            , phone_number
           ) 
               VALUES (
                 :login
               , :password
               , :surname
               , :name
               , :phone_number)''',
            {'login': login, 'password': password, 'surname': surname, 'name': name, 'phone_number': phone_number})
        connection.commit()

