import threading
import time
from _io import TextIOWrapper

from dumpers.vk_d.__main__ import VK


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
    def check(self):
        pass

    def update(self):
        pass

    def close(self):
        pass


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
            }[service].__new__(service)


class Dumper(threading.Thread):
    def __init__(self, service, log, config):
        super().__init__(self)
        self.log: TextIOWrapper = log
        self.config = config
        self.service: DumperMixin = get_wrapper(service)

    def run(self):
        flage = 0
        while flage < self.config.max_attempts:
            try:
                if self.service.check():
                    self.service.update()
                    if flage > 0: flage = 0
                else:
                    time.sleep(self.config.waiting_time)
                    # TODO: fix this code
            except Exception as e:
                flage += 1
                self.log.write(
                    "\ncant update " + self.service.__class__ + ": " + str(e) + "\ntime:" + str(time.time()) + "\n")
                self.log.flush()
