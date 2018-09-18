# -*- coding: utf-8 -*-
import requests
import time
import random
import socket
import xml.etree.ElementTree as ET
import os
import logging
import shutil
from common_proto import trasform_to_human_time
from conference import Program, program_json, conference_about, wifi_text
from db_proto import Cash

INTERVAL = 0.5
LINE_SIZE = 3

def parse_program(programs):
    mas = sorted(list(programs))
    keyboard = []
    keyboard.append( [{'text': mas[0], 'callback_data': mas[0]}] )
    for elem in mas[1:]:
        if len(keyboard[-1])!= LINE_SIZE:
            keyboard[-1].append({'text': elem, 'callback_data': elem})
        else:
            keyboard.append([{'text': elem, 'callback_data': elem}])
    return keyboard

def create_inline(programs):
    mas = sorted(list(programs))
    LINE_SIZE = 3
    keyboard = []
    keyboard.append( [{'text': mas[0], 'callback_data': mas[0]}] )
    for elem in mas[1:]:
        if len(keyboard[-1])!= LINE_SIZE:
            keyboard[-1].append({'text': elem, 'callback_data': elem})
        else:
            keyboard.append([{'text': elem, 'callback_data': elem}])
    return keyboard

def get_token(tree):
    root = tree.getroot()
    token = root.findall('telegram_token')[0].text
    return token

def get_type(tree):
    root = tree.getroot()
    type = root.findall('type')[0].text
    return int(type)

def get_admin(tree):
    root = tree.getroot()
    admin_id = root.findall('telegram_admin_id')[0].text
    return int(admin_id)


def get_proxies(tree):
    root = tree.getroot()
    proxy_url = root.findall('proxy')[0].text
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
    return proxies


def check_mode(tree):
    import requests

    try:
        requests.get('https://www.google.com')
        return False
    except:
        proxies = get_proxies(tree)
        requests.get('https://www.google.com', proxies=proxies)
        return True


###
#   TYPE
#   1 - Economy
#   2 - Standart
#   3 - Busieness
###

