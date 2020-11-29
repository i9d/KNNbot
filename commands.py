import db
from datetime import datetime


def register(message):
    userID = message.from_user.id
    name = message.text.replace('/reg ', '')
    s = ".,:;!_*-+()/#%&"
    for char in s:
        if char in name:
            result = "В имени есть недопустимые символы. Используйте только латиницу, кириллицу и знак пробела"
            return result
    if not isExistID(userID):
        if not isExistName(name):
            _date = datetime.today().strftime('%Y-%m-%d')
            query = "INSERT INTO `MAIN`(`TELEGRAM_ID`, `NAME`, `Created`, `LastOffense`) VALUES(%s, %s, %s, %s)"
            db.update(query, (userID, name, _date, _date))
            result = "Вы зарегистрированы как " + name
        else:
            result = "Имя " + name + " уже занято"
    else:
        result = "Вы уже зарегистрированы."
    return result


def isExistID(data):
    query = "SELECT EXISTS(SELECT * FROM `main` WHERE `TELEGRAM_ID` = %s)"
    _isExist = "EXISTS(SELECT * FROM `main` WHERE `TELEGRAM_ID` = " + str(data) + ")"
    result = db.select(query, data)
    return result[_isExist]


def isExistName(data):
    query = "SELECT EXISTS(SELECT * FROM `main` WHERE `NAME` = %s)"
    _isExist = "EXISTS(SELECT * FROM `main` WHERE `NAME` = '" + str(data) + "')"
    print(_isExist)
    result = db.select(query, data)
    print(result)
    print(result[_isExist])
    return result[_isExist]


def isGOD(userID):
    query = "SELECT `isGOD` FROM `main` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, userID)
    return result['isGOD']


def isKicked(userID):
    query = "SELECT `isKicked` FROM `main` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, userID)
    return result['isKicked']


def isRole(userID, role):
    query = "SELECT %s FROM `main` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, (role, userID))
    return result[role]


def setPoint(message):
    if isGOD(message.from_user.id):
        if hasattr(message.reply_to_message, 'from_user'):
            userID = str(message.reply_to_message.from_user.id)
            value = message.text.replace('/setpoint', '')
            if ' ' in value:
                value = value.replace(' ', '')
            else:
                result = 'Вы не ввели значение'
                return result
        else:
            text = message.text.replace('/setpoint', '').split()
            if len(text) == 2:
                userID = str(text[0])
                value = str(text[1])
            else:
                result = 'Неправильно введена команда. Используйте /setpoint [id] ' \
                         '[количество] или /setpoint [количество] в ответ на сообщение'
                return result
        if int(value) < 0 or int(value) > 140:
            result = 'Неверное значение. Доступные значения: [0..140]'
            return result
        if isExistID(int(userID)):
            query = "UPDATE `main` SET `POINT` = %s WHERE TELEGRAM_ID = %s"
            db.update(query, (value, userID))
            result = 'Установлено количество поинтов для ' + userID + ': ' + value
        else:
            result = 'Пользователь не найден'
    else:
        result = 'Недостаточно прав'
    return result


def getPoint(userID):
    query = "SELECT `POINT` FROM `main` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, userID)
    return result['POINT']


def deleteUser(message):
    if isGOD(message.from_user.id):
        if hasattr(message.reply_to_message, 'from_user'):
            userID = message.reply_to_message.from_user.id
        else:
            userID = message.text.replace('/del ', '').split()
        if isExistID(userID):
            if message.from_user.id == userID:
                result = 'Самоуничтожение невозможно'
            else:
                query = "DELETE FROM `main` WHERE `TELEGRAM_ID` = %s"
                db.update(query, userID)
                result = 'Пользователь удален'
        else:
            result = 'Пользователь не найден'
    else:
        result = 'Недостаточно прав'
    return result


def changePoints(message):
    query = "SELECT `POINT` FROM `main` WHERE `TELEGRAM_ID` = %s"
    userID = message.from_user.id
    points = db.select(query, userID)
    if points['POINT'] < 5:
        query = "UPDATE `main` SET `isKicked` = %s WHERE TELEGRAM_ID = %s"
        db.update(query, (1, userID))
    else:
        query = "UPDATE `main` SET `POINT` = %s WHERE TELEGRAM_ID = %s"
        db.update(query, (points['POINT'] - 5, userID))


