import json
import base
import threading

number = 0
with open(base.LAUNCH_CONFIG_PATH, 'r') as launch_config_file:
    launch_config = json.load(launch_config_file)
    try:
        simulated = launch_config["simulated"]
        username = launch_config["username"]
        single_multi = launch_config["single_multi"]
        debug = launch_config["debug"]
    except KeyError as e:
        raise Exception(f"Launch config missing the: {e} property")
    warning = launch_config.get("Do not modify this file unless you know what you are doing")
    simulated = launch_config.get("simulated")
    username = launch_config.get("username")
    single_multi = launch_config.get("single_multi")
    debug = launch_config.get("debug")
with open(base.LAUNCH_CONFIG_PATH, 'w') as launch_config_file:
    json_go = {
        "Do not modify this file unless you know what you are doing": warning,
        "simulated": simulated,
        "username": username,
        "single_multi": single_multi,
        "debug": debug,
        "integrity_checks": "passed"
    }
    json.dump(json_go, launch_config_file)

def command_manager():
    while not base.STOP_COMMAND:
        command_state = "undefined"
        if base.command == {"command": {"args": [], "name": "NONE"}}:
            command_state = "cleared"
        else:
           command_state = "busy"
        if command_state == "cleared":
            base.command_stack
            if base.command_stack.empty():
                continue
            base.command = base.command_stack.get()

command_manager_thread = threading.Thread(target=command_manager, daemon=True)
command_manager_thread.start()