class Telegram:
    def __init__(self):
        if not os.path.exists("photos"):
            os.makedirs("photos")
        self.cfgtree = ET.parse('private_config.xml')
        self.type = get_type(self.cfgtree)
        self.proxy = check_mode(self.cfgtree)
        self.TOKEN = get_token(self.cfgtree)
        self.URL = 'https://api.telegram.org/bot'
        #self.URL = 'http://127.0.0.1:5000/bot'
        self.admin_id = get_admin(self.cfgtree)
        self.standart_photo = "photos//nophoto.png"
        self.offset = 0
        self.interval = 1
        self.host = socket.getfqdn()
        self.Interval = INTERVAL
        self.emoji_list = ['🌏', '🌐', '🏙', '📱', '💻', '⌨']
        self.cash = Cash()
        self.program = Program(program_json)
        self.conference_about = conference_about
        self.wifi_text = wifi_text
        #
        # Logging
        #
        logging.basicConfig(filename='new.log', format='%(asctime)s %(levelname)s %(message)s', level=logging.ERROR)
        self.logger = logging.getLogger('new.log')
        self.logger.setLevel(logging.ERROR)


        if self.proxy:
            self.proxies = get_proxies(self.cfgtree)
            self.send_text(self.admin_id, "running")
            self.log_event("Init completed with proxy, host: " + str(self.host))
        else:
            self.send_text(self.admin_id, "running")
            self.log_event("Init completed, host: " + str(self.host))


    def log_event(self, text, type_logging=''):
        if type_logging == 'e':
            print "ERROR: ", text
            self.logger.error(text)
        elif type_logging == 'i':
            print "INFO", text
            self.logger.error(text)
        else:
            print "DEBUG", text
            self.logger.error(text)
        return True

    def edit_keyboard(self, chat_id, message_id, keyboard):

        json_data = {"chat_id": chat_id, "message_id": message_id,
                     "reply_markup": {"inline_keyboard": keyboard, "one_time_keyboard": True, "resize_keyboard": True}}

        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/editMessageReplyMarkup', json=json_data,
                                    proxies=self.proxies)  # HTTP request with proxy
        else:
            request = requests.post(self.URL + self.TOKEN + '/editMessageReplyMarkup', json=json_data)

        if not request.status_code == 200:  # Check server status
            self.log_event("REAL ERROR" + request.text, "e")
            print "Error", request.text
            return False
        return request.json()['ok']  # Check API

    def send_text_with_keyboard(self, chat_id, text, keyboard):
        json_data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML",
                     "reply_markup": {"keyboard": keyboard, "one_time_keyboard": True, "resize_keyboard": True}}
        if not self.proxy:  # no proxy
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data)  # HTTP request

        else:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data,
                                    proxies=self.proxies)  # HTTP request with proxy

        if not request.status_code == 200:  # Check server status
            self.log_event("REAL ERROR" + request.text, "e")
            print "Error", request.text
            return False
        return request.json()['ok']  # Check API

    def send_text_with_inline_keyboard(self, chat_id, text, keyboard):
        '''
        Keyboard example:
         [
         [  {'text': 1, 'callback_data': 1},
            {'text': 2, 'callback_data': 2},
            {'text': 3, 'callback_data': 3} ]
         ]
        '''
        # try:
        #     self.log_event('Sending to %s: %s; keyboard: %s' % (chat_id, text, keyboard))  # Logging
        # except:
        #     self.log_event('Error with LOGGING')
        json_data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML",
                     "reply_markup": {"inline_keyboard": keyboard, "one_time_keyboard": True, "resize_keyboard": True}}
        if not self.proxy:  # no proxy
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data)  # HTTP request

        else:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data,
                                    proxies=self.proxies)  # HTTP request with proxy

        if not request.status_code == 200:  # Check server status
            self.log_event("REAL ERROR" + request.text, "e")
            print "Error", request.text
            return False
        return request.json()['ok']  # Check API

    def get_updates(self):
        data = {'offset': self.offset + 1, 'limit': 5, 'timeout': 0}
        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/getUpdates', data=data, proxies=self.proxies)
        else:
            request = requests.post(self.URL + self.TOKEN + '/getUpdates', data=data)
        if (not request.status_code == 200) or (not request.json()['ok']):
            return False
        updates_list = []
        if not request.json()['result']:
            #self.log_event("No updates", 'i')
            return updates_list
        else:
            #self.log_event("GET UPDATE: ", request.text)
            for update in request.json()['result']:
                try:
                    telegram_update = TelegramUpdate(update, self)
                    self.offset = telegram_update.update_id
                    if telegram_update.type == 0:
                        self.log_event("GET ERROR UPDATE:", 'e')
                        self.log_event(request.json(), 'e')
                    else:
                        #self.log_event(request.json(), 'i')
                        updates_list.append(telegram_update)
                except:
                    self.log_event(update, "e")
        return updates_list

    def send_photo(self, chat_id, text, image_path):
        self.log_event('Sending photo to %s: %s' % (chat_id, image_path))  # Logging
        data = {"chat_id": chat_id,
                "parse_mode": "HTML",
                "caption": text}
        try:
            files = {'photo': (image_path, open(image_path, "rb"))}
        except IOError:
            files = {'photo': (self.standart_photo, open(self.standart_photo, "rb"))}

        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/sendPhoto', data=data, files=files,
                                    proxies=self.proxies)  # HTTP request with proxy)
        else:
            request = requests.post(self.URL + self.TOKEN + '/sendPhoto', data=data, files=files)  # HTTP request
        if not request.status_code == 200:  # Check server status
            self.log_event("REAL ERROR" + request.text, "e")
            print "Error", request.text
            return False
        return request.json()['ok']  # Check API


    def send_text(self, chat_id, text):
        data = {'chat_id': chat_id, 'text': text, "parse_mode": "HTML"}  # Request create
        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data,
                                    proxies=self.proxies)  # HTTP request with proxy
        else:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', data=data)  # HTTP request
        if not request.status_code == 200:  # Check server status
            self.log_event("REAL ERROR" + request.text, "e")
            print "Error", request.text
            return False
        return request.json()['ok']  # Check API

    def send_menu(self, chat_id):
        emoji = random.choice(self.emoji_list)
        self.send_text_with_keyboard(chat_id, emoji, [["🏠 Меню"]])
        menu_keyboard = [
            [
                {'text': "📅 Программа", 'callback_data': "View the schedule"},
                {'text': "🌟 Моё расписание", 'callback_data': "My schedule"}
            ],
            [
                {'text': "📰 О конференции", 'callback_data': "About"}
            ],
            [
                {'text': "📶 Wi-Fi", 'callback_data': "Wifi"}
            ],
            [
                {'text': "🔔 Чат конференции", 'url': "https://t.me/joinchat/EF-QtE0QaFlHe_jFesMfVw"}
            ],
            [
                {'text': "👥 Нетворкинг", 'callback_data': "Networking"}
            ],
            [
                {'text': "👔 Заказать бота", 'url': "https://marketingbot.ru/"}
            ]
         ]
        self.send_text_with_inline_keyboard(chat_id, "<b> AI Conference </b>", menu_keyboard)
        self.log_event("[{0}] SEND_MENU to {0})".format(chat_id))

        return True


    def ask_contact(self, chat_id):
        self.send_text(chat_id, "<b> Телефон [шаг 1 из 7] </b>")
        json_data = {"chat_id": chat_id,
                     "text": "Пришлите, пожалуйста, свой телефон",
                     "parse_mode": "Markdown",
                     "reply_markup": {"one_time_keyboard": True,
                                      "keyboard": [[{"text": "Прислать телефонный номер", "request_contact": True}],
                                                   ["🏠 Меню"]]
                                      }
                     }

        if not self.proxy:  # no proxy
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data)  # HTTP request

        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/sendMessage', json=json_data,
                                    proxies=self.proxies)  # HTTP request with proxy

        if not request.status_code == 200:  # Check server status
            self.log_event("REAL ERROR" + request.text, "e")
            print "Error", request.text
            return False
        self.log_event("[{0}] ASK_CONTACT to {0})".format(chat_id))
        return request.json()['ok']  # Check API

    def ask_name(self, chat_id):
        self.send_text(chat_id, "<b> ФИО [шаг 2 из 7] </b>")
        self.send_text_with_keyboard(chat_id, "Пришлите, пожалуйста, свое ФИО", [["🏠 Меню"]])
        self.log_event("[{0}] ASK_NAME to {0}".format(chat_id))
        return

    def ask_mail(self, chat_id):
        keyboard = [[{'text': "Пропустить", 'callback_data': "No_Email"}]]
        self.send_text_with_keyboard(chat_id, "<b> E-Mail [шаг 3 из 7] </b>", [["🏠 Меню"]])
        self.send_text_with_inline_keyboard(chat_id, "Пришлите, пожалуйста, свой e-mail", keyboard)
        self.log_event("[{0}] ASK_MAIL to {0}".format(chat_id))
        return

    def ask_company(self, chat_id):
        keyboard = [[{'text': "Пропустить", 'callback_data': "No_company"}]]
        self.send_text_with_keyboard(chat_id, "<b> Компания [шаг 4 из 7] </b>", [["🏠 Меню"]])
        self.send_text_with_inline_keyboard(chat_id, "В какой компании вы работаете?", keyboard)
        self.log_event("[{0}] ASK_COMPANY to {0}".format(chat_id))
        return

    def ask_position(self, chat_id):
        keyboard = [[{'text': "Пропустить", 'callback_data': "No_position"}]]
        self.send_text_with_keyboard(chat_id, "<b> Компания [шаг 5 из 7] </b>", [["🏠 Меню"]])
        self.send_text_with_inline_keyboard(chat_id, "На какой позиции вы работаете?", keyboard)
        self.log_event("[{0}] ASK_POSITION to {0}".format(chat_id))
        return

    def ask_about(self, chat_id):
        text = '''Расскажите немного о себе.
Что вы ищите? О каких темах было бы интересно поговорить? В каких темах вы разбираетесь?'''
        keyboard = [[{'text': "Пропустить", 'callback_data': "No_about"}]]
        self.send_text_with_keyboard(chat_id, "<b> О себе [шаг 6 из 7] </b>", [["🏠 Меню"]])
        self.send_text_with_inline_keyboard(chat_id, text, keyboard)
        self.log_event("[{0}] ASK_ABOUT to {0}".format(chat_id))
        return

    def ask_photo(self, chat_id):
        photo_path = self.cash.get_photo_path(chat_id)
        if not photo_path:
            photo_path = self.standart_photo
        self.send_photo(chat_id, '<b> Фото [шаг 7 из 7] </b>', photo_path)
        keyboard = [
            [
                {'text': "Использовать фото профиля", 'callback_data': "Photo_Profile"}
            ],
            [
                {'text': "Хочу без фото", 'callback_data': "Without_Photo"}
            ],
            [
                {'text': "🏠 Меню", 'callback_data': "Menu"}
            ]
            ]
        self.send_text_with_inline_keyboard(chat_id, "Выберите фото из профиля или пришлите другое", keyboard)
        self.log_event("[{0}] ASK_PHOTO to {0})".format(chat_id))
        return

    def send_about(self, chat_id):
        self.send_text_with_keyboard(chat_id, self.conference_about, [["🏠 Меню"]])
        self.log_event("[{0}] SEND_ABOUT to {0})".format(chat_id))
        return

    def send_wifi(self, chat_id):
        self.send_text_with_keyboard(chat_id, self.wifi_text, [["🏠 Меню"]])
        self.log_event("[{0}] SEND_WIFI to {0})".format(chat_id))
        return

    def send_profile(self, chat_id, profile):
        self.send_text_with_keyboard(chat_id, "Ваш профиль:", [["Начать нетворкинг"], ["Обновить профиль"], ["🏠 Меню"]])
        profile_id = profile["user_id"]
        name = profile["name"]
        contact = profile["contact"]
        company = profile["company"]
        mail = profile["mail"]
        position = profile["position"]
        photo = profile["photo"]
        about = profile["about"]

        name_text = '''<b>Имя: {0}</b>\n'''.format(name)

        contact_text = '''<b>Телефон: {0}</b>\n'''.format(contact)

        if company == "no-company":
            company_text = ''
        else:
            company_text = "<b>Компания: </b>{0}\n".format(company)

        if position == "no-position":
            position_text = ''
        else:
            position_text = "<b>Позиция: </b>{0}\n".format(position)

        if mail == "no-mail":
            mail_text = ''
        else:
            mail_text = "<b>e-mail: </b>{0}\n".format(mail)

        if about == "no-about":
            about_text = ''
        else:
            about_text = "<b>О себе: </b>{0}\n".format(about)

        text = name_text + mail_text + company_text + position_text + contact_text + about_text

        self.send_photo(chat_id, text, photo)
        self.log_event("[{0}] SEND_OTHER_PROFILE to {0} profile {1})".format(chat_id, profile_id))
        return True

    def send_other_profile(self, chat_id, profile):
        profile_id = profile["user_id"]
        first_profile_id = self.cash.get_first_profile_id()
        last_profile_id = self.cash.get_last_profile_id()

        name = profile["name"]
        contact = profile["contact"]
        company = profile["company"]
        mail = profile["mail"]
        position = profile["position"]
        photo = profile["photo"]
        if not mail == "no-mail":
            text = '''<b>Имя: {0}</b>\n
<b>e-mail: </b>{1}\n
<b>Компания: </b>{2}\n
<b>Должность: </b>{3}\n
<b>Телефон: </b>{4}'''.format(name, mail, company, position, contact)
        else:
            text = '''<b>Имя: {0}</b>\n
<b>Компания: </b>{1}\n
<b>Должность: </b>{2}\n
<b>Телефон: </b>{3}'''.format(name, company, position, contact)

        self.send_photo(chat_id, "", photo)


        prev_profile = self.cash.get_prev_profile(profile_id)
        next_profile = self.cash.get_next_profile(profile_id)
        # print "ID: ", profile_id
        # print "Prev: ", prev_profile
        # print "Next: ", next_profile
        if profile_id == first_profile_id:
            inline_keyboard = [
                [
                    {'text': "->", 'callback_data': "Switch {0}".format(next_profile)}
                ],
                [
                    {'text': "🏠 Меню", 'callback_data': "Menu"}
                ]
             ]
        elif profile_id == last_profile_id:
            inline_keyboard = [
                [
                    {'text': "<-", 'callback_data': "Switch {0}".format(prev_profile)}
                ],
                [
                    {'text': "🏠 Меню", 'callback_data': "Menu"}
                ]
             ]
        else:
            inline_keyboard = [
                [
                    {'text': "<-", 'callback_data': "Switch {0}".format(prev_profile)},
                    {'text': "-> ", 'callback_data': "Switch {0}".format(next_profile)}
                ],
                [
                    {'text': "🏠 Меню", 'callback_data': "Menu"}
                ]
            ]
        self.send_text_with_inline_keyboard(chat_id, text, inline_keyboard)
        self.log_event("[{0}] SEND_OTHER_PROFILE to {0} profile {1} (prev profile: {2}, next profile:{3})".format(chat_id,
                                                                                              profile_id,
                                                                                              prev_profile,
                                                                                              next_profile))
        return True


    def get_file(self, file_link):
        #self.log_event('Getting file {0}'.format(file_link))  # Logging
        data = {'file_id': file_link}  # Request create
        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/getFile', data=data,
                                    proxies=self.proxies)  # HTTP request with proxy
        else:
            request = requests.post(self.URL + self.TOKEN + '/getFile', data=data)  # HTTP request
        print request.json()
        file_path = request.json()['result']['file_path']
        download_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(self.TOKEN, file_path)
        print download_url
        file_name = file_path.split('/')[-1]
        if self.proxy:
            request = requests.get(download_url, stream=True, proxies=self.proxies)  # HTTP request with proxy
        else:
            request = requests.get(download_url, stream=True)  # HTTP request
        with open("photos//" + file_name, 'wb') as f:
            shutil.copyfileobj(request.raw, f)
        self.log_event("File {0} getting".format(file_name))
        return "photos//" + file_name

    def send_event(self, user_id, event_id_str):
        event_id = int(event_id_str)
        event = self.program.get_event_by_id(event_id)
        user_likes = self.cash.get_likes(user_id)
        if event_id in user_likes:
            like_text = "Удалить из избранного"
            like_data = "Dislike {0}".format(event_id_str)
        else:
            like_text = "В избранное"
            like_data = "Like {0}".format(event_id_str)


        if event_id == 1:
            inline_keyboard = [
                [
                    {'text': like_text, 'callback_data': like_data},
                    {'text': "->", 'callback_data': "Switch {0}".format(event_id+1)}
                ]
             ]
        elif event_id == len(self.program.event_list):
            inline_keyboard = [
                [
                    {'text': "<-", 'callback_data': "Switch {0}".format(event_id - 1)},
                    {'text': like_text, 'callback_data': like_data}
                ]
             ]
        else:
            inline_keyboard = [
                [
                    {'text': "<-", 'callback_data': "Switch {0}".format(event_id - 1)},
                    {'text': like_text, 'callback_data': like_data},
                    {'text': "-> ", 'callback_data': "Switch {0}".format(event_id + 1)}
                ]
            ]
        text = event.html_text
        self.send_text_with_inline_keyboard(user_id, text, inline_keyboard)
        self.log_event("[{0}] SEND_EVENT to {0} event {1}".format(user_id, event_id))
        return True

    def change_like(self, user_id, message_id, event_id_str):
        event_id = int(event_id_str)
        event = self.program.get_event_by_id(event_id)
        user_likes = self.cash.get_likes(user_id)
        if event_id in user_likes:
            like_text = "Удалить из избранного"
            like_data = "Dislike {0}".format(event_id_str)
        else:
            like_text = "В избранное"
            like_data = "Like {0}".format(event_id_str)


        if event_id == 1:
            inline_keyboard = [
                [
                    {'text': like_text, 'callback_data': like_data},
                    {'text': "->", 'callback_data': "Switch {0}".format(event_id+1)}
                ]
             ]
        elif event_id == len(self.program.event_list):
            inline_keyboard = [
                [
                    {'text': "<-", 'callback_data': "Switch {0}".format(event_id - 1)},
                    {'text': like_text, 'callback_data': like_data}
                ]
             ]
        else:
            inline_keyboard = [
                [
                    {'text': "<-", 'callback_data': "Switch {0}".format(event_id - 1)},
                    {'text': like_text, 'callback_data': like_data},
                    {'text': "-> ", 'callback_data': "Switch {0}".format(event_id + 1)}
                ]
            ]
        text = event.html_text
        self.edit_keyboard(user_id, message_id, inline_keyboard)
        self.log_event("[{0}] CHANGE_LIKE to {0} message_id {1}".format(user_id, event_id))
        return True



    def change_like_all(self, user_id, message_id, event_id_str):
        event_id = int(event_id_str)
        user_likes = self.cash.get_likes(user_id)
        if event_id in user_likes:
            like_text = "Удалить из избранного"
            like_data = "Dislike {0}".format(event_id_str)
        else:
            like_text = "В избранное"
            like_data = "Like {0}".format(event_id_str)


        if event_id == 1:
            inline_keyboard = [
                [
                    {'text': like_text, 'callback_data': like_data}
                ]
             ]
        elif event_id == len(self.program.event_list):
            inline_keyboard = [
                [
                    {'text': like_text, 'callback_data': like_data}
                ]
             ]
        else:
            inline_keyboard = [
                [
                    {'text': like_text, 'callback_data': like_data}
                ]
            ]
        self.edit_keyboard(user_id, message_id, inline_keyboard)
        self.log_event("[{0}] CHANGE_LIKE_ALL to {0} message_id {1}".format(user_id, event_id))
        return True

    def send_schedule_ask(self, user_id):
        emoji = random.choice(self.emoji_list)
        event_keyboard = [
            [
                {'text': "Вся программа", 'callback_data': "All events"},
                {'text': "По времени", 'callback_data': "Time event"}
            ]
         ]
        self.send_text_with_inline_keyboard(user_id, emoji, event_keyboard)
        self.log_event("[{0}] SEND_SCHEDULE_ASK to {0}".format(user_id))
        return True

    def send_event_time(self, user_id):
        time_list = [event.time for event in self.program.event_list]
        emoji = random.choice(self.emoji_list)
        time_keyboard = parse_program(time_list)
        self.send_text_with_inline_keyboard(user_id, emoji, time_keyboard)
        self.log_event("[{0}] SEND_EVENT_TIME to {0}".format(user_id))
        return True


    def send_event_by_time(self, user_id, period):
        event = self.program.get_events_by_time(period)
        if event:
            self.send_event(user_id, event.id)
            return True
        else:
            return False

    def send_all_events(self, user_id):
        for event in self.program.event_list:
            event_id = event.id
            user_likes = self.cash.get_likes(user_id)
            if event_id in user_likes:
                like_text = "Удалить из избранного"
                like_data = "Dislike {0}".format(event_id)
            else:
                like_text = "В избранное"
                like_data = "Like {0}".format(event_id)

            inline_keyboard = [[{'text': like_text, 'callback_data': like_data}]]

            text = event.html_text
            self.send_text_with_inline_keyboard(user_id, text, inline_keyboard)
        self.log_event("[{0}] SEND_ALL_EVENTS to {0}".format(user_id))
        return True


    def send_favorite(self, user_id):
        user_likes = self.cash.get_likes(user_id)
        if not user_likes:
            self.send_text(user_id, "Вы пока ничего не добавили в избранное")
            return True
        favorite_list = []
        for event in self.program.event_list:
            event_id = event.id
            if not event_id in user_likes:
                continue
            favorite_list.append(event_id)

            if event_id in user_likes:
                like_text = "Удалить из избранного"
                like_data = "Dislike {0}".format(event_id)
            else:
                like_text = "В избранное"
                like_data = "Like {0}".format(event_id)

            inline_keyboard = [[{'text': like_text, 'callback_data': like_data}]]

            text = event.html_text
            self.send_text_with_inline_keyboard(user_id, text, inline_keyboard)
        self.log_event("[{0}] SEND_FAVORITE to {0}, FAVORITE_LIST={1}".format(user_id, str(favorite_list)))
        return True

    def get_user_photo(self, user_id):
        data = {'user_id': user_id}  # Request create
        if self.proxy:
            request = requests.post(self.URL + self.TOKEN + '/getUserProfilePhotos', data=data,
                                    proxies=self.proxies)  # HTTP request with proxy
        else:
            request = requests.post(self.URL + self.TOKEN + '/getUserProfilePhotos', data=data)  # HTTP request
        if not request.status_code == 200:  # Check server status
            self.log_event("REAL ERROR" + request.text, "e")
            print "Error", request.text
            return False
        file_size = 0
        try:
            for photo in request.json()['result']['photos'][0]:
                if photo["file_size"] > file_size:
                    file_id = photo["file_id"]
            file_name = self.get_file(file_id)
            return file_name
        except:
            return self.standart_photo

    def send_ok(self, user_id):
        ok_text = "Принято 👌"
        self.send_text(user_id, ok_text)
        self.log_event("[{0}] SEND_OK to {0}".format(user_id))
        return True





