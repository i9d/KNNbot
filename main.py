from urllib.request import urlopen
from PIL import Image
import button_setup
import config
import commands
import random
import telebot
import time

# подключение к боту
bot = telebot.TeleBot(config.token)

stickermode = 0


# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_sticker(message.chat.id, random.choice(config.welcome_stickers_id))
    start_message = f"Привет, {message.from_user.first_name}!\nЧем могу быть полезен?"
    # Обращаемся к пользователю по имени в telegram
    bot.send_message(message.chat.id, start_message, parse_mode='html', reply_markup=button_setup.button)


# Команда /developers_info
@bot.message_handler(commands=['developers_info'])
def developers_info(message):
    for name in config.team:
        start_message = name + ' - ' + config.team[name]  # выводим словарь
        bot.send_message(message.chat.id, start_message)
        time.sleep(0.2)  # мини-зареджка в 2 мс. для отправки сообщений в цикле


# Команда /about
@bot.message_handler(commands=['about'])
def about(message):
    # Ниже выводим ключи из словаря team
    about_message = "*Я — учебный проект 3 ФКН-щиков*\nИх зовут — " + ', '.join(
        config.team.keys()) + '\n\n[Проект на GitHub](https://github.com/i9d/KNNbot)'
    bot.send_message(message.chat.id, about_message, parse_mode='markdown')


# Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    help_message = "Для общения в чате нужно зарегистрироваться с помощью команды /reg [name]" \
                   "\nДля получения информации о себе, напишите /info \nНапишите /about, чтобы узнать о проекте" \
                   " или /team_info, чтобы узнать о разработчиках"
    bot.send_message(message.chat.id, help_message)


# Модерация голосовых и видео сообщений
@bot.message_handler(content_types=['voice', 'video_note'])
def get_voice(message):
    commands.mediaCounter(message.from_user.id)
    print('Пришло голосовое сообщение от', message.from_user.username)
    if message.chat.id not in config.group_id:
        # Удаление голосовых сообщений с предупреждением отправителя
        warning_message = commands.getName(message.from_user.id) \
                          + random.choice(config.warming_message_base) \
                          + '\nЯ это пока просто удалю, а потом уже дам бан'

        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, warning_message, parse_mode='MarkdownV2')
        print('Начинаю удалять сообщение')
        print(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Я не умею слушать, прости')


# Обработка фото, видео, аудио
@bot.message_handler(content_types=['photo', 'video', 'audio'])
def get_photo(message):
    commands.mediaCounter(message.from_user.id)


# Обработка входа участников
@bot.message_handler(content_types=['new_chat_members'])
def event_member_enter(message):
    if commands.isExistID(message.new_chat_members[0].id):
        if commands.isKicked(message.new_chat_members[0].id):
            sndmsg = 'Вы были кикнуты, доступ к беседе запрещен'
            bot.send_message(message.chat.id, sndmsg)
            bot.kick_chat_member(message.chat.id, message.new_chat_members[0].id)

    else:
        bot.send_sticker(message.chat.id, random.choice(config.welcome_stickers_id))
        start_message = f"Привет, @{message.new_chat_members[0].username}!" +\
                        '\nЗарегистрируйся с помощью команды /reg [name]'  # Обращаемся к пользователю по имени в telegram
        bot.send_message(message.chat.id, start_message)


# Обработка выхода участников
@bot.message_handler(content_types=['left_chat_member'])
def event_member_exit(message):
    image = Image.open(urlopen('https://cdn.everypony.ru/storage/01/75/20/2019/06/23/fba29a367f.png'))
    bot.send_photo(message.chat.id, image)


# Обработка закрепленных сообщений
@bot.message_handler(content_types=['pinned_message'])
def event_pin_message(message):
    bot.send_message(message.chat.id, 'Запомните, человеки!')


# Обработка смены аватарки
@bot.message_handler(content_types=['new_chat_photo', 'delete_chat_photo'])
def event_photo_chat_change(message):
    print(message.from_user.username, 'меняет фото')
    image = Image.open(urlopen('https://sun9-46.userapi.com/ecwT1VkRbiZDzPeLmK6BibvlxoVSyBxu983nPg/115Gbhs_ug4.jpg'))
    if message.from_user.username not in config.bot_username:
        bot.send_message(message.chat.id, 'Слыш, фото не трогай!')
        bot.set_chat_photo(message.chat.id, image)


# Когда бот получает стикер, будет отправлять случайные из stickers_lib.py
@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    global stickermode
    print(stickermode)
    print('Получен стикер от', message.from_user.username)  # обработка в консоль
    commands.stickerCounter(message.from_user.id)
    if message.chat.type == 'private' or stickermode == 1:
        bot.send_sticker(message.chat.id, random.choice(config.stickers_id))


# Смена раскладки
@bot.message_handler(commands=['раскладка'])
def change_layout(message):
    bot.reply_to(message, commands.layout(message))


# Выдача роли ReadOnly
@bot.message_handler(commands=['giveRoleRO'])
def giveRoleRO(message):
    bot.reply_to(message, commands.canReadOnly(message))


# Выдача роли Кик
@bot.message_handler(commands=['giveRoleKick'])
def giveRoleKick(message):
    bot.reply_to(message, commands.canKick(message))


# Выдача роли Бан Медиа
@bot.message_handler(commands=['giveRoleBanMedia'])
def giveRoleBanMedia(message):
    bot.reply_to(message, commands.canBanMedia(message))


# Обработка /info
@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, commands.info(message))


