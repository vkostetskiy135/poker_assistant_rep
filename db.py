import mysql.connector
from functools import wraps
from totally_unnecessary import db_host, db_user, db_password


def db_connection_decorator(func):
    @wraps(func)
    def wrapper(user_id):
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database='poker_star'
        )
        cursor = connection.cursor()
        result = func(user_id, db_cursor=cursor)
        connection.commit()
        cursor.close()
        connection.close()
        return result
    return wrapper

@db_connection_decorator
def user_known_cards(user_id, db_cursor=None):
    pass

