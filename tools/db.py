import pymongo


class DB:
    def __init__(self, db_url):
        # db_url = mongodb://<db_user>:<password>@<db_server_ip/domain>:<db_server_port>/<db_name>
        self.client = pymongo.MongoClient(db_url)
        self.db = self.client.get_default_database()

    def set(self, tg_id, token, vk_id):
        self.db.toks.save({"_id": tg_id, "token": token, "vk_id":vk_id})

    def get(self, tg_id):
        return self.db.toks.find_one({"_id": tg_id})

    def writeData(self, data):
        self.db.logs.insert_one(data)

    def setStatus(self, tg_id, status):
        self.db.stats.save({"_id": tg_id, "status": status})

    def getStatus(self, tg_id):
        status = self.db.stats.find_one({"_id": tg_id})
        if status == None:
            return 0
        else:
            return status.get('status')

    def setVkId(self, tg_id, vk_id):
        self.db.long_pool.save({"_id": tg_id, "vk_id": vk_id})

    def getVkId(self, tg_id):
        return self.db.long_pool.find_one({"_id": tg_id}).get("vk_id")

    def getIgnoredPeers(self, tg_id):
        return self.db.delMsgs_vkIgnoredPeers.find_one({"_id": tg_id})

    def addIgnoredPeers(self, tg_id, peers):
        old = self.getIgnoredPeers(tg_id)
        if old != None:
            peers+=old
        self.db.delMsgs_vkIgnoredPeers.save({"_id": tg_id, "item": peers})
