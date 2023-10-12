# INSTANCE CONSTANTS
# Encompasses all categories in instance
PARAMETERS = "parameters"

# Size parameters
SIZE = "size"
NB_JOBS = "nb_jobs"
NB_TASKS = "nb_tasks"
NB_MACHINES = "nb_machines"
NB_OPERATORS = "nb_operators"

# Costs parameters
COSTS = "costs"
UNIT_PENALTY = "unit_penalty"
TARDINESS = "tardiness"

# Jobs
JOBS = "jobs"
JOB = "job"
SEQUENCE = "sequence"
RELEASE_DATE = "release_date"
DUE_DATE = "due_date"
WEIGHT = "weight"

# Tasks
TASKS = "tasks"
TASK = "task"
PROCESSING_TIME = "processing_time"

# Machines
MACHINES = "machines"
MACHINE = "machine"
OPERATORS = "operators"

# SOLUTION CONSTANTS
START = "start"
OPERATOR = "operator"


# Keys needed in solutions
KEYS_EXPECTED = [TASK, START, MACHINE, OPERATOR]
# Maximum size of values in solution
MATCHING = {TASK: NB_TASKS, OPERATOR: NB_OPERATORS, MACHINE: NB_MACHINES}
