# Данные бота
token = '1020063385:AAG5dWsOWwd6UgHQZnkh9FRl8oI3ozhnSx0'

#beta_version_fkn_bot = 1020063385:AAG5dWsOWwd6UgHQZnkh9FRl8oI3ozhnSx0
#fkn_top_bot = 1313903888:AAGLfKkVqVHnNltMUdRr86oyetAssEikXGk

# Список групп
group_id = ['-1001281269402']

# Список ботов (чтобы не реагировал на своих)
bot_username = ['fkn_top_bot', 'beta_version_fkn_bot']

# Алфавит
alphabet =   {'а' : ['а', 'a', '@'],
  'б' : ['б', '6', 'b'],
  'в' : ['в', 'b', 'v'],
  'г' : ['г', 'r', 'g'],
  'д' : ['д', 'd'],
  'е' : ['е', 'e'],
  'ё' : ['ё', 'e'],
  'ж' : ['ж', 'zh', '*'],
  'з' : ['з', '3', 'z'],
  'и' : ['и', 'u', 'i'],
  'й' : ['й', 'u', 'i'],
  'к' : ['к', 'k', 'i{', '|{'],
  'л' : ['л', 'l', 'ji'],
  'м' : ['м', 'm'],
  'н' : ['н', 'h', 'n'],
  'о' : ['о', 'o', '0'],
  'п' : ['п', 'n', 'p'],
  'р' : ['р', 'r', 'p'],
  'с' : ['с', 'c', 's'],
  'т' : ['т', 'm', 't'],
  'у' : ['у', 'y', 'u'],
  'ф' : ['ф', 'f'],
  'х' : ['х', 'x', 'h' , '}{'],
  'ц' : ['ц', 'c', 'u,'],
  'ч' : ['ч', 'ch'],
  'ш' : ['ш', 'sh'],
  'щ' : ['щ', 'sch'],
  'ь' : ['ь', 'b'],
  'ы' : ['ы', 'bi'],
  'ъ' : ['ъ'],
  'э' : ['э', 'e'],
  'ю' : ['ю', 'io'],
  'я' : ['я', 'ya']
}

# Словарь про команду
team = {'Настя': 'отвечает за поиск библеотек на начальном этапе, а затем будет помогать с тестами модулей',
        'Никита': 'ставит всё на сервер и работает с БД',
        'Коля': 'пишет код для этого бота'
        }

# База запрещенных слов
restricted_messages = ['ахуел', 'ахуенно', 'бля', 'блядь', 'блять', 'ебаль', 'ебал',
                       'еблан', 'eбaл', 'eбaть', 'eбyч', 'соси', 'сосать', 'сука', 'хуета', 'хуита', 'хуище', 'хуля', 'хуй', 'хуйня', 'хую', 'хуюл', 'хуя', 'хуяк', 'хуякать',
                       'хуякнуть', 'хуяра', 'хуясе', 'хуячить', 'целка', 'чмо', 'чмошник', 'чмырь',
                       'шалава', 'шалавой', 'шараёбиться', 'шлюха', 'шлюхой', 'шлюшка', 'пезда', 'ананас', 'гуси', 'банан']

# База приветсвенных стикеров
welcome_stickers_id = ['CAACAgIAAxkBAAJAJ1-Y7xYeCFw7W1d1NTDPSbWFqKJgAAJ0AAM7YCQUs8te1W3kR_QbBA',
                       'CAACAgIAAxkBAAJAKl-Y7zFxon611n7irTqF9ppIJzI_AAL1AwACRxVoCYDkI4apaTHtGwQ',
                       'CAACAgIAAxkBAAJALV-Y709SS_NbyoBfTC8BOop4GJySAAJOAgACel9AC_2AVZz45IeJGwQ',
                       'CAACAgIAAxkBAAJAM1-Y72Zyac3q-uyMFLMIkqiPZd2cAALkAAOWn4wOxwgM9TN-1vcbBA',
                       'CAACAgIAAxkBAAJAMF-Y72V1A2xY3Aj9V2GMfV-ZYDr8AAKHAgACVp29CkLtdCtAV9CQGwQ'
                       ]

# База стикеров
stickers_id = ['CAACAgIAAxkBAAJANl-Y75YQ8pGWtBipNGYpjGqrfbUgAAJaAAM_W6Y7v9jKOFYpupYbBA',
               'CAACAgEAAxkBAAJAOV-Y75euhdoT5NCZ-THhr9rPvxfzAALBAAP27y4t7kciaRUJBTQbBA',
               'CAACAgIAAxkBAAJAPF-Y75jt3dFep2Q5grddgYHl70jZAAKGAgACVp29CurmC5LHcbYBGwQ',
               'CAACAgIAAxkBAAJAP1-Y75rMlvfFQfvO7rs37-IQU3qDAAKaAAMw1J0R-btImmvuDbMbBA',
               'CAACAgIAAxkBAAJAQl-Y75rR7RGcoDN7p2oUdahYKIVFAAIHBAACRxVoCU5aoy0hvrnIGwQ',
               'CAACAgEAAxkBAAJARV-Y75tLUpFcBUy4LuhOBji_lF37AAISAAP27y4togq5RPoXHUIbBA',
               'CAACAgIAAxkBAAJASF-Y75wau8s-8VdrazQRBTpI3p6OAAKPEQACPLPFBzLcyrxNSGysGwQ',
               'CAACAgIAAxkBAAJAS1-Y76IEqlJ3DZrBNMcn8AWQOYU8AALRAQACPQ3oBPCyBQkFuchBGwQ',
               'CAACAgIAAxkBAAJATl-Y76MOdsCnkFIAAZZQuIbAmN-rWwACngAD9wLIDxjzyiQZP6pbGwQ',
               'CAACAgIAAxkBAAJAUV-Y76kaZUR7R4aO32CWJm8G_CZCAAIyAAMWQmsKn00v9tKrWXkbBA',
               'CAACAgIAAxkBAAJAVF-Y76ojVliBi2M7xsnGjjkGVTuGAAJQAQACzcBIGNnToTej4DmQGwQ',
               'CAACAgEAAxkBAAJAV1-Y8DOsNvEAAe-RHczZdZ7dMsLmXwACDAAD9u8uLaQAATQ2tFWAcRsE'
               ]

# Предупредительные сообщения за голосовые и видео- сообщения
warming_message_base = [', голосовые и видео сообщения запрещены. Не надо их сюда отправлять',
                        ', ну и сколько раз тебе говорить? Без голосовых и видео сообщений тут!',
                        '!!!!!!!!!!!!!!!!!!!! ЗАМОЛЧИ',
                        '!',
                        ', ну ты меня уважаешь? Напиши, а? Боты не умеют слушать. Смотреть тоже']

# Предупредительные сообщения за использование запрещенных слов
warming_message_base2 = ['Обнаружено запрещённое сообщение от',
                         'Давай ты сам это удалишь... Не пиши так больше',
                         'Не, ну это бан... Прощай,']