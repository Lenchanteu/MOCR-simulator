import simulated_base
import subprocess
import sys
import json
import threading
subprocess.run([sys.executable, 'CODE/integrity_holder.py'])
subprocess.run([sys.executable, 'CODE/cubesat.py'])

def function():
    while True:
        user_input = input("")
        user_input = str.lower(user_input)
        if user_input == "stop":
            with open(simulated_base.COMMAND_STACK_PATH, 'a') as command_stack_file:
                dumper = {"command": {"args": [], "name": "STOP"}}
                json.dump(dumper, command_stack_file)

new_thread = threading.Thread(target=function)
new_thread.start()