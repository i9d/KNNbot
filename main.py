import button_setup, config, db_config, random, time, telebot

from urllib.request import urlopen
from PIL import Image

# подключение к боту
bot = telebot.TeleBot(config.token)

ban_time = time.time() + 31  # 31 секунда

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
        config.team.keys()) + '\n\n[Проект на GitHub](https://github.com/i9d/superbottelegramskoleyinastey)'
    bot.send_message(message.chat.id, about_message, parse_mode='markdown')


# Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    help_message = "Я могу зарегистрировать пользователя у себя в базе данных. Чтобы зарегистрироваться напиши" \
                   " /reg \nЧтобы проверить регистрацию, напишите /info \nНапишите /about, чтобы узнать о проекте" \
                   " или /team_info, чтобы узнать о разработчиках"
    bot.send_message(message.chat.id, help_message)


# Команда /reg
@bot.message_handler(commands=['reg'])
def reg(message):
    db_config.insert(message)
    reg_message = "Вы зарегистрированы как " + message.from_user.username
    bot.send_message(message.chat.id, reg_message)

# Команда /info
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
    if message.chat.id not in config.group_id:
        # Удаление голосовых сообщений с предупреждением отправителя
        warming_message = '@' + str(message.from_user.username) + random.choice(
            config.warming_message_base) + '\nЯ это пока просто удалю, а потом уже дам бан.'
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, warming_message)
        print('Начинаю удалять сообщение')
    else:
        bot.send_message(message.chat.id, 'Я не умею слушать, прости')


# Обработка входа участников
@bot.message_handler(content_types=['new_chat_members'])
def event_member_enter(message):
    bot.send_sticker(message.chat.id, random.choice(config.welcome_stickers_id))
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
    bot.send_message(message.chat.id, 'Запомните, человеки!')


# Обработка смены аватарки
@bot.message_handler(content_types=['new_chat_photo', 'delete_chat_photo'])
def event_photo_chat_change(message):
    print(message.from_user.username, 'меняет фото')
    image = Image.open(urlopen('https://sun9-46.userapi.com/ecwT1VkRbiZDzPeLmK6BibvlxoVSyBxu983nPg/115Gbhs_ug4.jpg'))
    if message.from_user.username not in config.bot_username:
        bot.send_message(message.chat.id, 'Слыш, фото не трогай!')
        bot.set_chat_photo(message.chat.id, image)


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text(message):
    # обработка в консоль
    print('Пришло сообщение от', message.from_user.username + ':')
    print(message.text)
    global stickermode

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
    for word in config.restricted_messages:
            if word in text:
                # Удаление запрещенных сообщений
                warming_message = random.choice(config.warming_message_base2) + ' @' + str(
                    message.from_user.username) + '!\n\nПусть теперь сидит и читает только, пока не помилуют'
                bot.reply_to(message,
                             warming_message)  # можно заменить на main.bot.delete_message(message.chat.id, message.message_id)
                bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=int(ban_time))
                print('Даю мут пользователю', message.from_user.username)

    if message.text == 'О проекте':
        about(message)
    elif message.text == 'Разработчики':
        developers_info(message)
    elif message.text == '/sticker_on':
        stickermode= 1
    elif message.text == '/sticker_off':
        stickermode = 0
    # else:
    #    bot.send_message(message.from_user.id, "Я пока не знаю что с этим делать. Попробуй написать /help")

# Когда бот получает стикер, будет отправлять случайные из stickers_lib.py
@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    global stickermode
    print(stickermode)
    print('Получен стикер от', message.from_user.username)  # обработка в консоль
    if message.chat.type == 'private':
        bot.send_sticker(message.chat.id, random.choice(config.stickers_id))
    elif stickermode == 1:
        bot.send_sticker(message.chat.id, random.choice(config.stickers_id))

# Бот постоянно ждёт для себя сообщения
bot.polling(none_stop=True)
import button_setup, config, db_config, random, time, telebot

from urllib.request import urlopen
from PIL import Image

# подключение к боту
bot = telebot.TeleBot(config.token)

ban_time = time.time() + 31  # 31 секунда

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
        config.team.keys()) + '\n\n[Проект на GitHub](https://github.com/i9d/superbottelegramskoleyinastey)'
    bot.send_message(message.chat.id, about_message, parse_mode='markdown')


# Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    help_message = "Я могу зарегистрировать пользователя у себя в базе данных. Чтобы зарегистрироваться напиши" \
                   " /reg \nЧтобы проверить регистрацию, напишите /info \nНапишите /about, чтобы узнать о проекте" \
                   " или /team_info, чтобы узнать о разработчиках"
    bot.send_message(message.chat.id, help_message)


# Команда /reg
@bot.message_handler(commands=['reg'])
def reg(message):
    db_config.insert(message)
    reg_message = "Вы зарегистрированы как " + message.from_user.username
    bot.send_message(message.chat.id, reg_message)

# Команда /info
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
    if message.chat.id not in config.group_id:
        # Удаление голосовых сообщений с предупреждением отправителя
        warming_message = '@' + str(message.from_user.username) + random.choice(
            config.warming_message_base) + '\nЯ это пока просто удалю, а потом уже дам бан.'
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, warming_message)
        print('Начинаю удалять сообщение')
    else:
        bot.send_message(message.chat.id, 'Я не умею слушать, прости')


# Обработка входа участников
@bot.message_handler(content_types=['new_chat_members'])
def event_member_enter(message):
    bot.send_sticker(message.chat.id, random.choice(config.welcome_stickers_id))
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
    bot.send_message(message.chat.id, 'Запомните, человеки!')


# Обработка смены аватарки
@bot.message_handler(content_types=['new_chat_photo', 'delete_chat_photo'])
def event_photo_chat_change(message):
    print(message.from_user.username, 'меняет фото')
    image = Image.open(urlopen('https://sun9-46.userapi.com/ecwT1VkRbiZDzPeLmK6BibvlxoVSyBxu983nPg/115Gbhs_ug4.jpg'))
    if message.from_user.username not in config.bot_username:
        bot.send_message(message.chat.id, 'Слыш, фото не трогай!')
        bot.set_chat_photo(message.chat.id, image)


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text(message):
    # обработка в консоль
    print('Пришло сообщение от', message.from_user.username + ':')
    print(message.text)
    global stickermode

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
    for word in config.restricted_messages:
            if word in text:
                # Удаление запрещенных сообщений
                warming_message = random.choice(config.warming_message_base2) + ' @' + str(
                    message.from_user.username) + '!\n\nПусть теперь сидит и читает только, пока не помилуют'
                bot.reply_to(message,
                             warming_message)  # можно заменить на main.bot.delete_message(message.chat.id, message.message_id)
                bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=int(ban_time))
                print('Даю мут пользователю', message.from_user.username)

    if message.text == 'О проекте':
        about(message)
    elif message.text == 'Разработчики':
        developers_info(message)
    elif message.text == '/sticker_on':
        stickermode= 1
    elif message.text == '/sticker_off':
        stickermode = 0
    # else:
    #    bot.send_message(message.from_user.id, "Я пока не знаю что с этим делать. Попробуй написать /help")

# Когда бот получает стикер, будет отправлять случайные из stickers_lib.py
@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    global stickermode
    print(stickermode)
    print('Получен стикер от', message.from_user.username)  # обработка в консоль
    if message.chat.type == 'private':
        bot.send_sticker(message.chat.id, random.choice(config.stickers_id))
    elif stickermode == 1:
        bot.send_sticker(message.chat.id, random.choice(config.stickers_id))

# Бот постоянно ждёт для себя сообщения
bot.polling(none_stop=True)