# Обработка /kick
@bot.message_handler(commands=['kick'])
def kick(message):
    if commands.isRole(message.from_user.id, 'RoleKick'):
        if hasattr(message.reply_to_message, 'from_user'):
            user_id = message.reply_to_message.from_user.id
        else:
            result = 'Вы должны отправить команду ответом на сообщение'
            return result
        if not commands.isGOD(user_id) and user_id != message.from_user.id:
            tmp = commands.kick(user_id)
            if tmp == 1:
                sndMsg = commands.getName(user_id) + ' кикнут'
                bot.kick_chat_member(message.chat.id, user_id)
            elif tmp == 0:
                sndMsg = commands.getName(user_id) + ' пощажен'
            else:
                sndMsg = tmp
        else:
            sndMsg = 'Ты кого кикать собрался, псина?'
    else:
        sndMsg = 'Недостаточно прав'
    bot.reply_to(message, sndMsg, parse_mode='MarkdownV2')


# Обработка /banmedia_on
@bot.message_handler(commands=['banmedia_on'])
def banmedia_on(message):
    if commands.isRole(message.from_user.id, 'RoleBanMedia'):
        if hasattr(message.reply_to_message, 'from_user'):
            user_id = message.reply_to_message.from_user.id
        else:
            result = 'Вы должны отправить команду ответом на сообщение'
            return result
        if not commands.isGOD(user_id) and user_id != message.from_user.id:
            sndMsg = 'Медиа заблокированы для пользователя ' + commands.getName(user_id)
            bot.restrict_chat_member(message.chat.id, user_id, can_send_media_messages=0, can_send_messages=1)
            bot.delete_message(message.chat.id, message.reply_to_message.id)
        else:
            sndMsg = 'Попытка устроить переворот'
    else:
        sndMsg = 'Недостаточно прав'
    bot.reply_to(message, sndMsg, parse_mode='MarkdownV2')


# Обработка /banmedia_off
@bot.message_handler(commands=['banmedia_off'])
def banmedia_off(message):
    if commands.isRole(message.from_user.id, 'RoleBanMedia'):
        if hasattr(message.reply_to_message, 'from_user'):
            user_id = message.reply_to_message.from_user.id
        else:
            result = 'Вы должны отправить команду ответом на сообщение'
            return result
        if not commands.isGOD(user_id) and user_id != message.from_user.id:
            sndMsg = 'Медиа разблокированы для пользователя ' + commands.getName(user_id)
            bot.restrict_chat_member(message.chat.id, user_id, can_send_media_messages=1, can_send_other_messages=1, can_add_web_page_previews=1)
        else:
            sndMsg = 'Попытка устроить переворот'
    else:
        sndMsg = 'Недостаточно прав'
    bot.reply_to(message, sndMsg, parse_mode='MarkdownV2')

# Обработка /readonly_on
@bot.message_handler(commands=['readonly_on'])
def readonly_on(message):
    if commands.isRole(message.from_user.id, 'RoleReadOnly'):
        if hasattr(message.reply_to_message, 'from_user'):
            user_id = message.reply_to_message.from_user.id
        else:
            result = 'Вы должны отправить команду ответом на сообщение'
            return result
        if not commands.isGOD(user_id) and user_id != message.from_user.id:
            bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            sndMsg = 'Включен режим ReadOnly для пользователя ' + commands.getName(user_id)
            bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=0)
            bot.delete_message(message.chat.id, message.reply_to_message.id)
        else:
            sndMsg = 'Попытка устроить переворот'
    else:
        sndMsg = 'Недостаточно прав'
    bot.reply_to(message, sndMsg, parse_mode='MarkdownV2')


