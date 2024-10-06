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

    def upgrade_tube(self, other_building, new_capacity=2):
        cost = self.distance_to(other_building) * new_capacity
        command_string = f"UPGRADE {self.building_id} {other_building.building_id}"
        return cost, command_string

    @classmethod
    def from_string(cls, input_string, landing_pads, modules):
        building_type, *values = map(int, input_string.split())
        if building_type == Building.LANDING_PAD_TYPE:
            landing_pad = LandingPad(*values)
            landing_pads.append(landing_pad)
            return landing_pad
        module = Module(building_type, *values)
        if module.module_type in modules:
            modules[module.module_type].append(module)
        else:
            modules[module.module_type] = [module]
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


def estimate_traveling_astronauts(landing_pads, transportation_infrastructure):
    list_of_routes = []
    for landing_pad in landing_pads:
        if landing_pad in transportation_infrastructure:
            for astronaut_type, astronauts in landing_pad.astronauts.items():
                _, infrastructures = find_optimal_route(transportation_infrastructure,
                                                        transportation_infrastructure[landing_pad],
                                                        astronaut_type, astronauts)
                for infrastructure in infrastructures:
                    infrastructure.add_astronauts(astronauts)
                list_of_routes.append(infrastructures)
    list_of_upgrade_required_infrastructure = []
    for infrastructures in list_of_routes:
        at_least_one_needs_upgrade = False
        for infrastructure in infrastructures:
            if infrastructure.needs_upgrade:
                at_least_one_needs_upgrade = True
                break
        if at_least_one_needs_upgrade:
            list_of_upgrade_required_infrastructure.append(infrastructures)
    return list_of_upgrade_required_infrastructure


def find_optimal_route(all_infrastructures, infrastructures, astronaut_type, astronauts):
    best_value = None
    best_infrastructures = None
    for infrastructure in infrastructures:
        building_to = infrastructure.to_building
        if building_to.module_type == astronaut_type:
            return 1, [infrastructure]
        if building_to in all_infrastructures:
            next_infrastructure = all_infrastructures[building_to]
            length, route = find_optimal_route(all_infrastructures, next_infrastructure, astronaut_type, astronauts)
            if best_value is None or length < best_value:
                best_value = length
                if best_infrastructures is None:
                    best_infrastructures = [next_infrastructure] + route
    return best_value + 1, best_infrastructures


def create_action_commands(resources, transportation_infrastructure, pods, all_buildings, landing_pads, modules: dict[int, list[Module]]):
    pod_commands = ["POD {} 0 1 0 2 0", "POD {} 0 2 0 1 0"]
    POD_COST = 1000
    total_astronauts = {}
    for landing_pad in landing_pads:
        # TODO -- problems with several landing pads
        total_astronauts.update(landing_pad.astronauts)
    debug(total_astronauts)
    command_string = []
    pods_built = len(pods)
    if len(transportation_infrastructure) == 0:
        # TODO -- from the actual landing pad xD
        modules_accepting_astronauts = [module_list for module_type, module_list in modules.items()
                                        if module_type in total_astronauts]
        for module_list in modules_accepting_astronauts:
            module = module_list[0]  # TODO -- create a path of tubes / infrastructure to it
            resource_cost, tube_command = landing_pads[0].tube_to(module)
            resources -= resource_cost
            command_string.append(tube_command)
    elif pods_built > 2:  # TODO -- better estimation of when to upgrade
        # TODO -- from the actual landing pad xD
        infrastructure_requires_upgrade = estimate_traveling_astronauts(landing_pads, transportation_infrastructure)
        for infrastructure_list in infrastructure_requires_upgrade:
            for infrastructure in infrastructure_list:
                _from, _to = infrastructure.from_building, infrastructure.to_building
                resource_cost, upgrade_tube_command = _from.upgrade_tube(_to)
                if resource_cost <= resources:
                    resources -= resource_cost
                    command_string.append(upgrade_tube_command)

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
        self.traveling_astronauts = 0

    @classmethod
    def from_values(cls, building_from, building_to, capacity):
        if capacity > 0:
            return Tube(building_from, building_to, capacity)
        return Teleporter(building_from, building_to)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.from_building} -> {self.to_building}"

    @property
    def needs_upgrade(self):
        return False

    def add_astronauts(self, astronauts):
        self.traveling_astronauts += astronauts

    def desired_astronauts(self):
        return self.traveling_astronauts


class Teleporter(Infrastructure):

    def __init__(self, from_building, to_building):
        super().__init__(from_building, to_building)


class Tube(Infrastructure):

    def __init__(self, from_building, to_building, capacity):
        super().__init__(from_building, to_building)
        self.capacity = capacity

    @property
    def needs_upgrade(self):
        return self.capacity * 10 < self.desired_astronauts()


all_buildings = {}
landing_pads = []
modules = {}

# game loop
while True:
    resources = int(input())
    num_travel_routes = int(input())
    transportation_infrastructure = {}
    for i in range(num_travel_routes):
        transport_id_from, transport_id_to, capacity = [int(j) for j in input().split()]
        building_from = all_buildings[transport_id_from]
        building_to = all_buildings[transport_id_to]
        transport = Infrastructure.from_values(building_from, building_to, capacity)
        if building_from in transportation_infrastructure:
            transportation_infrastructure[building_from].append(transport)
        else:
            transportation_infrastructure[building_from] = [transport]

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
