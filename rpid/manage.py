from rpid.controller import Controller
import rpid.config

def start():
    controller = Controller()
    for thread in controller.get_dumpers():
        thread.start()
    return None

_actions = {
    'start': start
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = _actions[sys.argv[1]]
    else:
        exit(-1)
        
    if len(sys.argv) > 2 and sys.argv[2] == "--log":
        config.logging_.config["loggers"]["general"]["handlers"].append("console")
        logging.config.dictConfig(config.logging_.config)
    
    action()
