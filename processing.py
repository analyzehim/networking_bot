# -*- coding: utf-8 -*-
from telegram_proto import Telegram

def network_process(telebot, message):
    if len(message.status) == 2:
        if message.status[1] == "Ask_Contact":
            if message.type == 3:
                telebot.cash.add_profile_contact(message.from_id, message.contact)
                file_name = telebot.get_user_photo(message.from_id)
                telebot.send_ok(message.from_id)
                telebot.cash.add_profile_photo(message.from_id, file_name)
                telebot.ask_name(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Networking Ask_name")
                return True

            elif message.type == 1:
                telebot.cash.add_profile_contact(message.from_id, message.text)
                telebot.send_ok(message.from_id)
                telebot.ask_name(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Networking Ask_name")
                return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "Ask_name":
            if message.type == 1:
                telebot.cash.add_profile_name(message.from_id, message.text)
                telebot.send_ok(message.from_id)
                telebot.ask_mail(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Networking Ask_mail")
                return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "Ask_mail":
            if message.type == 1:
                telebot.cash.add_profile_mail(message.from_id, message.text)
                telebot.send_ok(message.from_id)
                telebot.ask_company(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Networking Ask_company")
                return True

            elif message.type == 2:
                if message.callback_text == "No_Email":
                    telebot.cash.add_profile_mail(message.from_id, "no-mail")
                    telebot.send_ok(message.from_id)
                    telebot.ask_company(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Networking Ask_company")
                    return True
                else:
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True

            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "Ask_company":
            if message.type == 1:
                telebot.cash.add_profile_company(message.from_id, message.text)
                telebot.send_ok(message.from_id)
                telebot.ask_position(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Networking Ask_position")
                return True

            elif message.type == 2:
                if message.callback_text == "No_company":
                    telebot.cash.add_profile_company(message.from_id, "no-company")
                    telebot.send_ok(message.from_id)
                    telebot.ask_position(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Networking Ask_position")
                    return True
                else:
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "Ask_position":
            if message.type == 1:
                telebot.cash.add_profile_position(message.from_id, message.text)
                telebot.send_ok(message.from_id)
                telebot.ask_about(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Networking Ask_about")
                return True

            elif message.type == 2:
                if message.callback_text == "No_position":
                    telebot.cash.add_profile_position(message.from_id, "no-position")
                    telebot.send_ok(message.from_id)
                    telebot.ask_about(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Networking Ask_about")
                    return True
                else:
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "Ask_about":
            if message.type == 1:
                telebot.cash.add_profile_about(message.from_id, message.text)
                telebot.send_ok(message.from_id)
                telebot.ask_photo(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Networking Ask_photo")
                return True

            elif message.type == 2:
                if message.callback_text == "No_about":
                    telebot.cash.add_profile_about(message.from_id, "no-about")
                    telebot.send_ok(message.from_id)
                    telebot.ask_photo(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Networking Ask_photo")
                    return True
                else:
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "Ask_photo":
            if message.type == 2:
                if message.callback_text == "Photo_Profile":
                    telebot.send_ok(message.from_id)
                    profile = telebot.cash.check_profile_status(message.from_id)
                    telebot.send_profile(message.from_id, profile)
                    telebot.cash.set_user_status(message.from_id, "Networking Profile_Show")
                    return True

                elif message.callback_text == "Without_Photo":
                    telebot.cash.add_profile_photo(message.from_id, telebot.standart_photo)
                    telebot.send_ok(message.from_id)
                    profile = telebot.cash.check_profile_status(message.from_id)
                    telebot.send_profile(message.from_id, profile)
                    telebot.cash.set_user_status(message.from_id, "Networking Profile_Show")
                    return True
                else:
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True


            elif message.type == 4:
                telebot.cash.add_profile_photo(message.from_id, message.file_name)
                telebot.send_ok(message.from_id)
                profile = telebot.cash.check_profile_status(message.from_id)
                telebot.send_profile(message.from_id, profile)
                telebot.cash.set_user_status(message.from_id, "Networking Profile_Show")
                return True

            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "Profile_Show":
            if message.type == 1:
                if message.text == "Начать нетворкинг":
                    profile = telebot.cash.get_random_profile(message.from_id)
                    telebot.send_other_profile(message.from_id, profile)
                    telebot.cash.set_user_status(message.from_id, "Networking Profiles")
                    return True

                elif message.text == "Обновить профиль":
                    telebot.ask_contact(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Networking Ask_Contact")
                    return True
                else:
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "Choose":
            if message.type == 1:
                if message.text == "Начать нетворкинг":
                    profile = telebot.cash.get_random_profile(message.from_id)
                    telebot.send_other_profile(message.from_id, profile)
                    telebot.cash.set_user_status(message.from_id, "Networking Profiles")
                    return True
                else:
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "Profiles":
            if message.type == 2:
                if message.callback_text.split(' ')[0] == 'Switch':
                    profile = telebot.cash.check_profile_status(int(message.callback_text.split(' ')[1]))
                    telebot.send_other_profile(message.from_id, profile)
                    telebot.cash.set_user_status(message.from_id, "Networking Profiles")
                    return True
                elif message.callback_text =='Menu':
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True

                else:
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True


        else:
            telebot.send_menu(message.from_id)
            telebot.cash.set_user_status(message.from_id, "Menu")
            return True
    else:
        telebot.send_menu(message.from_id)
        telebot.cash.set_user_status(message.from_id, "Menu")
        return True



def schedule_process(telebot, message):

    if len(message.status) == 2:
        if message.status[1] == "Ask":
            if message.type == 2:
                if message.callback_text == "Time event":
                    telebot.send_event_time(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Schedule Choose_time")
                    return True
                elif message.callback_text == "All events":
                    telebot.send_all_events(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Schedule All_event")
                    return True
                else:
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "All_event":
            if message.type == 2:
                if message.callback_text.split(' ')[0] == 'Like':
                    telebot.cash.add_user_like(message.from_id, int(message.callback_text.split(' ')[1]))
                    telebot.change_like_all(message.from_id, message.callback_message_id, int(message.callback_text.split(' ')[1]))
                    telebot.cash.set_user_status(message.from_id, "Schedule All_event")
                    return True

                elif message.callback_text.split(' ')[0] == 'Dislike':
                    telebot.cash.delete_user_like(message.from_id, int(message.callback_text.split(' ')[1]))
                    telebot.change_like_all(message.from_id, message.callback_message_id, int(message.callback_text.split(' ')[1]))
                    telebot.cash.set_user_status(message.from_id, "Schedule All_event")
                    return True
                else:
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "Choose_time":
            if message.type == 2:
                telebot.send_event_by_time(message.from_id, message.callback_text)
                telebot.cash.set_user_status(message.from_id, "Schedule Show_event")
                return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True

        elif message.status[1] == "Show_event":
            if message.type == 2:
                if message.callback_text.split(' ')[0] == 'Switch':
                    telebot.send_event(message.from_id, int(message.callback_text.split(' ')[1]))
                    telebot.cash.set_user_status(message.from_id, "Schedule Show_event")
                    return True

                elif message.callback_text.split(' ')[0] == 'Like':
                    telebot.cash.add_user_like(message.from_id, int(message.callback_text.split(' ')[1]))
                    telebot.change_like(message.from_id, message.callback_message_id, int(message.callback_text.split(' ')[1]))
                    telebot.cash.set_user_status(message.from_id, "Schedule Show_event")
                    return True

                elif message.callback_text.split(' ')[0] == 'Dislike':
                    telebot.cash.delete_user_like(message.from_id, int(message.callback_text.split(' ')[1]))
                    telebot.change_like(message.from_id, message.callback_message_id, int(message.callback_text.split(' ')[1]))
                    telebot.cash.set_user_status(message.from_id, "Schedule Show_event")
                    return True
                else:
                    telebot.send_menu(message.from_id)
                    telebot.cash.set_user_status(message.from_id, "Menu")
                    return True
            else:
                telebot.send_menu(message.from_id)
                telebot.cash.set_user_status(message.from_id, "Menu")
                return True
        else:
            telebot.send_menu(message.from_id)
            telebot.cash.set_user_status(message.from_id, "Menu")
            return True
    else:
        telebot.send_menu(message.from_id)
        telebot.cash.set_user_status(message.from_id, "Menu")
        return True


def favorite_process(telebot, message):

        if len(message.status) == 2:
            if message.status[1] == "Show":
                if message.type == 2:
                    if message.callback_text.split(' ')[0] == 'Like':
                        telebot.cash.add_user_like(message.from_id, int(message.callback_text.split(' ')[1]))
                        telebot.change_like_all(message.from_id, message.callback_message_id,
                                                int(message.callback_text.split(' ')[1]))
                        telebot.cash.set_user_status(message.from_id, "Favorite All_event")
                        return True

                    elif message.callback_text.split(' ')[0] == 'Dislike':
                        telebot.cash.delete_user_like(message.from_id, int(message.callback_text.split(' ')[1]))
                        telebot.change_like_all(message.from_id, message.callback_message_id,
                                                int(message.callback_text.split(' ')[1]))
                        telebot.cash.set_user_status(message.from_id, "Favorite All_event")
                        return True


        telebot.send_menu(message.from_id)
        telebot.cash.set_user_status(message.from_id, "Menu")
        return True




