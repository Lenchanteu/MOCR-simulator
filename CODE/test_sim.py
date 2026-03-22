import base
import subprocess
import sys
import threading
exec(open('CODE/integrity_holder.py').read())
exec(open('CODE/cubesat.py').read())

while base.STOP_COMMAND == False:
    user_input = input("")
    user_input = str.lower(user_input)
    if user_input == "stop":
        base.command_stack.put({"command": {"args": [], "name": "STOP"}})
    if user_input == "MOVE":
        base.command_stack.put({"command":  {"args": [[1,1,1],10,10], "name": "MOVE"}})
    print(base.simulated_comm)
base.save_file(base.sim_batt_level, base.sim_internal_temp, base. sim_rotation, base.sim_location, base.sim_comm_status, base.sim_message)
command_manager_thread = threading.Thread(target=base.command_manager, daemon=True)
command_manager_thread.start()

