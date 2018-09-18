# -*- coding: utf-8 -*-
from telegram_proto import Telegram
from db_proto import Cash
from common_proto import get_exception
from processing import network_process, schedule_process, favorite_process
import time



def process(message):
    log_str = "[{0}] STATUS: ".format(message.from_id) + str(message.status) + ' ' + "COMMING MESSAGE: " + str(message)
    telebot.log_event(log_str)
    # if not message.from_id == telebot.admin_id:
    #     telebot.log_event(message, "e")
    #     #telebot.send_text(message.from_id, "Ты кто? Не пиши мне больше.")
    #     return True


    if message.status[0] == "0":
        telebot.send_menu(message.from_id)
        telebot.cash.set_user_status(message.from_id, "Menu")
        return True

    if message.type == 1:
        if message.text == "🏠 Меню":
            telebot.send_menu(message.from_id)
            telebot.cash.set_user_status(message.from_id, "Menu")
            return True

    if message.status[0] == "Menu":
        if message.type == 2:
            if message.callback_text == "View the schedule":
                telebot.send_schedule_ask(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Schedule Ask")
                return True

            elif message.callback_text == "My schedule":
                telebot.send_favorite(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Favorite Show")
                return True

            elif message.callback_text == "About":
                telebot.send_about(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

            elif message.callback_text == "Wifi":
                telebot.send_wifi(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

            elif message.callback_text == "Networking":
                profile = telebot.cash.check_profile_status(message.from_id)
                if not profile:
                    telebot.ask_contact(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Networking Ask_Contact")
                else:
                    telebot.send_profile(message.from_id, profile)
                    telebot.cash.set_user_status(message.from_id, "Networking Profile_Show")
                return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        else:
            telebot.send_menu(message.from_id)
            telebot.cash.set_user_status(message.from_id, "Menu")
            return True

    elif message.status[0] == "Networking":
        network_process(telebot, message)
        return True

    elif message.status[0] == "Schedule":
        schedule_process(telebot, message)
        return True

    elif message.status[0] == "Favorite":
        favorite_process(telebot, message)
        return True

    else:
        telebot.send_menu(message.from_id)
        telebot.cash.set_user_status(message.from_id, "Menu")
        return True










if __name__ == "__main__":
    telebot = Telegram()
    while True:
        try:
            telegram_message_list = telebot.get_updates()
            if telegram_message_list:
                for telegram_message in telegram_message_list:
                    process(telegram_message)
            else:
                pass
            time.sleep(telebot.interval)
        except Exception as e:
            telebot.log_event(get_exception(), 'e')
