import db
import config
from datetime import datetime
import capcha

def register(message, bot):
    user_id = message.from_user.id
    name = message.text.replace('/reg ', '')
    s = ".,:;!_*-+()/\`'#%&"
    for char in s:
        if char in name:
            result = "В имени есть недопустимые символы. Используйте только латиницу, кириллицу, цифры и знак пробела"
            return result
    if not isExistID(user_id):
        if not isExistName(name):
            _date = datetime.today().strftime('%Y-%m-%d')
            query = "INSERT INTO `users`(`TELEGRAM_ID`, `NAME`, `Created`, `LastOffense`) VALUES(%s, %s, %s, %s)"
            db.update(query, (user_id, name, _date, _date))
            bot.send_message(message.chat.id, 'Вы зарегистрированы как ' + name)
            bot.send_message(message.chat.id, 'Теперь Вам нужно сделать учетную запись активной')
            bot.send_message(message.chat.id, 'Введите символы с картинки ниже')
            updateCapcha(message, bot)

        else:
            result = "Имя " + name + " уже занято"
            bot.send_message(message.chat.id, result)
    else:
        result = "Вы уже зарегистрированы."
        bot.send_message(message.chat.id, result)


def updateCapcha(message, bot):
    _capcha = capcha.CaptchaGenerator(message.chat.id, bot)
    query = "UPDATE `users` SET `Capcha` = %s WHERE TELEGRAM_ID = %s"
    db.update(query, (_capcha, message.from_user.id))


def isActive(user_id):
    query = "SELECT `IsActive` FROM `users` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, user_id)
    return result['IsActive']


def makeActive(user_id):
    query = "UPDATE `users` SET `IsActive` = 1, `Capcha` = '' WHERE TELEGRAM_ID = %s"
    db.update(query, user_id)


def getHash(user_id):
    query = "SELECT `Capcha` FROM `users` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, user_id)
    return result['Capcha']

def isExistID(data):
    query = "SELECT EXISTS(SELECT * FROM `users` WHERE `TELEGRAM_ID` = %s)"
    _isExist = "EXISTS(SELECT * FROM `users` WHERE `TELEGRAM_ID` = " + str(data) + ")"
    result = db.select(query, data)
    return result[_isExist]


def isExistName(data):
    query = "SELECT EXISTS(SELECT * FROM `users` WHERE `NAME` = %s)"
    _isExist = "EXISTS(SELECT * FROM `users` WHERE `NAME` = '" + str(data) + "')"
    result = db.select(query, data)
    return result[_isExist]


def isGOD(user_id):
    query = "SELECT `isGod` FROM `users` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, user_id)
    return result['isGod']


def isKicked(user_id):
    query = "SELECT `isKicked` FROM `users` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, user_id)
    return result['isKicked']


def isRoleKick(user_id):
    query = "SELECT `RoleKick` FROM `users` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, user_id)
    return result['RoleKick']


def isRoleBanMedia(user_id):
    query = "SELECT `RoleBanMedia` FROM `users` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, user_id)
    return result['RoleBanMedia']


def isRoleReadOnly(user_id):
    query = "SELECT `RoleReadOnly` FROM `users` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, user_id)
    return result['RoleReadOnly']


def setPoint(message):
    if isGOD(message.from_user.id):
        if hasattr(message.reply_to_message, 'from_user'):
            user_id = str(message.reply_to_message.from_user.id)
            value = message.text.replace('/setpoint', '')
            if ' ' in value:
                value = value.replace(' ', '')
            else:
                result = 'Вы не ввели значение'
                return result
        else:
            text = message.text.replace('/setpoint', '').split()
            if len(text) == 2:
                user_id = str(text[0])
                value = str(text[1])
            else:
                result = 'Неправильно введена команда. Используйте /setpoint [id] ' \
                         '[количество] или /setpoint [количество] в ответ на сообщение'
                return result
        if int(value) < 0 or int(value) > 140:
            result = 'Неверное значение. Доступные значения: [0..140]'
            return result
        if isExistID(int(user_id)):
            query = "UPDATE `users` SET `POINT` = %s WHERE TELEGRAM_ID = %s"
            db.update(query, (value, user_id))
            result = 'Установлено количество поинтов для ' + user_id + ': ' + value
        else:
            result = 'Пользователь не найден'
    else:
        result = 'Недостаточно прав'
    return result


