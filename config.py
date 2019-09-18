import logging.config
import urllib.parse as parse
import os

from typing import List, Dict


class db:
    login: str = parse.quote_plus(None)
    password: str = parse.quote_plus(None)
    server: str = None
    port: int = None
    db_name: str = None # "rpid"
    db_uri: str = f"mongodb://{login}:{password}@{server}:{port}/{db_name}"
# ======================
class vk:
    login: str = None # like "+7**********"
    password: str = None
    ignore: List = None
# ======================
class path:
    base_dir: str = os.path.dirname(os.path.abspath(__file__))
    to_log: str = os.path.join(base_dir, "data/log.log")
    to_vk_dump: str = os.path.join(base_dir, "data/vk/")
    to_tg_dump: str = os.path.join(base_dir, "data/tg/")
    to_fb_dump: str = os.path.join(base_dir, "data/fb/")
# ======================
class settings:
    max_attempts: int = 5
    waiting_time: int = 5 # seconds
    proxy: Dict = None # like {"host": "127.0.0.1", "port": 9050}
# ======================
class telegram_auth:
    api_id: int = None
    api_hash: str = None
# ======================
class logging_:
    config: Dict = {
        "version": 1,
        'disable_existing_loggers': False,
        "formatters": {
            "verbose": {
                "format": "%(asctime)s %(levelname)s | %(pathname)s:%(funcName)s:%(lineno)d | %(threadName)s[%(thread)d] | %(message)s"
            },
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "formatter": "verbose",
                "level": "DEBUG",
                "filename": path.to_log,
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose"
            },
        },
        "loggers": {
            "general": {
                "handlers": ["console", "file"],
                "level": "INFO",
                'propagate': False,
            },
        },
    }


try:
    from local_config import *
except ImportError as e:
    pass


logging.config.dictConfig(logging_.config)