# -*- coding: utf-8 -*-
from telegram_proto import Telegram
telebot = Telegram()
text = '''Дорогие друзья, рассылаем материалы по мотивам нашей конференции! \n
Презентации спикеров: https://drive.google.com/file/d/1ZZjLUez36AyjAlLF8nu_AWlJfilvYO-J/view \n
Фотоотчет: https://aiconference.ru/ru/photo2018'''

users_list = telebot.cash.get_user_list()
for user in users_list:
    try:
        telebot.send_text(user, text)
    except:
        pass