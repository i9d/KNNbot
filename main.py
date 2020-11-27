import button_setup
import config
import messages_lib
import db_config

import random
import time

import telebot

from urllib.request import urlopen
from PIL import Image

# подключение к боту
bot = telebot.TeleBot(config.token)

ban_time = time.time() + 31  # 31 секунда

# Словарь про команду
team = {'Настя': 'отвечает за поиск библеотек на начальном этапе, а затем будет помогать с тестами модулей',
        'Никита': 'ставит всё на сервер и работает с БД',
        'Коля': 'пишет код для этого бота'
        }

# Список запрещенных сообщений берем из файла
restricted_messages = []
with open("bad_words", 'r') as read_file:
    for line in read_file:
        restricted_messages.append(line.strip('\n'))


# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_sticker(message.chat.id, random.choice(messages_lib.welcome_stickers_id))
    start_message = f"Привет, {message.from_user.first_name}!\nЧем могу быть полезен?"
    # Обращаемся к пользователю по имени в telegram
    bot.send_message(message.chat.id, start_message, parse_mode='html', reply_markup=button_setup.button)


# Команда /developers_info
@bot.message_handler(commands=['developers_info'])
def developers_info(message):
    for name in team:
        start_message = name + ' - ' + team[name]  # выводим словарь
        bot.send_message(message.chat.id, start_message)
        time.sleep(0.2)  # мини-зареджка в 2 мс. для отправки сообщений в цикле


# Команда /about
@bot.message_handler(commands=['about'])
def about(message):
    # Ниже выводим ключи из словаря team
    about_message = "*Я — учебный проект 3 ФКН-щиков*\nИх зовут — " + ', '.join(
        team.keys()) + '\n\n[Проект на GitHub](https://github.com/i9d/superbottelegramskoleyinastey)'
    bot.send_message(message.chat.id, about_message, parse_mode='markdown')


# Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    help_message = "Пока я могу только рассказать о проекте и нашей команде. Введи команду /about или /team_info"
    bot.send_message(message.chat.id, help_message)


# Команда /reg
@bot.message_handler(commands=['reg'])
def reg(message):
    db_config.insert(message)
    reg_message = "Вы зарегистрированы как " + message.from_user.username
    bot.send_message(message.chat.id, reg_message)


@bot.message_handler(commands=['info'])
def user_info(message):
    sel = "SELECT * FROM `MAIN` WHERE TELEGRAM_ID=" + str(message.from_user.id) #тут эту гавну выведи в файл, чтоб не выглядело как гавно
    data = db_config.select(sel)
    information = 'Телеграм ID: ' + str(data['TELEGRAM_ID']) + '\nИмя: ' + data['NAME'] + '\nПредупреждения: ' + str(data['WARN']) + '\nПоинты: ' + str(data['POINT'])
    bot.send_message(message.chat.id, information)


# Модерация голосовых и видео сообщений
@bot.message_handler(content_types=['voice', 'video_note'])
def get_voice(message):
    print('Пришло голосовое сообщение от', message.from_user.username)
    if message.chat.id == config.group_id:
        # Удаление голосовых сообщений с предупреждением отправителя
        warming_message = '@' + str(message.from_user.username) + random.choice(
            messages_lib.warming_message_base) + '\nЯ это пока просто удалю, а потом уже дам бан.'
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, warming_message)
        print('Начинаю удалять сообщение')
    else:
        bot.send_message(message.chat.id, 'Я не умею слушать, прости')


# Обработка входа участников
@bot.message_handler(content_types=['new_chat_members'])
def event_member_enter(message):
    bot.send_sticker(message.chat.id, random.choice(messages_lib.welcome_stickers_id))
    start_message = f"Привет, @{message.from_user.username}!"  # Обращаемся к пользователю по имени в telegram
    bot.send_message(message.chat.id, start_message)


# Обработка выхода участников
@bot.message_handler(content_types=['left_chat_member'])
def event_member_exit(message):
    image = Image.open(urlopen('https://cdn.everypony.ru/storage/01/75/20/2019/06/23/fba29a367f.png'))
    bot.send_photo(message.chat.id, image)


# Обработка закрепленных сообщений
@bot.message_handler(content_types=['pinned_message'])
def event_pin_message(message):
    bot.send_message(message.chat.id, 'Запомните, твари!')


# Обработка смены аватарки
@bot.message_handler(content_types=['new_chat_photo', 'delete_chat_photo'])
def event_photo_chat_change(message):
    image = Image.open(urlopen('https://sun9-46.userapi.com/ecwT1VkRbiZDzPeLmK6BibvlxoVSyBxu983nPg/115Gbhs_ug4.jpg'))
    if message.from_user.username != 'beta_version_fkn_bot':
        bot.send_message(message.chat.id, 'Слыш, фото не трогай!')
        bot.set_chat_photo(message.chat.id, image)


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text(message):
    # обработка в консоль
    print('Пришло сообщение от', message.from_user.username + ':')
    print(message.text)

    # Обработка запрещенных сообщений
    # if message.text in restricted_messages and message.chat.id == config.group_id:
    for word in restricted_messages:
        if word in message.text.lower() and message.chat.id == config.group_id:
            # Удаление запрещенных сообщений
            warming_message = random.choice(messages_lib.warming_message_base2) + ' @' + str(
                message.from_user.username) + '!\n\nПусть теперь сидит и читает только, пока не помилуют'
            bot.reply_to(message,
                         warming_message)  # можно заменить на main.bot.delete_message(message.chat.id, message.message_id)
            bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=int(ban_time))
            print('Даю мут пользователю', message.from_user.username)

    if message.text == 'О проекте':
        about(message)
    elif message.text == 'Разработчики':
        developers_info(message)
    # else:
    #    bot.send_message(message.from_user.id, "Я пока не знаю что с этим делать. Попробуй написать /help")


# Когда бот получает стикер, будет отправлять случайные из stickers_lib.py
@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    print('Получен стикер от', message.from_user.username)  # обработка в консоль
    if message.chat.id != config.group_id:
        bot.send_sticker(message.chat.id, random.choice(messages_lib.stickers_id))


# Бот постоянно ждёт для себя сообщения
bot.polling(none_stop=True)
