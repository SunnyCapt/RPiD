from rpid.controller import Controller
import rpid.config

def main():
    controller = Controller()
    for thread in controller.get_dumpers():
        thread.start()
    return None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--log":
        config.logging_.config["loggers"]["general"]["handlers"].append("console")
        logging.config.dictConfig(config.logging_.config)
    main()
