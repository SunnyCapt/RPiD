import json
import os
import time
import logging

import math
import vk
from vk.exceptions import VkAPIError

import config

logger = logging.getLogger("general")

PAUSE_TIME = 1.3


class VkMixin:
    def __init__(self):
        self.api: vk.API = None
        raise NotImplemented

    def __check(self):
        raise NotImplemented


class Account(VkMixin):
    __LAST_CALL_TIME = int(time.time())

    def __new__(cls, *arg, **args):
        if cls is Account:
            return None
        return object.__new__(cls)

    def get_name(self, vk_id="", need_full_info=False):
        self.__check()
        vk_id = str(vk_id)
        if vk_id.startswith("-"):
            resp = self.api.groups.getById(group_id=str(vk_id)[1:], v=5.0)
            if need_full_info:
                return resp
            else:
                return resp['name']
        else:
            if vk_id:
                resp = self.api.users.get(user_ids=vk_id, v=5.100)[0]
            else:
                resp = self.api.users.get(v=5.100)[0]
            if need_full_info:
                return resp
            else:
                return "%s %s" % (resp['first_name'], resp['last_name'])

    def __check(self):
        field_name = f'{self.__class__.__name__}__LAST_CALL_TIME'.lower()
        if getattr(self, field_name, None) is None:
            setattr(self, field_name, self.__LAST_CALL_TIME)
        past_time = int(time.time()) - getattr(self, field_name)
        if past_time < PAUSE_TIME: time.sleep(PAUSE_TIME - past_time)
        setattr(self, field_name, time.time())


class Messages(VkMixin):
    __LAST_CALL_TIME = int(time.time())

    def __new__(cls, *arg, **args):
        if cls is Messages:
            return None
        return object.__new__(cls)

    def get_dialogs(self, page=0, count=200):
        self.__check()
        return self.api.messages.getDialogs(offset=count * page, count=count, v=5.0)

    def get_peers(self, page=0, count=15):
        dialogs = self.get_dialogs(page, count)["items"]
        peers = []
        date_hash = 0
        for peer in dialogs:
            if "chat_id" in peer.keys():
                peers.append(2000000000 + peer['chat_id'])
            else:
                peers.append(peer['user_id'])
            date_hash += peer["date"]
        return {"items": peers, "hash": date_hash}

    def get_all_peers(self):
        page = 0
        dialogs = self.get_dialogs(page, 200)["items"]
        peers = []
        date_hash = 0
        while True:
            for peer in dialogs:
                if "chat_id" in peer.keys():
                    peers.append(2000000000 + peer['chat_id'])
                else:
                    peers.append(peer['user_id'])
                date_hash += peer["date"]
            page += 1
            dialogs = self.get_dialogs(page, 200)["items"]
            if len(dialogs) != 200: break
        return {"items": peers, "hash": date_hash}

    def get_messages(self, vk_id, page, count=15):
        self.__check()
        return self.api.messages.getHistory(offset=count * page, count=count, peer_id=vk_id, v=5.38)

    def __check(self):
        field_name = f'{self.__class__.__name__}__LAST_CALL_TIME'.lower()
        if getattr(self, field_name, None) is None:
            setattr(self, field_name, self.__LAST_CALL_TIME)
        past_time = int(time.time()) - getattr(self, field_name)
        if past_time < PAUSE_TIME: time.sleep(PAUSE_TIME - past_time)
        setattr(self, field_name, time.time())


class Media(VkMixin):
    __LAST_CALL_TIME = int(time.time())

    def __new__(cls, *arg, **args):
        if cls is Media:
            return None
        return object.__new__(cls)

    def get_max_size_photo(self, attachment):
        # self.__check()
        old_size = -1
        max_size = -1
        if 'photo' in attachment.keys():
            photo = attachment['photo']
        else:
            photo = attachment
        for key in photo.keys():
            if 'photo' in key:
                new_size = int(key.split('_')[1])
                if new_size > old_size:
                    max_size = key
                    old_size = new_size
        if max_size:
            return photo[max_size]
        else:
            raise AttributeError("It isnt photo attachment")

    def get_posts(self, owner_id, page, count=15):
        self.__check()
        return self.api.wall.get(owner_id=owner_id, count=count, offset=count * page, v=5.92)

    def __check(self):
        field_name = f'{self.__class__.__name__}__LAST_CALL_TIME'.lower()
        if getattr(self, field_name, None) is None:
            setattr(self, field_name, self.__LAST_CALL_TIME)
        past_time = int(time.time()) - getattr(self, field_name)
        if past_time < PAUSE_TIME: time.sleep(PAUSE_TIME - past_time)
        setattr(self, field_name, time.time())


    # dont work
    # def getVideo(self, raw_video):
    #     raw_video = raw_video['video']
    #     url = 'https://api.vk.com/method/video.get?videos=%d_%d_%s&access_token=%s&v=5.60' % (
    #         raw_video['owner_id'], raw_video['id'], raw_video['access_key'], self.token)
    #     session = requests.Session()
    #     session.headers.update({'User-Agent': 'VKAndroidApp/4.12-1118'})
    #     video = session.get(url).json()["response"]['items'][0]
    #     return {'player': video['player'], 'photo': self.getMaxSizePhoto(raw_video)}


