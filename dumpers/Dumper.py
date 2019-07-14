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
        self.hash = -1

    def check(self):
        peers = self.api.get_peers(count=200)
        if self.hash == peers["hash"]: return False
        self.hash = peers["hash"]
        return True

    def update(self):
        peers = self.api.get_peers(count=200)["items"]



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
        flage = 0
        while flage < config.settings.max_attempts:
            try:
                if self.service.check():
                    self.service.update()
                    if flage > 0: flage = 0
                else:
                    time.sleep(config.settings.waiting_time)
                    # TODO: fix this code
            except Exception as e:
                flage += 1
                self.logger.write(
                    "cant update " + self.service.__class__.__name__ + ": " + str(e))
