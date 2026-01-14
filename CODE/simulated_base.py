#base library for every simulated object
import json
from pathlib import Path
from functools import partial

BASE_DIR = Path(__file__).resolve().parent
COMM_MAIN_PATH = BASE_DIR / 'JSON' / 'communicationFromMain.json'
COMM_CUBESAT_PATH = BASE_DIR / 'JSON' / 'communicationFromCubesat.json'
COMMANDS_PATH = BASE_DIR / 'JSON' / 'commands.json'
batt_level = max(0, 100) #battery level range in %
def __checker(batt_level):
    if batt_level>100:
        batt_level=100 
        print(SystemError("Battery level exceeded 100%, resetting to 100%"))
def locationUpdater(rotation, power, time, batt_level, timestep, location, batt_efficiency): #time should be in second, rotation in degrees, power in percent
    __checker(batt_level)
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
        return batt_level, location
    else:  
        print("Battery too low for movement")
        return batt_level, location   
def __mover(location, move_cycles, displacement_x, displacement_y, displacement_z, batt_level, batt_efficiency): #actual movement function
    __checker(batt_level)
    batt_cost = ((abs(displacement_x) + abs(displacement_y) + abs(displacement_z)) * batt_efficiency * move_cycles)
    if batt_level < batt_cost:
        move_cycles = int(batt_level // ((displacement_x + displacement_y + displacement_z) * batt_efficiency))
        batt_cost = ((displacement_x + displacement_y + displacement_z) * batt_efficiency * move_cycles)
        print("Battery low, adjusting movement cycles to:", move_cycles)

    for cycle in range (0, move_cycles):
        location[0] += displacement_x
        location[1] += displacement_y
        location[2] += displacement_z

    displacement_x = abs(displacement_x)
    displacement_y = abs(displacement_y)
    displacement_z = abs(displacement_z)

    batt_level -= batt_cost
    print(batt_level)
    return batt_level, location

def receiveCommand():
        try:
            with open(COMMANDS_PATH, 'r') as command_file:
                data = json.load(command_file)
                if data == {"command": {"args": [], "name": "None"}}:
                    return None, None
                command = data.get("command", {"args": [], "name": "NONE"})
                args = command.get("args", [])
                command_name = command.get("name", "NONE")
                if command != "NONE":
                    with open(COMMANDS_PATH, 'w') as command_file:
                        json.dump({"command": {"args": [], "name": "NONE"}}, command_file)
                    return command_name, args
                else:
                    return None, None
        except FileNotFoundError:
            print(Exception("No command file detected: please verify that commands.json exists in the JSON folder"))
        
        except json.decoder.JSONDecodeError:
            print(Exception("Commands file is corrupted: please delte it and run the program again."))

def noop():
    pass
def sendData(batt_level, internal_temp, rotation, location, comm_status, message):
        data = {
            "batt_level": batt_level,
            "internal_temp": internal_temp,
            "rotation": rotation,
            "location": location,
            "comm_status": comm_status,
            "message": message,
        }
        try:
            with open(COMM_CUBESAT_PATH, 'w',) as comm_file:
                json.dump(data, comm_file)
        except Exception as e:
            try:
                with open(COMM_CUBESAT_PATH, 'x') as comm_file:
                    json.dump(data, comm_file)
            except:
                print(Warning(f"{e} :No communication line: the simulated object will not be able to communicate. Verify that communication.json is not opened in another program."))

def receiveData():
        try:
            with open(COMM_MAIN_PATH, 'r') as comm_file:
                data = json.load(comm_file)
                sim_state = data.get("sim_state", 0)
                timestep = data.get("timestep", 0.1)
                return sim_state, timestep
        except Exception as e:
            print(Exception(f"{e} :No communication file detected, please verify the state of communication.json"))

def dispatchCommands(command_table, command_name, json_args, self):
    if command_name not in command_table:
        raise ValueError(f"Command {command_name} not found in command table.")
    
    entry = command_table[command_name]
    func = entry["name"]
    arg_names = entry["args"]

    resolved_args = []

    for arg in arg_names:
        if arg in json_args:
            resolved_args.append(json_args[arg])
        elif hasattr(self, arg):
            resolved_args.append(getattr(self, arg))
        else:
            raise ValueError(f"Missing some argument: {arg} ")
    return partial(func, *resolved_args)
