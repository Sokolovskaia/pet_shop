import sqlite3


def open_db(url):
    connection = sqlite3.connect(url)
    connection.row_factory = sqlite3.Row
    return connection


def create_table_pets(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_pets (
            ad_id INTEGER PRIMARY KEY AUTOINCREMENT
          , category TEXT NOT NULL
          , category_lowercased TEXT NOT NULL
          , breed TEXT
          , breed_lowercased TEXT
          , gender TEXT
          , birthdate TEXT
          , name TEXT
          , name_lowercased TEXT
          , price INTEGER NOT NULL
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
        CREATE TABLE IF NOT EXISTS test_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT
          , login TEXT NOT NULL UNIQUE 
          , password TEXT NOT NULL
          , surname TEXT NOT NULL
          , name TEXT NOT NULL
          , phone_number INTEGER NOT NULL
        );
        """)
        connection.commit()


def create_table_favourites(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_favourites (
            id INTEGER PRIMARY KEY AUTOINCREMENT
          , ad INTEGER 
          , user INTEGER
          , FOREIGN KEY (ad) REFERENCES pets (ad_id) ON DELETE CASCADE 
        );
        """)
        connection.commit()

