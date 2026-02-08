import json
import simulated_base
import time
import threading

number = 0
with open(simulated_base.LAUNCH_CONFIG_PATH, 'r') as launch_config_file:
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
with open(simulated_base.LAUNCH_CONFIG_PATH, 'w') as launch_config_file:
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
    while not simulated_base.STOP_COMMAND:
        command_state = "not defined"
        with open(simulated_base.COMMANDS_PATH, 'r') as command_file:
            commands = json.load(command_file)
            if commands == {"command": {"args": [], "name": "NONE"}}:
                command_state = "cleared"
            else:
               command_state = "busy"
        if command_state == "cleared":
            with open(simulated_base.COMMAND_STACK_PATH, 'r') as command_stack_file:
                command_stack = json.load(command_stack_file)
                command_stack = list(command_stack)
                if command_stack == []:
                    continue
            
            with open(simulated_base.COMMAND_STACK_PATH, 'w') as command_stack_file:
                with open(simulated_base.COMMANDS_PATH, 'w') as command_file:
                    next_command = command_stack[0]
                    json.dump(next_command, command_file)
                    command_stack.pop(0)
                    json.dump(command_stack, command_stack_file)

command_manager_thread = threading.Thread(target=command_manager)
command_manager_thread.start()

