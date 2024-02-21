import csv
import os
import sys
import sqlite3
import datetime as dt
import logging


TABLES_NAME = {
    'category': 'titles_category',
    'genre': 'titles_genre',
    'review': 'reviews_review',
    'comments': 'reviews_comments',
    'titles': 'titles_title',
    'genre_title': 'titles_genretitle',
    'users': 'users_user',
}

FILES_NAME = {
    'category': 'category.csv',
    'genre': 'genre.csv',
    'review': 'review.csv',
    'comments': 'comments.csv',
    'titles': 'titles.csv',
    'genre_title': 'genre_title.csv',
    'users': 'users.csv',
}
SCHEMA_NAME = {
    'category': 'id,name,slug',
    'genre': 'id,name,slug',
    'review': 'id,text,score,pub_date,author_id,title_id',
    'comments': 'id,text,pub_date,author_id,review_id',
    'titles': 'id,name,year,description,category_id',
    'genre_title': 'id,title_id,genre_id',
    'users': (
        'id,'
        'password,'
        'last_login,'
        'is_superuser,'
        'username,'
        'first_name,'
        'last_name,'
        'role,'
        'bio,'
        'email,'
        'confirmation_code,'
        'is_staff,'
        'is_active,'
        'created_at,'
        'updated_at,'
        'date_joined'
    )
}


def insert_multiple_records(records, schema, table):
    values = ','.join(['?' for i in range(len(schema.split(',')))])
    try:
        sqlite_connection = sqlite3.connect('db.sqlite3')
        cursor = sqlite_connection.cursor()
        logging.debug('Подключен к SQLite')

        sqlite_insert_query = (
            f'INSERT INTO {table} ({schema}) VALUES ({values});'
        )

        cursor.executemany(sqlite_insert_query, records)
        sqlite_connection.commit()
        logging.info(
            (
                f'В таблицу {table} '
                f'успешно вставленых записей - {cursor.rowcount}'
            )
        )
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        logging.error(f'Ошибка при работе с SQLite {error}')
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            logging.debug("Соединение с SQLite закрыто")


def read_file(filename):
    with open(filename, 'r', encoding="utf8") as f:
        reader = csv.DictReader(f, delimiter=",")
        header = [i for i in reader]
    return header


def prep_category(data):
    """id,name,slug"""
    result = []
    for i in data:
        result.append(
            (
                i['id'],
                i['name'],
                i['slug']
            )
        )
    return result


def prep_genre(data):
    """id,name,slug"""
    result = []
    for i in data:
        result.append(
            (
                i['id'],
                i['name'],
                i['slug']
            )
        )
    return result


def prep_reviews(data):
    """id,text,score,pub_date,author_id,title_id"""
    result = []
    for i in data:
        result.append(
            (
                i['id'],
                i['text'],
                i['score'],
                i['pub_date'],
                i['author'],
                i['title_id']
            )
        )
    return result


def prep_genre_title(data):
    """id,title_id,genre_id"""
    result = []
    for i in data:
        result.append(
            (
                i['id'],
                i['title_id'],
                i['genre_id']
            )
        )
    return result


def prep_titles(data):
    """id,name,year,description,category_id"""
    result = []
    for i in data:
        result.append(
            (
                i['id'],
                i['name'],
                i['year'],
                '',
                i['category'],
            )
        )
    return result


def prep_comments(data):
    """id,text,pub_date,author_id,review_id"""
    result = []
    for i in data:
        result.append(
            (
                i['id'],
                i['text'],
                i['pub_date'],
                i['author'],
                i['review_id'],
            )
        )
    return result


def prep_users(data):
    """
        'id,'
        'password,'
        'last_login,'
        'is_superuser,'
        'username,'
        'first_name,'
        'last_name,'
        'role,'
        'bio,'
        'email,'
        'confirmation_code,'
        'is_staff,'
        'is_active,'
        'created_at,'
        'updated_at,'
        'date_joined'
    """
    result = []
    datetime_stamp = dt.datetime.now().isoformat()
    for i in data:
        result.append(
            (
                i['id'],
                '',
                datetime_stamp,
                False,
                i['username'],
                i['first_name'],
                i['last_name'],
                i['role'],
                i['bio'],
                i['email'],
                '',
                False,
                True,
                datetime_stamp,
                datetime_stamp,
                datetime_stamp
            )
        )
    return result


def main():

    logging.info('Запуск импорта.')

    for steps, steps_fn in LOAD_STEPS.items():
        prep_file = steps_fn(
            read_file(
                os.path.join(
                    BASE_DIR, FILES_NAME[steps]
                )
            )
        )
        insert_multiple_records(
            prep_file, SCHEMA_NAME[steps],
            TABLES_NAME[steps]
        )

    logging.info('Импорт завершен.')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

    logging.debug(sys.argv)

    if len(sys.argv) < 2:
        raise ValueError('Не задана папка ждя загрузки файлов.')

    BASE_DIR = sys.argv[1]

    logging.debug(BASE_DIR)

    LOAD_STEPS = {
        'category': prep_category,
        'genre': prep_genre,
        'genre_title': prep_genre_title,
        'titles': prep_titles,
        'review': prep_reviews,
        'comments': prep_comments,
        'users': prep_users,
    }
    main()
