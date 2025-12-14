#Launch page for the MOCR simulator

import subprocess
import sys
import json

'''simulated object
username
multi or single user
debug if debug = True: timestep, commands, 
Old game: if true -> file, takes json input and parse it into special json

'''
simulated = str.lower(input("Debug mode: simulated object: choice = cubesat"))
username = str(input("enter username: "))
while True: #Only in use while multiplayer is not implemented
    single_multi = str.lower(input("Debug mode: single or multiplayer: choice = single, multi not implemented"))
    if single_multi == "single":
        single_multi = True
        break
    else:
        single_multi = False
        raise Exception("Multiplayer not implemented") #Only in use while multiplayer is not implemented
    
debug = bool(input("Debug mode: True/False"))
#Checks for valid input
if simulated != "cubesat":
    raise Exception("Only cubesat simulation is currently implemented")
if debug not in [True, False]:
    raise Exception("Debug input must be True or False")
if single_multi not in [True, False]:
    raise Exception("Single/Multi input must be single or multi")
#Saves configuration to a json file
launch_config = {
    "Do no modify this file unless you know what you are doing": "This file is used to pass launch configs to main.py",
    "simulated": simulated,
    "username": username,
    "single_multi": single_multi,
    "debug": debug
}
with open('SIM_FILES/launch_config.json', 'w') as launch_config_file:
    json.dump(launch_config, launch_config_file)

#Launches the main program, must be at the end of the file
subprocess.run([sys.executable, "CODE/main.py"])