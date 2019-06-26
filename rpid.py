from _io import TextIOWrapper
import tools
import config
import dumpers


class Logger:
    def __init__(self, path_to_log: str = config.path_to_log):
        self._can_write = True
        self._file: TextIOWrapper = open(path_to_log, "a+")
        self._queue = []

    def write(self, data: str):
        self._queue.append(data)
        while self._queue:
            self._file.write(data)
            self._queue.pop(0)


class RPiD:
    def __init__(self):
        self.logger = Logger()
        try:
            self.db = tools.db(config.db_url)
            self.vk = dumpers.vk_d.VK(config.vk_login, config.vk_password)
            # TODO tg auth
            # TODO fb auth
        except Exception as e:
            print("can't run dumper" + str(e))
            self.logger.write(str(e))
            exit(-1)


def main():
    dumper = RPiD()
    # TODO multythread: one servise - one thread


if __name__ == "__main__":

    main()
