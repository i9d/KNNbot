import pymysql
# host = 'sql7.freemysqlhosting.net'
# user = 'sql7373867'
# password = 'VTf1x8IBhu'
# port = 3306
# db = 'sql7373867'
host = 'localhost'
user = 'admin'
password = '123456'
port = 3306
db = 'chatdb'
charset = 'utf8mb4'
cursorclass = pymysql.cursors.DictCursor


def select(query, args):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        db=db,
        charset=charset,
        cursorclass=cursorclass
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            result = cursor.fetchone()
    finally:
        connection.close()
    return result


def update(query, args):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        db=db,
        charset=charset,
        cursorclass=cursorclass
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, args)
        connection.commit()
    finally:
        connection.close()