def updateLastOffense(message):
    userID = message.from_user.id
    query = "UPDATE `main` SET `LastOffense` = %s WHERE TELEGRAM_ID = %s"
    db.update(query, (datetime.today().strftime('%Y-%m-%d'), userID))


def info(message):
    if hasattr(message.reply_to_message, 'from_user'):
        if isGOD(message.from_user.id):
            userID = message.reply_to_message.from_user.id
        else:
            result = 'Вы не можете просмотреть информацию о другом пользователе'
            return result
    else:
        userID = message.from_user.id
    if isExistID(userID):
        query = "SELECT * FROM `MAIN` WHERE `TELEGRAM_ID` = %s"
        data = db.select(query, userID)
        result = \
            'Телеграм ID: ' + str(data['TELEGRAM_ID']) + \
            '\nИмя: ' + data['NAME'] +  \
            '\nПоинты: ' + str(data['POINT']) + \
            '\nДата регистрации: ' + str(data['Created'])
    else:
        result = 'Пользователь не зарегистрирован'
    return result


def canKick(message):
    if hasattr(message.reply_to_message, 'from_user'):
        userID = message.reply_to_message.from_user.id
    else:
        result = 'Вы должны отправить команду ответом на сообщение'
        return result
    query = "SELECT `RoleKick` FROM `main` WHERE `TELEGRAM_ID` = %s"
    data = db.select(query, userID)
    role = data['RoleKick']
    if role:
        query = "UPDATE `main` SET `RoleKick` = 0 WHERE TELEGRAM_ID = %s"
        db.update(query, userID)
        result = 'Пользователь больше не может кикать'
    else:
        query = "UPDATE `main` SET `RoleKick` = 1 WHERE TELEGRAM_ID = %s"
        db.update(query, userID)
        result = 'Пользователь теперь может кикать'
    return result


def canBanMedia(message):
    if hasattr(message.reply_to_message, 'from_user'):
        userID = message.reply_to_message.from_user.id
    else:
        result = 'Вы должны отправить команду ответом на сообщение'
        return result
    query = "SELECT `RoleBanMedia` FROM `main` WHERE `TELEGRAM_ID` = %s"
    data = db.select(query, userID)
    role = data['RoleBanMedia']
    if role:
        query = "UPDATE `main` SET `RoleBanMedia` = 0 WHERE TELEGRAM_ID = %s"
        db.update(query, userID)
        result = 'Пользователь больше не может запрещать медиа'
    else:
        query = "UPDATE `main` SET `RoleBanMedia` = 1 WHERE TELEGRAM_ID = %s"
        db.update(query, userID)
        result = 'Пользователь теперь может запрещать медиа'
    return result


def canReadOnly(message):
    if hasattr(message.reply_to_message, 'from_user'):
        userID = message.reply_to_message.from_user.id
    else:
        result = 'Вы должны отправить команду ответом на сообщение'
        return result
    query = "SELECT `RoleReadOnly` FROM `main` WHERE `TELEGRAM_ID` = %s"
    data = db.select(query, userID)
    role = data['RoleReadOnly']
    if role:
        query = "UPDATE `main` SET `RoleReadOnly` = 0 WHERE TELEGRAM_ID = %s"
        db.update(query, userID)
        result = 'Пользователь больше не может ставить режим ReadOnly'
    else:
        query = "UPDATE `main` SET `RoleKick` = 1 WHERE TELEGRAM_ID = %s"
        db.update(query, userID)
        result = 'Пользователь теперь может ставить режим ReadOnly'
    return result


def kick(userID):
    query = "SELECT `IsKicked` FROM `main` WHERE `TELEGRAM_ID` = %s"
    data = db.select(query, userID)
    role = data['IsKicked']
    if role:
        query = "UPDATE `main` SET `IsKicked` = 0 WHERE TELEGRAM_ID = %s"
        db.update(query, userID)
        result = 0
    else:
        query = "UPDATE `main` SET `IsKicked` = 1 WHERE TELEGRAM_ID = %s"
        db.update(query, userID)
        result = 1
    return result


def banMedia(message):
    if hasattr(message.reply_to_message, 'from_user'):
        userID = message.reply_to_message.from_user.id
    else:
        result = 'Вы должны отправить команду ответом на сообщение'
        return result

def readOnly(message):
    if hasattr(message.reply_to_message, 'from_user'):
        userID = message.reply_to_message.from_user.id
    else:
        result = 'Вы должны отправить команду ответом на сообщение'
        return result





















