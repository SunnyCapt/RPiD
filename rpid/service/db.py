from pymongo import MongoClient


class DB:
    def __init__(self, db_uri: str):
        # db_uri = mongodb://<db_user>:<password>@<db_server_ip/domain>:<db_server_port>/<db_name>
        self.client = MongoClient(db_uri)
        self.db = self.client.get_database(db_uri[db_uri.rfind("/") + 1:])

    def set(self, tg_id, token, vk_id):
        self.db.tokens.save({"_id": tg_id, "token": token, "vk_id": vk_id})

    def get(self, tg_id):
        return self.db.tokens.find_one({"_id": tg_id})

    def write_data(self, data):
        self.db.logs.insert_one(data)

    def set_status(self, tg_id, status):
        self.db.stats.save({"_id": tg_id, "status": status})

    def get_status(self, tg_id):
        status = self.db.stats.find_one({"_id": tg_id})
        if status == None:
            return 0
        else:
            return status.get('status')

    def set_vk_id(self, tg_id, vk_id):
        self.db.long_pool.save({"_id": tg_id, "vk_id": vk_id})

    def get_vk_id(self, tg_id):
        return self.db.long_pool.find_one({"_id": tg_id}).get("vk_id")

    def get_ignored_peers(self, tg_id):
        return self.db.del_msgs_vk_ignored_peers.find_one({"_id": tg_id})

    def add_ignored_peers(self, tg_id, peers):
        old = self.get_ignored_peers(tg_id)
        if old is not None:
            peers += old
        self.db.del_msgs_vk_ignored_peers.save({"_id": tg_id, "item": peers})
