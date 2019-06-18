
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
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            presence INTEGER DEFAULT 0 CHECK (presence IN (1, 0)),
            photo TEXT,
            description TEXT
        );
        """)
        connection.commit()


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


def create_new_pet(connection, vendor_code, category, breed, gender, birthdate, name, price, description ):
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO goods (vendor_code, category, breed, gender, birthdate, name, price, description) 
               VALUES (:vendor_code, :category, :breed, :gender, :birthdate, :name, :price, :description)''',
            {'vendor_code': vendor_code, 'category': category, 'breed': breed, 'gender': gender, 'birthdate': birthdate,
             'name': name, 'price': price, 'description': description})
        connection.commit()

