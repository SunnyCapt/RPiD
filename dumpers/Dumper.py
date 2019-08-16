import os
import threading
import time

import config
from dumpers.vk_d.api import VK


class DumperMixin:
    def __init__(self, service_api):
        self.api = service_api

    def check(self) -> bool:
        """State change checking

        :return: True - if there are new changes, else False
        """
        raise NotImplemented()

    def update(self):
        """Getting and writing updates"""
        raise NotImplemented()

    def close(self):
        """Close all connections and streams for self.service"""
        raise NotImplemented()


class VkDumper(DumperMixin):
    def __init__(self, service):
        self.api: VK = service
        self.peers = []
        self.hash = -1

    @staticmethod
    def _check_paths():
        os.makedirs(config.path.to_vk_dump, exist_ok=True)
        return None

    def check(self):
        peers = self.api.get_all_peers()
        if self.hash == peers["hash"]: return False
        self.hash = peers["hash"]
        self.peers = peers["items"]
        return True

    def update(self):
        self._check_paths()
        print("VK is updated!")
        return None



"""
class TgDumper(DumperMixin):
    def check(self):
        pass

    def update(self):
        pass

    def close(self):
        pass
"""

"""
class FbDumper(DumperMixin):
    def check(self):
        pass

    def update(self):
        pass

    def close(self):
        pass
"""


def get_wrapper(service) -> DumperMixin:
    return {VK: VkDumper
            # TODO: tg = TgDumper
            # TODO: fb = FbDumper
            }[service.__class__](service)


class Dumper(threading.Thread):
    def __init__(self, service, logger, db):
        threading.Thread.__init__(self, name=service.__class__.__name__)
        self.logger = logger
        self.db = db
        self.service: DumperMixin = get_wrapper(service)

    def run(self):
        att_count = 0
        while att_count < config.settings.max_attempts:
            try:
                if self.service.check():
                    self.service.update()
                    if att_count > 0: att_count = 0
                time.sleep(config.settings.waiting_time)
                # TODO: fix this code
            except Exception as e:
                att_count += 1
                self.logger.write("cant check or update " + self.service.__class__.__name__ + ": " + str(e))
