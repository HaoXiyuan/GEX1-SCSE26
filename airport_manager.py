######################## IMPORTANT ########################
""" Do not rename the variables or functions.
Do not change the function parameters.
Do not add input() calls inside airport_manager.py.
The file must be importable by the tests. """
###########################################################


airport_info = ("OUL", 1, "14-09-2026")
allowed_gates = {"A1", "A2", "A3", "A4", "B1", "B2"}
restricted_destinations = {"Moscow", "Pyongyang"}
flights = {
    "AY450": {
        "destination": "Helsinki",
        "departure": "08:30",
        "gate": "A2",
        "capacity": 5,
        "passengers": ["Alice Wong", "David Kim", "Fatima Ali"]
    },
    "SK271": {
        "destination": "Stockholm",
        "departure": "10:15",
        "gate": "B1",
        "capacity": 4,
        "passengers": ["Chen Wei", "George Smith"]
    },
    "LH2491": {
        "destination": "Munich",
        "departure": "12:40",
        "gate": "A4",
        "capacity": 5,
        "passengers": ["Hana Lee", "Maria Garcia", "Noah Wilson"]
    }
}


def _normalize_flight_number(value):
    if type(value) != str:
        return ""
    return value.strip().upper()


def _normalize_name(value):
    if type(value) != str:
        return ""
    return value.strip().lower()


## Logic to find if a flight exists
def find_flight(flights, flight_number):
    target = _normalize_flight_number(flight_number)
    if target == "":
        return None

    for key in flights:
        if _normalize_flight_number(key) == target:
            return key
    return None


## Logic to find if a passenger exists
def passenger_exists(passengers, passenger_name):
    target = _normalize_name(passenger_name)
    if target == "":
        return False

    for p in passengers:
        if _normalize_name(p) == target:
            return True
    return False


## Logic to check in a passenger
def check_in_passenger(
    flights,
    flight_number,
    passenger_name,
    restricted_destinations
):
    key = find_flight(flights, flight_number)
    if key is None:
        return "FLIGHT_NOT_FOUND"

    if passenger_name is None:
        return "EMPTY_NAME"
    name = passenger_name.strip()
    if name == "":
        return "EMPTY_NAME"

    flight = flights[key]

    destination = flight.get("destination", "")
    restricted = restricted_destinations or set()
    for r in restricted:
        if _normalize_name(r) == _normalize_name(destination):
            return "RESTRICTED"

    if passenger_exists(flight["passengers"], name):
        return "DUPLICATE"

    if len(flight["passengers"]) >= flight["capacity"]:
        return "FULL"

    flight["passengers"].append(name.title())
    return "OK"


## Logic to remove a passenger from a flight
def remove_passenger(
    flights,
    flight_number,
    passenger_name
):
    key = find_flight(flights, flight_number)
    if key is None:
        return "FLIGHT_NOT_FOUND"

    target = _normalize_name(passenger_name)
    if target == "":
        return "PASSENGER_NOT_FOUND"

    passengers = flights[key]["passengers"]

    for i, p in enumerate(passengers):
        if _normalize_name(p) == target:
            passengers.pop(i)
            return "OK"

    return "PASSENGER_NOT_FOUND"


# Logic to change the gate of a flight
def change_gate(
    flights,
    flight_number,
    new_gate,
    allowed_gates
):
    key = find_flight(flights, flight_number)
    if key is None:
        return "FLIGHT_NOT_FOUND"

    if type(new_gate) != str:
        return "INVALID_GATE"

    gate = new_gate.strip().upper()

    allowed_upper = set()
    for g in (allowed_gates or set()):
        if type(g) == str:
            allowed_upper.add(g.strip().upper())

    if gate not in allowed_upper:
        return "INVALID_GATE"

    flights[key]["gate"] = gate
    return "OK"


# Logic to get the status of a flight
def flight_status(flight):
    capacity = flight.get("capacity", 0)
    count = len(flight.get("passengers", []))

    if capacity <= 0:
        return "FULL"

    percentage = count / capacity * 100

    if percentage >= 100:
        return "FULL"
    elif percentage >= 75:
        return "ALMOST FULL"
    else:
        return "AVAILABLE"


# Logic to get the sorted manifest of a flight
def sorted_manifest(
    flights,
    flight_number
):
    key = find_flight(flights, flight_number)
    if key is None:
        return None
    return sorted(flights[key]["passengers"])


# Logic to get the total number of passengers across all flights
def total_passengers(flights):
    total = 0
    for f in flights.values():
        total += len(f.get("passengers", []))
    return total


# Logic to check if any flight is full
def any_full_flight(flights):
    for f in flights.values():
        if len(f.get("passengers", [])) >= f.get("capacity", 0):
            return True
    return False


# Logic to check if all flights have at least one passenger
def all_flights_have_passengers(flights):
    if not flights:
        return False
    for f in flights.values():
        if len(f.get("passengers", [])) == 0:
            return False
    return True