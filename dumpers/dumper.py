import os
import time
import logging
from threading import Thread

import config
from dumpers.vk_d import api as vk_api
from dumpers.vk_d.api import VK

logger = logging.getLogger("general")

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

    def _check_paths(self):
        os.makedirs(config.path.to_vk_dump, exist_ok=True)
        os.makedirs(os.path.join(config.path.to_vk_dump, str(self.api.info.id)), exist_ok=True)
        os.makedirs(os.path.join(config.path.to_vk_dump, str(self.api.info.id), 'dialogs'), exist_ok=True)
        return None

    def _update(self):
        try:
            vk_api.get_dialogs_history(self.api, self.peers)
        except Exception as e:
            logger.error(f"Cannt update vk: {e}[{e.__traceback__.tb_lineno}]")

    def check(self):
        peers = self.api.get_all_peers()
        if self.hash == peers["hash"]: return False
        self.hash = peers["hash"]
        self.peers = peers["items"]
        return True

    def update(self):
        self._check_paths()
        self._update()
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


class Dumper(Thread):
    def __init__(self, service, db):
        Thread.__init__(self)
        self.name = service.__class__.__name__
        self.db = db
        self.service: DumperMixin = get_wrapper(service)

    def run(self):
        att_count = 0
        while att_count < config.settings.max_attempts:
            try:
                logger.info(f"Checking {self.service.__class__.__name__}")
                if self.service.check():
                    logger.info(f"Start updating of {self.service.__class__.__name__}")
                    self.service.update()
                    logger.info(f"Finished updating of {self.service.__class__.__name__}")
                    if att_count > 0: att_count = 0
                time.sleep(config.settings.waiting_time)
                # TODO: fix this code
            except Exception as e:
                att_count += 1
                logger.error(f"cant check or update {self.service.__class__.__name__}: {e}[{e.__traceback__.tb_lineno}]")
                raise e