class TelegramUpdate:
    def __init__(self, update, telebot):
        self.update_id = update["update_id"]
        self.type = 0
        if "message" in update:
            if 'text' in update['message']:
                self.type = 1
                self.text = update['message']['text'].encode("utf-8")
                self.text_unicode = update['message']['text']
                self.from_id = update['message']['from']['id']

                self.from_name = "Anonim"
                if 'first_name' in update['message']['from']:
                    self.from_name = update['message']['from']['first_name']
                if 'last_name' in update['message']['from']:
                    self.from_name = update['message']['from']['last_name']
                if 'username' in update['message']['from']:
                    self.from_name = update['message']['from']['username']

                self.message_id = update['message']['message_id']
                self.date = update['message']['date']
                self.human_date = trasform_to_human_time(self.date)
                self.status = telebot.cash.get_user_status(self.from_id)
                return

            elif 'contact' in update['message']:
                self.type = 3
                self.contact = update['message']['contact']['phone_number']
                self.from_id = update['message']['chat']['id']

                self.from_name = "Anonim"
                if 'first_name' in update['message']['chat']:
                    self.from_name = update['message']['chat']['first_name']
                if 'last_name' in update['message']['chat']:
                    self.from_name = update['message']['chat']['last_name']
                if 'username' in update['message']['chat']:
                    self.from_name = update['message']['chat']['username']

                self.date = update['message']['date']
                self.human_date = trasform_to_human_time(self.date)
                self.status = telebot.cash.get_user_status(self.from_id)
                return

            elif "photo" in update['message']:
                self.type = 4
                size = 0
                for photo in update['message']['photo']:
                    if photo["file_size"] > size:
                        file_id = photo['file_id']
                self.from_id = update['message']['chat']['id']  # Chat ID
                self.file_name = telebot.get_file(file_id)

                self.from_name = "Anonim"
                if 'first_name' in update['message']['chat']:
                    self.from_name = update['message']['chat']['first_name']
                if 'last_name' in update['message']['chat']:
                    self.from_name = update['message']['chat']['last_name']
                if 'username' in update['message']['chat']:
                    self.from_name = update['message']['chat']['username']

                self.status = telebot.cash.get_user_status(self.from_id)
                self.date = update['message']['date']
                self.human_date = trasform_to_human_time(self.date)

            else:
                return

        elif "callback_query" in update:
            self.type = 2
            self.callback_text = update['callback_query']['data']
            self.callback_message_id = update['callback_query']['message']['message_id']
            self.callback_message_date = update['callback_query']['message']['date']
            self.callback_message_text = update['callback_query']['message']['text'].encode("utf-8")
            self.callback_message_text_unicode = update['callback_query']['message']['text']
            self.callback_message_human_date = trasform_to_human_time(self.callback_message_date)
            self.from_id = update['callback_query']['from']['id']

            self.from_name = "Anonim"
            if 'first_name' in update['callback_query']['from']:
                self.from_name = update['callback_query']['from']['first_name']
            if 'last_name' in update['callback_query']['from']:
                self.from_name = update['callback_query']['from']['last_name']
            if 'username' in update['callback_query']['from']:
                self.from_name = update['callback_query']['from']['username']

            self.status = telebot.cash.get_user_status(self.from_id)
            return
        else:
            telebot.log_event("GET STRANGE UPDATE: {0}".format(update))
            return

    def __str__(self):
        if self.type == 1:
            return "[mes] {0} (id{1}) send message: {2} on [{3}]".format(self.from_name,
                                                               self.from_id,
                                                               self.text,
                                                               self.human_date)
        elif self.type == 2:
            return "[callback] {0} (id{1}) callback: text={2}, message_id ={3}, message_date = {4} ".format(
                                                                self.from_name,
                                                                self.from_id,
                                                                self.callback_text,
                                                                self.callback_message_id,
                                                                self.callback_message_human_date)
        elif self.type == 3:
            return "[contact] {0} (id{1}) contact: {2}, message_date = {3} ".format(
                                                                self.from_name,
                                                                self.from_id,
                                                                self.contact,
                                                                self.human_date)
        elif self.type == 4:
            return "[photo] {0} (id{1}) photo: {2}, message_date = {3} ".format(
                                                                self.from_name,
                                                                self.from_id,
                                                                self.file_name,
                                                                self.human_date)
        else:
            return "UNKNOWN MESSAGE TYPE"