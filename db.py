import mysql.connector
from functools import wraps
from totally_unnecessary import db_host, db_user, db_password


def db_connection_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database='poker_star'
        )
        cursor = connection.cursor()
        result = func(*args, **kwargs, db_cursor=cursor)
        connection.commit()
        cursor.close()
        connection.close()
        return result
    return wrapper


@db_connection_decorator
def db_init(user_id, db_cursor=None):
    '''ARGS - user_id'''
    try:
        db_cursor.execute(f'''
            INSERT INTO user_cards (user_id, known_cards) values ({str(user_id)}, '');
            ''')
    except mysql.connector.errors.IntegrityError:
        db_cursor.execute(f'''
                    UPDATE user_cards SET known_cards = '' WHERE user_id = {str(user_id)};
                    ''')


@db_connection_decorator
def db_update_cards(user_id, known_cards, db_cursor=None):
    '''ARGS - user_id, known_cards'''
    db_cursor.execute(f'''
    SELECT known_cards FROM user_cards WHERE user_id = '{user_id}';
    ''')
    db_known_cards = db_cursor.fetchone()
    db_cursor.execute(f'''
    UPDATE user_cards SET known_cards = '{db_known_cards[0]} {known_cards}' WHERE user_id = '{user_id}' ;
    ''')


@db_connection_decorator
def db_clear_cards(user_id, db_cursor=None):
    db_cursor.execute(f'''
    UPDATE user_cards SET known_cards = '' WHERE user_id = '{user_id}';
    ''')


@db_connection_decorator
def db_pull_cards(user_id, db_cursor=None):
    db_cursor.execute(f'''
    SELECT known_cards FROM user_cards WHERE user_id = '{user_id}';
    ''')
    known_cards = db_cursor.fetchone()[0].upper().split()
    result = []
    for card in known_cards:
        if card[-1] == 'Ч':
            result.append((card[0:-1], 'Черва'))
        elif card[-1] == 'Б':
            result.append((card[0:-1], 'Буба'))
        elif card[-1] == 'К':
            result.append((card[0:-1], 'Крести'))
        elif card[-1] == 'П':
            result.append((card[0:-1], 'Пика'))
    return result