def getPoint(user_id):
    query = "SELECT `POINT` FROM `users` WHERE `TELEGRAM_ID` = %s"
    result = db.select(query, user_id)
    return result['POINT']


def deleteUser(message):
    if isGOD(message.from_user.id):
        if hasattr(message.reply_to_message, 'from_user'):
            user_id = message.reply_to_message.from_user.id
        else:
            user_id = message.text.replace('/del ', '').split()
        if isExistID(user_id):
            if message.from_user.id == user_id:
                result = 'Самоуничтожение невозможно'
            else:
                query = "DELETE FROM `users` WHERE `TELEGRAM_ID` = %s"
                db.update(query, user_id)
                result = 'Пользователь удален'
        else:
            result = 'Пользователь не найден'
    else:
        result = 'Недостаточно прав'
    return result


def changePoints(message):
    query = "SELECT `POINT` FROM `users` WHERE `TELEGRAM_ID` = %s"
    user_id = message.from_user.id
    points = db.select(query, user_id)
    if points['POINT'] < 5:
        query = "UPDATE `users` SET `isKicked` = %s WHERE TELEGRAM_ID = %s"
        db.update(query, (1, user_id))
    else:
        query = "UPDATE `users` SET `POINT` = %s WHERE TELEGRAM_ID = %s"
        db.update(query, (points['POINT'] - 5, user_id))


def updateLastOffense(message):
    user_id = message.from_user.id
    query = "UPDATE `users` SET `LastOffense` = %s WHERE TELEGRAM_ID = %s"
    db.update(query, (datetime.today().strftime('%Y-%m-%d'), user_id))


def info(message):
    if hasattr(message.reply_to_message, 'from_user'):
        if isGOD(message.from_user.id):
            user_id = message.reply_to_message.from_user.id
        else:
            result = 'Вы не можете просмотреть информацию о другом пользователе'
            return result
    else:
        user_id = message.from_user.id
    if isExistID(user_id):
        query = "SELECT * FROM `users` WHERE `TELEGRAM_ID` = %s"
        data = db.select(query, user_id)
        result = \
            'Телеграм ID: ' + str(data['TELEGRAM_ID']) + \
            '\nИмя: ' + data['NAME'] +  \
            '\nПоинты: ' + str(data['POINT']) + \
            '\nДата регистрации: ' + str(data['Created']) + \
            '\nСообщений всего: ' + str(data['MessageStat']) + \
            '\nМедиа всего: ' + str(data['MediaStat']) + \
            '\nСтикеров отправлено: ' + str(data['StickerStat'])
        if data['RoleKick'] == 1 or data['RoleReadOnly'] == 1 or data['RoleBanMedia'] == 1 or data['IsGod'] == 1:
            result += '\nРоли:'
            if data['RoleKick'] == 1:
                result += '\n   Возможность кика'
            if data['RoleReadOnly'] == 1:
                result += '\n   Возможность ставить режим ReadOnly'
            if data['RoleBanMedia'] == 1:
                result += '\n   Возможность запрета Медиа'
            if data['IsGod'] == 1:
                result += '\n   God'

    else:
        result = 'Пользователь не зарегистрирован'
    return result


def canKick(message):
    if hasattr(message.reply_to_message, 'from_user'):
        if isGOD(message.from_user.id):
            user_id = message.reply_to_message.from_user.id
            query = "SELECT `RoleKick` FROM `users` WHERE `TELEGRAM_ID` = %s"
            data = db.select(query, user_id)
            role = data['RoleKick']
            if role:
                query = "UPDATE `users` SET `RoleKick` = 0 WHERE TELEGRAM_ID = %s"
                db.update(query, user_id)
                result = 'Пользователь больше не может кикать'
            else:
                query = "UPDATE `users` SET `RoleKick` = 1 WHERE TELEGRAM_ID = %s"
                db.update(query, user_id)
                result = 'Пользователь теперь может кикать'
        else:
            result = 'Недостаточно прав'
    else:
        result = 'Вы должны отправить команду ответом на сообщение'
    return result


