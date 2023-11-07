# INPUT PARAMETERS NAMES

# General parameters
GEN_PARAMETERS = "general_parameters"
MAX_POWER = "maximum_power"
CURTAILING_COST = "curtailing_cost"
CURTAILING_PENA = "curtailing_penalty"
MAX_CURTAILING = "maximum_curtailing"
FIX_COST_CABLE = "fixed_cost_cable"  # Cost of the turbine - substation cables
VAR_COST_CABLE = "variable_cost_cable"  # Cost of turbine - substation cables
MAIN_LAND_STATION = "main_land_station"

# Position parameters
X = "x"
Y = "y"

# Substation parameters
SUBSTATION_TYPES = "substation_types"
ID = "id"
COST = "cost"
RATING = "rating"
PROB_FAIL = "probability_of_failure"

# Land-Substation cables parameters
LAND_SUB_CABLE_TYPES = "land_substation_cable_types"
# Already defined, same as before
# (if need be, might separate ids and others by type later)
# ID = "id"
FIX_COST = "fixed_cost"
VAR_COST = "variable_cost"
# PROB_FAIL = "probability_of_failure"
# RATING  = "rating"

# Substation-Substation cable parameters
SUB_SUB_CABLE_TYPES = "substation_substation_cable_types"
# SAME INTERNAL PARAMETERS AS LAND_SUB_TYPES
# ID = "id"
# FIX_COST = "fixed_cost"
# VAR_COST = "variable_cost"
# PROB_FAIL = "probability_of_failure"
# RATING  = "rating"

# Subtation location parameters
SUBSTATION_LOCATION = "substation_locations"
# ID = "id"
# X = "x"
# Y = "y"

# wind turbines parameters
WIND_TURBINES = "wind_turbines"
# ID = "id"
# X = "x"
# Y = "y"

# Scenarios parameters
WIND_SCENARIOS = "wind_scenarios"
# ID = "id"
PROBABILITY = "probability"
POWER_GENERATION = "power_generation"


# OUTPUT PARAMETERS NAMES

SUBSTATIONS = "substations"
# ID = "id"
SUB_TYPE = "substation_type"
LAND_CABLE_TYPE = "land_cable_type"

TURBINES = "turbines"
# ID = "id"
SUBSTATION_ID = "substation_id"

SUBSTATION_SUBSTATION_CABLES = "substation_substation_cables"
# SUBSTATION_ID = "substation_id"
OTHER_SUB_ID = "other_substation_id"
CABLE_TYPE_SUBSUB = "cable_type"

# Keys needed in solutions
KEYS_EXPECTED_IDS = [TURBINES, SUBSTATIONS]
KEYS_EXPECTED_PAIRS = [SUBSTATION_SUBSTATION_CABLES]
KEYS_EXPECTED = KEYS_EXPECTED_IDS + KEYS_EXPECTED_PAIRS
# Keys needed in the substation dics
KEYS_EXPECTED_SUBSTATION = [
    ID,
    SUB_TYPE,
    LAND_CABLE_TYPE,
]
# Keys needed in the turbine dics
KEYS_EXPECTED_TURBINES = [ID, SUBSTATION_ID]

# Keys needed in the substation-substation cable types
KEYS_EXPECTED_SUB_SUB_CABLE = [SUBSTATION_ID, OTHER_SUB_ID, CABLE_TYPE_SUBSUB]
