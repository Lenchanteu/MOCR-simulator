#Launch page for the MOCR simulator

import subprocess
import sys
import json
import pathlib

'''simulated object
username
multi or single user
debug if debug = True: timestep, commands, 
Old game: if true -> file, takes json input and parse it into special json

'''
User_Home_Path = str(pathlib.Path.home())
Sim_Path = f'{User_Home_Path}\\MOCRSim'
pathlib.Path(Sim_Path).mkdir(parents=True, exist_ok=True)
OldGamebool = str.lower(input("Old game loading: true/false"))
if OldGamebool == "true":
    OldGamebool = True
else:
    OldGamebool = False
if OldGamebool == True:
    OldGameFile = json.load(open(input("Enter the file path of the save in .json: ")))
    with open(f'{User_Home_Path}\\MOCRSim\\launch_config.json', 'w') as launch_config_file:
        json.dump(OldGameFile, launch_config_file)
else:
    simulated = "cubesat" #str.lower(input("Debug mode: simulated object: choice = cubesat: ")) used later when more simulations are developed
    username = str(input("enter username: "))
    while True: #Only in use while multiplayer is not implemented
        single_multi = str.lower(input("Debug mode: single or multiplayer: choice = single, multi not implemented: "))
        if single_multi == "single":
            single_multi = True
            break
        else:
            single_multi = False
            raise Exception("Multiplayer not implemented") #Only in use while multiplayer is not implemented
        
    debug = str.lower(input("Debug mode: True/False"))
    if debug == "true":
        debug = True
    else:
        debug = False
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

    with open(f'{User_Home_Path}\\MOCRSim\\launch_config.json', 'w') as launch_config_file:
        json.dump(launch_config, launch_config_file)

#Launches the main program, must be at the end of the file
subprocess.run([sys.executable, "CODE/main.py"])
quit()