def canBanMedia(message):
    if hasattr(message.reply_to_message, 'from_user'):
        if isGOD(message.from_user.id):
            user_id = message.reply_to_message.from_user.id
            query = "SELECT `RoleBanMedia` FROM `users` WHERE `TELEGRAM_ID` = %s"
            data = db.select(query, user_id)
            role = data['RoleBanMedia']
            if role:
                query = "UPDATE `users` SET `RoleBanMedia` = 0 WHERE TELEGRAM_ID = %s"
                db.update(query, user_id)
                result = 'Пользователь больше не может запрещать медиа'
            else:
                query = "UPDATE `users` SET `RoleBanMedia` = 1 WHERE TELEGRAM_ID = %s"
                db.update(query, user_id)
                result = 'Пользователь теперь может запрещать медиа'
        else:
            result = 'Недостаточно прав'
    else:
        result = 'Вы должны отправить команду ответом на сообщение'
    return result


def canReadOnly(message):
    if hasattr(message.reply_to_message, 'from_user'):
        if isGOD(message.from_user.id):
            user_id = message.reply_to_message.from_user.id
            query = "SELECT `RoleReadOnly` FROM `users` WHERE `TELEGRAM_ID` = %s"
            data = db.select(query, user_id)
            role = data['RoleReadOnly']
            if role:
                query = "UPDATE `users` SET `RoleReadOnly` = 0 WHERE TELEGRAM_ID = %s"
                db.update(query, user_id)
                result = 'Пользователь больше не может ставить режим ReadOnly'
            else:
                query = "UPDATE `users` SET `RoleReadOnly` = 1 WHERE TELEGRAM_ID = %s"
                db.update(query, user_id)
                result = 'Пользователь теперь может ставить режим ReadOnly'
        else:
            result = 'Недостаточно прав'
    else:
        result = 'Вы должны отправить команду ответом на сообщение'
    return result


def kick(user_id):
    query = "SELECT `IsKicked` FROM `users` WHERE `TELEGRAM_ID` = %s"
    data = db.select(query, user_id)
    role = data['IsKicked']
    if role:
        query = "UPDATE `users` SET `IsKicked` = 0 WHERE TELEGRAM_ID = %s"
        db.update(query, user_id)
        result = 0
    else:
        query = "UPDATE `users` SET `IsKicked` = 1 WHERE TELEGRAM_ID = %s"
        db.update(query, user_id)
        result = 1
    return result


def stickerCounter(user_id):
    query = "SELECT `StickerStat` FROM `users` WHERE `TELEGRAM_ID` = %s"
    data = db.select(query, user_id)
    newcount = data['StickerStat'] + 1
    query = "UPDATE `users` SET `StickerStat` = %s WHERE TELEGRAM_ID = %s"
    db.update(query, (newcount, user_id))

def messageCounter(user_id):
    query = "SELECT `MessageStat` FROM `users` WHERE `TELEGRAM_ID` = %s"
    data = db.select(query, user_id)
    newcount = data['MessageStat'] + 1
    query = "UPDATE `users` SET `MessageStat` = %s WHERE TELEGRAM_ID = %s"
    db.update(query, (newcount, user_id))

def mediaCounter(user_id):
    query = "SELECT `MediaStat` FROM `users` WHERE `TELEGRAM_ID` = %s"
    data = db.select(query, user_id)
    newcount = data['MediaStat'] + 1
    query = "UPDATE `users` SET `MediaStat` = %s WHERE TELEGRAM_ID = %s"
    db.update(query, (newcount, user_id))


def getName(user_id):
    query = "SELECT `NAME` FROM `users` WHERE `TELEGRAM_ID` = %s"
    data = db.select(query, user_id)
    result = '[' + str(data['NAME']) + '](tg://user?id=' + str(user_id) + ')'
    return result


def layout(message):
    if hasattr(message.reply_to_message, 'from_user'):
        msg = message.reply_to_message.text
        if msg != "":
            result = ""
            for char in msg:
                if char in config.alphabet_changelayout:
                    result += config.alphabet_changelayout[char]
                else:
                    result += char
        else:
            result = 'В сообщении нет текста, невозможно сменить раскладку'
    else:
        result = 'Вы должны отправить команду ответом на сообщение'
    return result