# Обработка /readonly_off
@bot.message_handler(commands=['readonly_off'])
def readonly_off(message):
    if commands.isRole(message.from_user.id, 'RoleReadOnly'):
        if hasattr(message.reply_to_message, 'from_user'):
            user_id = message.reply_to_message.from_user.id
        else:
            result = 'Вы должны отправить команду ответом на сообщение'
            return result
        if not commands.isGOD(user_id) and user_id != message.from_user.id:
            sndMsg = 'Выключен режим ReadOnly для пользователя ' + commands.getName(user_id)
            bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=1)
        else:
            sndMsg = 'Попытка устроить переворот'
    else:
        sndMsg = 'Недостаточно прав'
    bot.reply_to(message, sndMsg, parse_mode='MarkdownV2')


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text(message):
    # обработка в консоль
    print('Пришло сообщение от', message.from_user.username + ':')
    print(message.text)
    global stickermode

    # Если в БД ключ isKicked = 1, то пользователь удаляется из конференции
    if commands.isExistID(message.from_user.id) and commands.isKicked(message.from_user.id):
        bot.restrict_chat_member(message.chat.id, message.from_user.id)
        print('Даю пермач пользователю', message.from_user.username)
        sndMsg = "Пользователь удален за многократные нарушения."
        bot.reply_to(message, sndMsg)
        bot.kick_chat_member(message.chat.id, message.from_user.id)

    # Обработка команды /reg
    if "/reg " in message.text:
        sndMsg = commands.register(message)
        bot.reply_to(message, sndMsg)

    # Обработка основной части сообщений(только если пользователь зарегистрирован)
    elif commands.isExistID(message.from_user.id):
        # Мат-фильтр, только для not IsGOD
        commands.messageCounter(message.from_user.id)
        if not commands.isGOD(message.from_user.id):
            text = message.text.lower().replace(' ', '')
            text = ''.join(text)

            for key, value in config.alphabet.items():
                # Проходимся по каждой букве в значении словаря. То есть по вот этим спискам ['а', 'a', '@'].
                for letter in value:
                    # Проходимся по каждой букве в нашей фразе.
                    for phr in text:
                        # Если буква совпадает с буквой в нашем списке.
                        if letter == phr:
                            # Заменяем эту букву на ключ словаря.
                            text = text.replace(phr, key)

            text = [c for c in text if c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- ']
            text = ''.join(text)
            print(text)

            # Обработка запрещенных сообщений
            # if message.text in restricted_messages and message.chat.id == config.group_id:
            # bad_words = open('bad_words', 'r')
            for word in config.restricted_messages:
                if word in text:
                    # Удаление запрещенных сообщений
                    points = commands.getPoint(message.from_user.id)
                    ban_seconds = 604800 // ((points * points) + 1)
                    warning_message = random.choice(config.warming_message_base2) + ' @' + \
                                      str(message.from_user.username) + \
                                      '!\n\nПусть теперь сидит и читает только целых ' +\
                                      str(ban_seconds) + ' секунд!'
                    bot.reply_to(message, warning_message)
                    bot.delete_message(message.chat.id, message.message_id)

                    ban_time = time.time() + ban_seconds
                    bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=ban_time)
                    print('Даю мут пользователю', message.from_user.username, ' на ', ban_seconds, ' секунд')
                    commands.changePoints(message)
                    commands.updateLastOffense(message)
        # Обработка сообщения 'О проекте'
        if message.text == 'О проекте':
            about(message)
        # Обработка сообщения 'Разработчики'
        elif message.text == 'Разработчики':
            developers_info(message)

    # Команды для GOD

        # Включение стикеров
        elif message.text == '/sticker_on':
            if commands.isGOD(message.from_user.id):
                stickermode = 1
                sndMsg = 'Стикеры включены'
            else:
                sndMsg = 'Недостаточно прав'
            bot.reply_to(message, sndMsg)

        # Выключение стикеров
        elif message.text == '/sticker_off':
            if commands.isGOD(message.from_user.id):
                stickermode = 0
                sndMsg = 'Стикеры выключены'
            else:
                sndMsg = 'Недостаточно прав'
            bot.reply_to(message, sndMsg)

        # Удаление пользователя из БД
        elif "/del" in message.text:
            if commands.isGOD(message.from_user.id):
                sndMsg = commands.deleteUser(message)
            else:
                sndMsg = 'Недостаточно прав'
            bot.reply_to(message, sndMsg)

        # Установить количество поинтов
        elif "/setpoint" in message.text:
            if commands.isGOD(message.from_user.id):
                sndMsg = commands.setPoint(message)
            else:
                sndMsg = 'Недостаточно прав'
            bot.reply_to(message, sndMsg)

    # Если пользователя нет в БД
    else:
        sndMsg = "Вы не зарегистрированы. Зарегистрируйтесь с помощью команды /reg [name]"
        bot.reply_to(message, sndMsg)
        bot.delete_message(message.chat.id, message.message_id)


# Бот постоянно ждёт для себя сообщения
bot.polling(none_stop=True)