class VK(Account, Messages, Media):
    class info:
        def __init__(self, id=0, name="", creation_time=0, login="", password=""):
            self.id = id
            self.name = name
            self.creation_time = creation_time
            self.login = login
            self.password = password

    def __init__(self, token="", login="", password=""):
        if token:
            self.token = token
            self.api = self._get_api(token)
        elif login and password:
            self.token = self._get_token(login, password)
            self.api = self._get_api(self.token)
        else:
            raise AttributeError("set token or login&password")
        self.info = VK.info(id=self.get_name(need_full_info=True)['id'],
                            name=self.get_name(),
                            creation_time=int(time.time()),
                            login=login,
                            password=password)

        # self.__dict__.update({'id': id, 'token': token, 'api': api})
        # self.messages = Messages(self.__dict__)
        # self.wall = Wall(self.__dict__)
        # self.media = Media(self.__dict__)

    def _get_token(self, login, password):
        if login.startswith("8"): login = '+7' + login[1:]
        try:
            session = vk.AuthSession('2685278', login, password, scope='2097151')
            return session.access_token
        except VkAPIError as e:
            raise VkAPIError("cannt login: " + e.message)

    def _get_api(self, token):
        try:
            return vk.API(vk.AuthSession(access_token=token))
        except VkAPIError as e:
            raise VkAPIError("cannt login: " + e.message)

    def __str__(self):
        return "%s\nid:   %s\nname: %s\n%s" % ("=" * 20, str(self.info["id"]), self.info["name"], "=" * 20)


def get_dialogs_history(vk_acc: VK, peers):
    all_dialogs_message = {}
    path_to_download = os.path.join(config.path.to_vk_dump, str(vk_acc.info.id), "dialogs")
    for peer in peers:
        try:
            if peer in config.vk.ignore:
                continue

            logger.info(f"Получение сообщений из диалога с {peer}")
            all_dialogs_message.update({peer: []})
            page = 0
            found_dialog = True

            old_messages = None
            if f"{peer}.json" in os.listdir(path_to_download):
                with open(os.path.join(path_to_download, f"{peer}.json"), "rb") as dialog:
                    old_messages = json.loads(dialog.read())

            while True:
                messages = vk_acc.get_messages(vk_id=peer, page=page, count=200)

                page_count = math.ceil(messages["count"] / 200) - 1 if messages["count"] > 0 else 0
                logger.info(f"Получено {page}/{page_count} страниц диалога с {peer} [всего сообщений {messages['count']}]")

                if messages is None or messages["count"] == 0:
                    found_dialog = False
                    break

                for message in messages["items"]:
                    if message["date"] > (old_messages[0]["date"] if old_messages else -1):
                        all_dialogs_message[peer].append(message)
                    else:
                        break

                page += 1

                if messages["items"][-1]["date"] <= (old_messages[0]["date"] if old_messages and old_messages[0] else -1) or page > page_count:
                    all_dialogs_message[peer] += old_messages if old_messages else []
                    break

            if not found_dialog:
                logger.info(f"Нет сообщений в диалоге с {peer}")
                continue

            logger.info(f"Получено {messages['count']} сообщений из диалога с {peer}")

            data = json.dumps(all_dialogs_message[peer], separators=(',', ':'))
            with open(os.path.join(path_to_download, f"{peer}.json"), "wb") as mess_file:
                mess_file.write(data.encode("utf-8"))

            logger.info(f"Дилог с {peer} записан, обработано {peers.index(peer) + 1}/{len(peers)} диалогов")

        except Exception as e:
                logger.error(f"Дилог с {peer} не получен: {e}[{e.__traceback__.tb_lineno}]")
    logger.info('Получены все сообщения')


if __name__ == '__main__':
    vk = VK(login=config.vk.login, password=config.vk.password)
    print(vk)
