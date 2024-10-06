import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def debug(s):
    print(s, file=sys.stderr, flush=True)


class Building:
    LANDING_PAD_TYPE = 0

    def __init__(self, building_id, coordX, coordY):
        self.building_id = building_id
        self.coordX = coordX
        self.coordY = coordY

    def __repr__(self):
        return f"{{}}{{}}#{self.building_id}({self.coordX}, {self.coordY})"

    @classmethod
    def from_string(cls, input_string):
        building_type, *values = map(int, input_string.split())
        if building_type == Building.LANDING_PAD_TYPE:
            return LandingPad(*values)
        return Module(building_type, *values)


class LandingPad(Building):
    """
    If the building is a landing pad:
    0 buildingId coordX coordY numAstronauts astronautType1 astronautType2 ...
    """
    def __init__(self, building_id, coordX, coordY, numAstronauts, *astronauts):
        super().__init__(building_id, coordX, coordY)
        self.num_astronauts = numAstronauts
        self.astronauts = {}
        for astronaut in astronauts:
            if astronaut in self.astronauts:
                self.astronauts[astronaut] += 1
            else:
                self.astronauts[astronaut] = 1

    def __repr__(self):
        super_repr = super().__repr__().format("LandingPad", self.LANDING_PAD_TYPE)
        return f"{super_repr}[{self.astronauts}]"


class Module(Building):
    """
    Otherwise, the first number is positive and the building is a lunar module:
    moduleType buildingId coordX coordY
    """
    def __init__(self, module_type, building_id, coordX, coordY):
        super().__init__(building_id, coordX, coordY)
        self.module_type = module_type

    def __repr__(self):
        super_repr = super().__repr__().format("Module", self.module_type)
        return f"{super_repr}{self.building_id}"

def create_action_commands(resources, transportation_infrastructure, pods, new_buildings):
    global all_buildings
    pod1_command = "POD 1 0 1 0 2 0"
    pod2_command = "POD 2 0 2 0 1 0"

    if crafted == 0:
        crafted += 1
        return f"TUBE 0 1;TUBE 0 2;{pod1_command}"
    elif crafted == 1:
        crafted += 1
        return f"{pod2_command}"

    return "WAIT"


all_buildings = []

# game loop
while True:
    resources = int(input())
    num_travel_routes = int(input())
    transportation_infrastructure = []
    for i in range(num_travel_routes):
        transport_id_from, transport_id_to, capacity = [int(j) for j in input().split()]
        transportation_infrastructure.append((transport_id_from, transport_id_to, capacity))
    num_pods = int(input())
    pods = []
    for i in range(num_pods):
        pod_properties = input()
        pods.append(pod_properties)
    num_new_buildings = int(input())
    new_buildings = []
    for i in range(num_new_buildings):
        building_properties = input()
        building = Building.from_string(building_properties)
        new_buildings.append(building)

    # Write an action using print

    debug(f"resources: {resources}")
    debug(f"buildings: {transportation_infrastructure}")
    debug(f"pods: {pods}")
    debug(f"new_buildings: {new_buildings}")

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    command = create_action_commands(resources, transportation_infrastructure, pods, new_buildings)
    print(command)
