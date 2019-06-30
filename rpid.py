import time
from _io import TextIOWrapper
from typing import List

import config
from dumpers.dumper import Dumper
from dumpers.vk_d.api import VK
from tools.db import DB


class Logger:
    def __init__(self, path_to_log: str = config.path_to_log):
        self._can_write = True
        self._file: TextIOWrapper = open(path_to_log, "a+")
        self._queue = []

    def write(self, data: str):
        self._queue.append(data)
        while self._queue:
            self._file.write("\n%s\n%s\ntime:%d" % ("="*25, data, time.time()))
            self._queue.pop(0)


class RPiD:
    def __init__(self):
        self.logger = Logger()
        try:
            self.db = DB(config.db_uri)
            self._s_vk = VK(login=config.VK.login, password=config.VK.password)
            # TODO tg auth
            # TODO fb auth
        except Exception as e:
            print("can't run dumper: " + str(e))
            self.logger.write(str(e))
            raise e
            # exit(-1)

    def _get_services(self) -> dict:
        fields = self.__dict__
        services = {}
        for key in fields.keys():
            if key.startswith("_s_"):
                services.update({key[3:]: fields[key]})
        return services

    def get_wrapped_serv(self) -> List[Dumper]:
        wrapped_services = []
        for service in self._get_services().values():
            dumper = Dumper(service, self.logger, self.db)
            wrapped_services.append(dumper)
        return wrapped_services


def main():
    rpid = RPiD()
    for thread in rpid.get_wrapped_serv():
        thread.setDaemon(True)
        thread.start()
    input()


if __name__ == "__main__":
    main()
