import simulated_base

location = [0,0,0]
batt_level = 100
while True:
    x = input()
    if x == "exit":
        break
    if x == "w":
        batt_level, location = simulated_base.locationUpdater([1,0,0], 5, 10, batt_level, 1, location, 0.01)
        print(batt_level, location)
    if x == "s":
        batt_level, location = simulated_base.locationUpdater([-1,0,0], 5, 10, batt_level, 1, location, 0.01)
        print(batt_level, location)
    if x == "a":
        batt_level, location = simulated_base.locationUpdater([0,1,0], 5, 10, batt_level, 1, location, 0.01)
        print(batt_level, location)
    if x == "d":
        batt_level, location = simulated_base.locationUpdater([0,-1,0], 5, 10, batt_level, 1, location, 0.01)
        print(batt_level, location)
    if x == "q":
        batt_level, location = simulated_base.locationUpdater([0,0,1], 5, 10, batt_level, 1, location, 0.01)
        print(batt_level, location)
    if x == "e":
        batt_level, location = simulated_base.locationUpdater([0,0,-1], 5, 10, batt_level, 1, location, 0.01)
        print(batt_level, location)
quit()