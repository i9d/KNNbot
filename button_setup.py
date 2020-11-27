from telebot import types

# создание кнопок
button = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_info = types.KeyboardButton(text='О проекте')
button_team_info = types.KeyboardButton(text='Разработчики')
button.add(button_info, button_team_info)