# KNNbot
Учебный проект студентов ФКН

v 1.1
---
Добавлены команды:
    /reg [name] - регистрирует пользователя с именем
    /del - удаляет пользователя
    /setpoint - устанавливает количество поинтов пользователю
    /cankick - устанавливает возможность кика. Только для GOD
    /canbanmedia - устанавливает возможность блокировать медиа. Только для GOD
    /canreadonly - устанавливает возможность ставить режим ReadOnly. Только для GOD
    /kick - Кикнуть пользователя с занесением ключа isKicked в БД
---
Полностью переписаны запросы БД
Переписана команда /info. Теперь GOD может смотреть статистику других пользователей
Если пользователь не зарегистрирован, он не сможет общаться в чате
Если пользователь isKicked = 1, при добавлении его в чат, бот автоматически его удалит
Исправлено приветствие пользователя при входе в чат
Исправлен баг с автоматическим ReadOnly по причине мата. Теперь блокирует на время
Время блокировки за мат теперь зависит от количества поинтов
Когда поинтов становится меньше 5, при следующем нарушении пользователь будет кикнут
При регистрации проверяется ID и имя на уникальность
При регистрации проверятся имя на спецсимволы
