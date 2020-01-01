import sys
import logging
from typing import List

from rpid import config
from rpid.service.dumpers.base import Dumper
from rpid.service.dumpers.vkdumper import VK
from rpid.service.db import DB

logger = logging.getLogger("general")


class Controller:
    def __init__(self):
        try:
            self.db = DB(config.db.db_uri)
            self._s_vk = VK(login=config.vk.login, password=config.vk.password)
            # TODO: tg auth
            # TODO: fb auth
        except Exception as e:
            logger.error(f"can't run dumper: {e}")
            raise e

    def _get_services(self) -> dict:
        fields = self.__dict__
        services = {}
        for key in fields.keys():
            if key.startswith("_s_"):
                services.update({key[3:]: fields[key]})
        return services

    def get_dumpers(self) -> List[Dumper]:
        wrapped_services = []
        for service in self._get_services().values():
            dumper = Dumper(service, self.db)
            wrapped_services.append(dumper)
        return wrapped_services

