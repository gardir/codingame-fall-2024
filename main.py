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

    def distance_to(self, other_building):
        x2 = (self.coordX + other_building.coordX)**2
        y2 = (self.coordY + other_building.coordY)**2
        return math.sqrt(x2 + y2)

    def tube_to(self, other_building):
        distance = self.distance_to(other_building)
        command_string = f"TUBE {self.building_id} {other_building.building_id}"
        return distance, command_string

    @classmethod
    def from_string(cls, input_string, landing_pads, modules):
        building_type, *values = map(int, input_string.split())
        if building_type == Building.LANDING_PAD_TYPE:
            landing_pad = LandingPad(*values)
            landing_pads.append(landing_pad)
            return landing_pad
        module = Module(building_type, *values)
        modules.append(module)
        return module


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


def create_action_commands(resources, transportation_infrastructure, pods, all_buildings, landing_pads, modules: list[Module]):
    pod_commands = ["POD {} 0 1 0 2 0", "POD {} 0 2 0 1 0"]
    POD_COST = 1000
    total_astronauts = {}
    for landing_pad in landing_pads:
        # TODO -- problems with several landing pads
        total_astronauts.update(landing_pad.astronauts)
    debug(total_astronauts)
    command_string = []
    if len(transportation_infrastructure) == 0:
        # TODO -- from the actual landing pad xD
        accepting_astronauts = [building for building in modules if building.module_type in total_astronauts]
        for module in accepting_astronauts:
            resource_cost, tube_command = landing_pads[0].tube_to(module)
            resources -= resource_cost
            command_string.append(tube_command)

    pods_built = len(pods)
    if pods_built > 2:
        # upgrade_capacity()
        pass

    while resources >= POD_COST:
        resources -= POD_COST
        pods_built += 1
        command_string.append(pod_commands[pods_built % len(pod_commands)].format(pods_built))

    return ';'.join(command_string) if len(command_string) > 0 else "WAIT"



class Infrastructure:
    """
    On the next numTravelRoutes lines, the description of a tube or teleporter as a list of three space-separated integers buildingId1, buildingId2 and capacity:
    buildingId1 and buildingId2 are the ends of the tube or teleporter.
    capacity equals 0 if the route is a teleporter, and represents the capacity of the tube otherwise.
    """
    def __init__(self, from_building, to_building):
        self.from_building = from_building
        self.to_building = to_building

    @classmethod
    def from_values(cls, building_from, building_to, capacity):
        if capacity > 0:
            return Tube(building_from, building_to, capacity)
        return Teleporter(building_from, building_to)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.from_building} -> {self.to_building}"


class Teleporter(Infrastructure):

    def __init__(self, from_building, to_building):
        super().__init__(from_building, to_building)


class Tube(Infrastructure):

    def __init__(self, from_building, to_building, capacity):
        super().__init__(from_building, to_building)
        self.capacity = capacity


all_buildings = {}
landing_pads = []
modules = []

# game loop
while True:
    resources = int(input())
    num_travel_routes = int(input())
    transportation_infrastructure = []
    for i in range(num_travel_routes):
        transport_id_from, transport_id_to, capacity = [int(j) for j in input().split()]
        building_from = all_buildings[transport_id_from]
        building_to = all_buildings[transport_id_to]
        transport = Infrastructure.from_values(building_from, building_to, capacity)
        transportation_infrastructure.append(transport)
    num_pods = int(input())
    pods = []
    for i in range(num_pods):
        pod_properties = input()
        pods.append(pod_properties)
    num_new_buildings = int(input())
    for i in range(num_new_buildings):
        building_properties = input()
        new_building = Building.from_string(building_properties, landing_pads, modules)
        all_buildings[new_building.building_id] = new_building

    # Write an action using print

    debug(f"resources: {resources}")
    debug(f"infrastructure: {transportation_infrastructure}")
    debug(f"pods: {pods}")
    debug(f"new_buildings: {all_buildings}")

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    command = create_action_commands(resources, transportation_infrastructure, pods, all_buildings, landing_pads, modules)
    print(command)
