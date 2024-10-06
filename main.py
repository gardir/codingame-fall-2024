import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def debug(s):
    print(s, file=sys.stderr, flush=True)


crafted = 0
pod1_command = "POD 1 0 1 0 2 0"
pod2_command = "POD 2 0 2 0 1 0"

# game loop
while True:
    resources = int(input())
    num_travel_routes = int(input())
    buildings = []
    for i in range(num_travel_routes):
        building_id_1, building_id_2, capacity = [int(j) for j in input().split()]
        buildings.append((building_id_1, building_id_2, capacity))
    num_pods = int(input())
    pods = []
    for i in range(num_pods):
        pod_properties = input()
        pods.append(pod_properties)
    num_new_buildings = int(input())
    new_buildings = []
    for i in range(num_new_buildings):
        building_properties = input()
        new_buildings.append(building_properties)

    # Write an action using print

    debug(f"resources: {resources}")
    debug(f"buildings: {buildings}")
    debug(f"pods: {pods}")
    debug(f"new_buildings: {new_buildings}")

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    if crafted == 0:
        print(f"TUBE 0 1;TUBE 0 2;{pod1_command}")
        crafted += 1
    elif crafted == 1:
        print(f"{pod2_command}")
        crafted += 1
    else:
        print("WAIT")
