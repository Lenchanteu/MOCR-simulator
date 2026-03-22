#base library for every simulated object
import json
from pathlib import Path
from functools import partial
import queue


iteration_number = 0
BASE_DIR = Path(__file__).resolve().parent
COMM_MAIN_PATH = BASE_DIR / 'JSON' / 'communicationFromMain.json'
COMM_CUBESAT_PATH = BASE_DIR / 'JSON' / 'communicationFromCubesat.json'
USER_HOME_DIR = Path.home() / 'MOCRSim'
LAUNCH_CONFIG_PATH = USER_HOME_DIR / 'launch_config.json'
SAVE_FILE_PATH = USER_HOME_DIR / 'save_file.json'
KEY_FILE_PATH = USER_HOME_DIR / 'key.json'
def getSaveFile():
    with open(SAVE_FILE_PATH, 'r') as save_file:
        save = json.load(save_file)
        iteration_number = save["iteration_number"]
getSaveFile()
LOG_FILE_PATH = USER_HOME_DIR / (str(iteration_number + 1) + '.log')
STOP_COMMAND = False
command = {"command": {"args": [], "name": "NONE"}}
command_stack = queue.Queue()
simulated_comm = {"batt_level": 72, 
                  "internal_temp": 20, 
                  "rotation": [0, 0, 0], 
                  "location": [0, 0, 0], 
                  "comm_status": "GOOD", 
                  "message": "CLEAR"}
sim_batt_level = 72
sim_internal_temp = 20
sim_rotation = [0,0,0]
sim_location = [0,0,0]
sim_comm_status = "GOOD"
sim_message = "CLEAR"
main_comm = {
    "sim_state": 1,
    "timestep": 0.1
}
batt_level = max(0, 100) #battery level range in %
sim_message  = 'CLEAR'
def __checker(batt_level):
    sim_message = 'Checking battery'
    if batt_level>100:
        batt_level=100 
        print(SystemError("Battery level exceeded 100%, resetting to 100%"))
    sim_message = 'CLEAR'
def locationUpdater(rotation, power, time, batt_level, timestep, location, batt_efficiency): #time should be in second, rotation in degrees, power in percent
    __checker(batt_level)
    sim_message = 'Calculating location'
    if batt_level >= 10: #minimum battery level to perform any movement
        #Calculate displacement on each axis
        displacement_x =  rotation[0]* power
        displacement_y =  rotation[1]* power
        displacement_z =  rotation[2]* power
        #calculate number of cycles to perform based on inputed time and main timestep
        move_cycles = time//timestep
        move_cycles = int(move_cycles)
        print(displacement_x, displacement_y, displacement_z, move_cycles)
        batt_level, location = __mover(location, move_cycles, displacement_x, displacement_y, displacement_z, batt_level, batt_efficiency)
        sim_message = 'CLEAR'
        return batt_level, location
    else:  
        print("Battery too low for movement")
        sim_message = 'CLEAR'
        return batt_level, location   
def __mover(location, move_cycles, displacement_x, displacement_y, displacement_z, batt_level, batt_efficiency): #actual movement function
    __checker(batt_level)
    batt_cost = ((abs(displacement_x) + abs(displacement_y) + abs(displacement_z)) * batt_efficiency * move_cycles)
    if batt_level < batt_cost:
        move_cycles = abs(int(batt_level // ((displacement_x + displacement_y + displacement_z) * batt_efficiency)))
        batt_cost = ((displacement_x + displacement_y + displacement_z) * batt_efficiency * move_cycles)
        print("Battery low, adjusting movement cycles to:", move_cycles)

    for cycle in range (0, move_cycles):
        sim_message = 'Moving'
        location[0] += displacement_x
        location[1] += displacement_y
        location[2] += displacement_z
    sim_message = 'CLEAR'
    displacement_x = abs(displacement_x)
    displacement_y = abs(displacement_y)
    displacement_z = abs(displacement_z)

    batt_level -= batt_cost
    print(batt_level)
    return batt_level, location

def noop():
    pass
def sendData(batt_level, internal_temp, rotation, location, comm_status, message):
        sim_batt_level = batt_level
        sim_internal_temp = internal_temp
        sim_rotation = rotation
        sim_location = location
        sim_comm_status = comm_status
        sim_message = message
        simulated_comm = {
            "batt_level": batt_level,
            "internal_temp": internal_temp,
            "rotation": rotation,
            "location": location,
            "comm_status": comm_status,
            "message": message,
        }
        
def receiveData(): 
        sim_state = main_comm.get("sim_state", 0)
        timestep = main_comm.get("timestep", 0.1)
        return sim_state, timestep
        
def dispatchCommands(command_table, command_name, args, self):
    if command_name not in command_table:
        raise ValueError(f"Command {command_name} not found in command table.")
    
    entry = command_table[command_name]
    func = entry["name"]
    arg_names = entry["args"]

    resolved_args = []

    for arg in arg_names:
        if arg in args:
            resolved_args.append(args[arg])
        elif hasattr(self, arg):
            resolved_args.append(getattr(self, arg))
        else:
            raise ValueError(f"Missing some argument: {arg} ")
    return partial(func, *resolved_args)

def verify_integrity_launch(): #MUST be executed before anything in EVERY file.
    with open(LAUNCH_CONFIG_PATH, 'r') as launch_config_file:
        launch_config = json.load(launch_config_file)
        if launch_config.get("integrity_checks") != "passed":
            raise Exception("Launch config file integrity checks failed. Closing program to prevent file corruption")

def new_log():
    with open(SAVE_FILE_PATH, 'r') as save_file:
        save = json.load(save_file)
        iteration_number = save["iteration_number"]
    iteration_number = int(iteration_number)
    iteration_number += 1
    LOG_FILE_PATH = USER_HOME_DIR / (str(iteration_number) + '.log')
    with open(LOG_FILE_PATH, 'x') as log_file:
        log_file.write("#new log. This can be used to detect errors AFTER runtime of program.")

def save_file(batt_level, internal_temp, rotation, location, comm_status, message):
    with open(SAVE_FILE_PATH, 'w') as save_file:
        save = { 
            "batt_level": batt_level,
            "internal_temp": internal_temp,
            "rotation": rotation,
            "location": location,
            "comm_status": comm_status,
            "message": message,
            "iteration_number": str(int(iteration_number) + 1)
        }
        json.dump(save, save_file)
def command_manager():
    while not STOP_COMMAND:
        command_state = "undefined"
        if command == {"command": {"args": [], "name": "NONE"}}: # type: ignore
            command_state = "cleared"
        else:
           command_state = "busy"
        if command_state == "cleared":
            if command_stack.empty():
                continue
            command = command_stack.get()
def start_comm():
    pass #not implemented