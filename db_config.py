import pymysql


def insert(message):
    connection = pymysql.connect(
        host='sql7.freemysqlhosting.net',
        user='sql7373867',
        password='VTf1x8IBhu',
        port=3306,
        db='sql7373867',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            _insert = """
                  INSERT
                  INTO
                  `MAIN`(`TELEGRAM_ID`, `NAME`, `WARN`, `IS_BANNED`, `POINT`)
                  VALUES(%s, %s, %s, %s, %s)
                  """
            cursor.execute(_insert, (message.from_user.id, message.from_user.username, 0, 0, 100))
        connection.commit()

    finally:
        connection.close()


def select(path):
    connection = pymysql.connect(
        host='sql7.freemysqlhosting.net',
        user='sql7373867',
        password='VTf1x8IBhu',
        port=3306,
        db='sql7373867',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            _select = path #"SELECT * FROM `MAIN`"
            cursor.execute(_select)
            result = cursor.fetchone()
    finally:
        connection.close()
    return result
