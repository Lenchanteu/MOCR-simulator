#base library for every simulated object
import json
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
            with open('JSON/commands.json', 'w') as command_file:
                data = json.load(command_file)
                command = data.get("command", "0")
                if command != "0":
                    json.dump({"command": {
                        None
                    }}, command_file)
                    return command
        except Exception as e:
            try:
                with open('JSON/commands.json', 'x') as command_file:
                    data = json.load(command_file)
                    command = data.get("command", "0")
                    if command != "0":
                        json.dump({"command": {
                            None
                        }}, command_file)
                        return command
            except Exception as e:
                print(Exception(f"{e} :No command file detected, please verify the state of commands.json"))

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
            with open('JSON/communication.json', 'w',) as comm_file:
                json.dump(data, comm_file)
        except Exception as e:
            try:
                with open('JSON/communication.json', 'x') as comm_file:
                    json.dump(data, comm_file)
            except:
                print(Warning(f"{e} :No communication line: the simulated object will not be able to communicate. Verify that communication.json is not opened in another program."))

def receiveData():
        try:
            with open('JSON/communication.json', 'r') as comm_file:
                data = json.load(comm_file)
                sim_state = data.get("sim_state", 0)
                timestep = data.get("timestep", 0.1)
                return sim_state, timestep
        except Exception as e:
            print(Exception(f"{e} :No communication file detected, please verify the state of communication.json"))