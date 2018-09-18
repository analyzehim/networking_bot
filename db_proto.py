import sqlite3
import time
import random
from common_proto import trasform_to_human_time, human_time

class Cash:
    def __init__(self):
        self.con = sqlite3.connect('cash.db')
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS `Messages_id`
                    (`mes_id` INTEGER PRIMARY KEY NOT NULL,
                     `time` VARCHAR(100));
                    ''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS `Users`
                      (`user_id` INTEGER PRIMARY KEY NOT NULL ,
                      `status` VARCHAR(100),
                      `time` INTEGER,
                      `human_time` VARCHAR(100));
                      ''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS `Profiles`
                      (`user_id` INTEGER PRIMARY KEY NOT NULL ,
                      `contact` VARCHAR(100),
                      `name` VARCHAR(100),
                      `mail` VARCHAR(100),
                      `company` VARCHAR(100),
                      `position` VARCHAR(100),
                      `photo` VARCHAR(100),
                      `about` VARCHAR(1000),
                      `time` INTEGER,
                      `human_time` VARCHAR(100));
                      ''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS `Likes`
                              (`user_id` INTEGER PRIMARY KEY NOT NULL ,
                              `likes_event_list` VARCHAR(1000));
                              ''')

        # self.cur.execute('''CREATE TABLE IF NOT EXISTS `Messages`
        #             (`mes_id` INTEGER PRIMARY KEY NOT NULL ,
        #             `body` VARCHAR(100));
        #             ''')
        #
        # self.cur.execute('''CREATE TABLE IF NOT EXISTS `Users`
        #              (`user_id` INTEGER PRIMARY KEY NOT NULL ,
        #              `status` INTEGER);
        #              ''')
        #
        # self.cur.execute('''CREATE TABLE IF NOT EXISTS `Chats`
        #              (`chat_id` INTEGER PRIMARY KEY NOT NULL ,
        #              `chatname` VARCHAR(100));
        #              ''')


    def get_last_mes_id(self):
        self.cur.execute('SELECT max(mes_id) FROM Messages_id')
        ans = self.cur.fetchone()
        last_mes_id = ans[0]
        if last_mes_id:
            return last_mes_id
        else:
            return 0

    def dump_last_mes_id(self, mes_id):
        self.cur.execute('''INSERT OR REPLACE INTO Messages_id VALUES ('{0}','{1}')'''.format(mes_id, human_time()))
        self.con.commit()
        return

    def get_user_status(self, user_id):
            self.cur.execute('SELECT status FROM Users Where user_id = {0}'.format(user_id))
            status = self.cur.fetchone()
            if status:
                return status[0].split(' ')
            else:
                self.set_user_status(user_id, "0")
                return "0"

    def set_user_status(self, user_id, status):
        timestamp = time.time()
        self.cur.execute('''INSERT OR REPLACE INTO Users VALUES
                                ('{0}','{1}','{2}','{3}')'''.format(user_id, status, timestamp, trasform_to_human_time(timestamp)))
        self.con.commit()
        return True


    def add_profile_contact(self, user_id, contact):
        timestamp = time.time()
        self.cur.execute('''INSERT OR REPLACE INTO Profiles(user_id, contact, time, human_time) VALUES
                                ('{0}','{1}','{2}','{3}')'''.format(user_id,
                                                                    contact,
                                                                    timestamp,
                                                                    trasform_to_human_time(timestamp)))
        self.con.commit()
        return True


    def add_profile_name(self, user_id, name):
        timestamp = time.time()
        self.cur.execute('''UPDATE Profiles SET name = '{0}',
                                                time = '{1}',
                                                human_time = '{2}'
                                                WHERE user_id ={3};'''.format(name,
                                                                            timestamp,
                                                                            trasform_to_human_time(timestamp),
                                                                            user_id))
        self.con.commit()
        return True

    def add_profile_mail(self, user_id, mail):
        timestamp = time.time()
        self.cur.execute('''UPDATE Profiles SET mail = '{0}',
                                                time = '{1}',
                                                human_time = '{2}'
                                                WHERE user_id ={3};'''.format(mail,
                                                                            timestamp,
                                                                            trasform_to_human_time(timestamp),
                                                                            user_id))
        self.con.commit()
        return True


    def add_profile_company(self, user_id, company):
        timestamp = time.time()
        self.cur.execute('''UPDATE Profiles SET company = '{0}',
                                                time = '{1}',
                                                human_time = '{2}'
                                                WHERE user_id ={3};'''.format(company,
                                                                            timestamp,
                                                                            trasform_to_human_time(timestamp),
                                                                            user_id))
        self.con.commit()
        return True

    def add_profile_position(self, user_id, position):
        timestamp = time.time()
        self.cur.execute('''UPDATE Profiles SET position = '{0}',
                                                time = '{1}',
                                                human_time = '{2}'
                                                WHERE user_id ={3};'''.format(position,
                                                                            timestamp,
                                                                            trasform_to_human_time(timestamp),
                                                                            user_id))
        self.con.commit()
        return True

    def add_profile_about(self, user_id, about):
        timestamp = time.time()
        self.cur.execute('''UPDATE Profiles SET about = '{0}',
                                                time = '{1}',
                                                human_time = '{2}'
                                                WHERE user_id ={3};'''.format(about,
                                                                            timestamp,
                                                                            trasform_to_human_time(timestamp),
                                                                            user_id))
        self.con.commit()
        return True

    def add_profile_photo(self, user_id, photo):
        timestamp = time.time()
        self.cur.execute('''UPDATE Profiles SET photo = '{0}',
                                                time = '{1}',
                                                human_time = '{2}'
                                                WHERE user_id ={3};'''.format(photo,
                                                                            timestamp,
                                                                            trasform_to_human_time(timestamp),
                                                                            user_id))
        self.con.commit()
        return True

    def check_profile_status(self, user_id):
        self.cur.execute('SELECT * FROM Profiles Where user_id = {0}'.format(user_id))
        status = self.cur.fetchone()
        if status:
            if status[1] and status[2] and status[3] and status[4] and status[5] and status[6] and status[7]:
                try:
                    text ="{0},{1},{2},{3},{4},{5},{6},{7}".format(status[0], status[1].encode('utf-8'),
                                                               status[2].encode('utf-8'),
                                                               status[3].encode('utf-8'), status[4].encode('utf-8'),
                                                               status[5].encode('utf-8'),
                                                               status[6].encode('utf-8'), status[7].encode('utf-8'))
                    return {"user_id": status[0],
                            "contact": status[1].encode('utf-8'),
                            "name": status[2].encode('utf-8'),
                            "mail": status[3].encode('utf-8'),
                            "company": status[4].encode('utf-8'),
                            "position": status[5].encode('utf-8'),
                            "photo": status[6].encode('utf-8'),
                            "about": status[7].encode('utf-8')}
                except:
                    return False
            else:
                return False
        else:
            return False

    def get_random_profile(self, from_id):
        self.cur.execute('SELECT * FROM Profiles')
        status = self.cur.fetchall()
        while True:
            profile = random.choice(status)
            if profile[0] != from_id:
                profile_body = self.check_profile_status(profile[0])
                if profile_body:
                    return profile_body
        else:
            return False

    def get_prev_profile(self, profile_id):
        self.cur.execute('SELECT * FROM Profiles')
        profile_list = self.cur.fetchall()
        prev_id = 0
        for profile in profile_list:
            if self.check_profile_status(profile[0]):
                if (profile[0]<profile_id) and (profile[0]>prev_id):
                    prev_id = profile[0]
        return prev_id

    def get_next_profile(self, profile_id):
        self.cur.execute('SELECT * FROM Profiles')
        profile_list = self.cur.fetchall()
        next_id = 100000000000
        for profile in profile_list:
            if self.check_profile_status(profile[0]):
                if (profile[0]>profile_id) and (profile[0]<next_id):
                    next_id = profile[0]
        return next_id


    def get_first_profile_id(self):
        self.cur.execute('SELECT MIN(user_id) FROM Profiles')
        return int(self.cur.fetchone()[0])

    def get_last_profile_id(self):
        self.cur.execute('SELECT MAX(user_id) FROM Profiles')
        return int(self.cur.fetchone()[0])

    def get_likes(self, user_id):
        self.cur.execute('SELECT likes_event_list FROM Likes Where user_id = {0}'.format(user_id))
        status = self.cur.fetchone()
        if status:
            event_list = status[0]
            return [int(event_id) for event_id in str(event_list)[1:-1].split(',')]
        else:
            return []



    def add_user_like(self, user_id, event_id):
        likes = self.get_likes(user_id)
        if likes:
            if not event_id in likes:
                likes.append(event_id)
            self.cur.execute('''UPDATE Likes SET likes_event_list = '{0}' WHERE user_id ={1};'''.format(likes, user_id))
            self.con.commit()
            return True
        else:
            event_list = str([event_id])
            self.cur.execute('''INSERT OR REPLACE INTO LIKES(user_id, likes_event_list) VALUES
                                            ('{0}','{1}')'''.format(user_id, event_list))
            self.con.commit()
            return True

    def delete_user_like(self, user_id, event_id):
        likes = self.get_likes(user_id)
        if likes:
            try:
                likes.remove(event_id)
            except:
                pass
            self.cur.execute('''UPDATE Likes SET likes_event_list = '{0}' WHERE user_id ={1};'''.format(likes, user_id))
            self.con.commit()
            return True
        else:
            return True

    def get_user_list(self):
        self.cur.execute('SELECT DISTINCT(user_id) FROM Users')
        user_list = self.cur.fetchall()
        return [int(user[0]) for user in user_list]

    def get_photo_path(self, user_id):
        self.cur.execute('''SELECT photo FROM Profiles WHERE user_id ={0};'''.format(user_id))
        photo_path = self.cur.fetchone()
        if photo_path:
            return photo_path[0]
        else:
            return False