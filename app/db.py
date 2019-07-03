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


def create_table_favourites(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS favourites (
            id INTEGER PRIMARY KEY AUTOINCREMENT
          , ad INTEGER 
          , user INTEGER
          , FOREIGN KEY (ad) REFERENCES pets(ad_id) ON DELETE CASCADE 
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


def all_ads_count(connection, category=None):
    with connection:
        cursor = connection.cursor()
        if category and category != 'Прочие':
            result = cursor.execute("""
            SELECT COUNT(ad_id) count_ads
            FROM pets
            WHERE category == :category""", {'category': category}).fetchone()
        elif category == 'Прочие':
            result = cursor.execute("""
            SELECT COUNT(ad_id) count_ads
            FROM pets
            WHERE category NOT IN ('Кошка', 'Собака')""").fetchone()
        else:
            result = cursor.execute("""
            SELECT COUNT(ad_id) count_ads
            FROM pets""").fetchone()
        return result


def all_ads_count_search(connection, search):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
                    SELECT COUNT(ad_id) count_ads
                    FROM pets
                    WHERE :search=ad_id 
                    OR :search=breed 
                    OR :search=category 
                    OR :search=name """, {'search': search}).fetchone()
        return result


def all_pets(connection, ads_on_page, pages_offset, category=None):
    with connection:
        cursor = connection.cursor()
        if category and category != 'Прочие':
            result = cursor.execute("""
            SELECT * 
              FROM pets
             WHERE category == :category
          ORDER BY ad_id 
             LIMIT :ads_on_page
            OFFSET :pages_offset""", {'ads_on_page': ads_on_page, 'pages_offset': pages_offset,
                                      'category': category}).fetchall()
        elif category == 'Прочие':
            result = cursor.execute("""
            SELECT * 
              FROM pets 
             WHERE category NOT IN ('Собака', 'Кошка') 
          ORDER BY ad_id 
             LIMIT :ads_on_page
            OFFSET :pages_offset""", {'ads_on_page': ads_on_page, 'pages_offset': pages_offset}).fetchall()
        else:
            result = cursor.execute("""
              SELECT * 
                FROM pets
            ORDER BY ad_id 
               LIMIT :ads_on_page
               OFFSET :pages_offset""", {'ads_on_page': ads_on_page, 'pages_offset': pages_offset}).fetchall()

        return result


def search_by_ad_id(connection, ad_id):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT p.ad_id
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
         WHERE p.ad_id = :ad_id""", {'ad_id': ad_id}).fetchone()
        return result


def search_pets(connection, search, ads_on_page, pages_offset):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT *
          FROM pets
         WHERE :search=ad_id 
            OR :search=breed_lowercased 
            OR :search=category_lowercased
            OR :search=name_lowercased 
         ORDER BY ad_id 
         LIMIT :ads_on_page
        OFFSET :pages_offset""",
                                {'search': search, 'ads_on_page': ads_on_page, 'pages_offset': pages_offset}).fetchall()
        return result


def create_new_pet(connection, category, category_lowercased, breed, breed_lowercased, gender, birthdate, name,
                   name_lowercased, price, photo, description, author_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO pets (
              category
            , category_lowercased
            , breed
            , breed_lowercased
            , gender
            , birthdate
            , name
            , name_lowercased
            , price
            , photo
            , description
            , author_id) 
               VALUES (
                 :category
               , :category_lowercased
               , :breed
               , :breed_lowercased
               , :gender
               , :birthdate
               , :name
               , :name_lowercased
               , :price
               , :photo
               , :description
               , :author_id)''',
            {'category': category, 'category_lowercased': category_lowercased, 'breed': breed,
             'breed_lowercased': breed_lowercased, 'gender': gender, 'birthdate': birthdate,
             'name': name, 'name_lowercased': name_lowercased, 'price': price, 'photo': photo,
             'description': description, 'author_id': author_id})
        connection.commit()


def remove_by_ad_id(connection, ad_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM pets
              WHERE ad_id = :ad_id
        """, {'ad_id': ad_id})
        connection.commit()


def edit_by_ad_id(connection, ad_id, category, category_lowercased, breed, breed_lowercased, gender, birthdate, name, name_lowercased, price, photo, description):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE pets 
           SET category = :category
             , category_lowercased = :category_lowercased
             , breed = :breed
             , breed_lowercased = :breed_lowercased
             , gender = :gender
             , birthdate = :birthdate
             , name = :name
             , name_lowercased = :name_lowercased
             , price = :price
             , photo = :photo
             , description = :description
         WHERE ad_id = :ad_id
        """, {'ad_id': ad_id, 'category': category, 'category_lowercased': category_lowercased, 'breed': breed, 'breed_lowercased': breed_lowercased, 'gender': gender, 'birthdate': birthdate,
              'name': name, 'name_lowercased': name_lowercased, 'price': price, 'photo': photo, 'description': description})
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
           SELECT COUNT(ad_id) ads
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


def add_to_favorites(connection, ad, user):
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO favourites (
              ad
            , user
            ) 
               VALUES (
                 :ad
               , :user);''',
            {'ad': ad, 'user': user})
        connection.commit()


def is_favorites(connection, ad, user):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
        SELECT * 
          FROM favourites 
         WHERE :ad = ad 
         AND   :user = user""", {'ad': ad, 'user': user}).fetchall()
        return result


def remove_from_favorites(connection, id):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM favourites
              WHERE id = :id
        """, {'id': id})
        connection.commit()


def counting_favorites(connection, ad):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
       SELECT ad, COUNT(user) number_users
         FROM favourites
         WHERE ad = :ad
     GROUP BY ad""", {'ad': ad}).fetchone()
        return result


def favorites_for_user(connection, user_id):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
       SELECT p.ad_id
            , p.category
            , p.breed
            , p.name
            , p.price
            , p.photo
         FROM pets p
    LEFT JOIN favourites f 
           ON p.ad_id = f.ad
        WHERE f.user = :user_id
     ORDER BY f.id
       """, {'user_id': user_id}).fetchall()
        return result


def counting_favorites_for_user(connection, user_id):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("""
       SELECT COUNT(id) number_favor_ads
         FROM favourites
         WHERE user = :user_id""", {'user_id': user_id}).fetchone()
        return result
