import sys

csp = {
    "variable_domains": {},
    "constraints": [],
    "state": {}
}


def readInputFile(filename: str, callback):
    file = open(filename, "r")

    for line in file:
        callback(line)
    return []


def processVariablesFile(line: str):
    current_variable = line[0:1]
    domain = [int(x) for x in line[1:].split() if x.isnumeric()]

    csp["variable_domains"][current_variable] = domain
    return  # this will set a json object of var with it's domain as values


def processConstraintFile(line: str):
    line = line.split()
    current_constraint = {"VAR1": line[0], "OP": line[1], "VAR2": line[2]}

    csp["constraints"].append(current_constraint)
    return  # this will set an array of constraints


''' HEURISTIC FUNCTIONS '''


def chooseVariable(csp):
    # find most constrained variables (return array with corresponding constraint values)
    # if there is a tie between top variables:
        # find most constraining variable (return array with corresponding constraining values)
        # if there is a tie, sort alphabetically, choose first
    return  # variable chosen


def chooseValue(csp, v):
    # find least constraining value for variable v # if forward checking enabled, make sure to choose from that list
    # if tie exists between values:
        # choose smaller value
    return  # value chosen (if none available, return null)


def most_constraining_variable(assignment, csp):
    # unassigned_variables = csp.variables - set(assignment.keys())
    # mcv = None
    # max_constraints = -1

    # for variable in unassigned_variables:
        # num_constraints = 0
        # for constraint in csp.constraints:
            # if variable in constraint.scope and all(v in assignment for v in constraint.scope):
                # num_constraints += 1
        # if num_constraints > max_constraints:
            # mcv = variable
            # max_constraints = num_constraints

    return  # mcv


def most_constrained_variable(csp):
    # variables = csp.variables
    # unassigned_variables = [var for var in variables if not csp.is_assigned(var)]
    # most_constrained_variable = None
    # smallest_domain_size = float('inf')

    # for var in unassigned_variables:
        # domain_size = csp.domain_size(var)
        # if domain_size < smallest_domain_size:
            # smallest_domain_size = domain_size
            # most_constrained_variable = var

    return  # most_constrained_variable


def break_tie_alphabetically(csp):
    # if 2 variables have the same constrained and constraining level
        # choose variable that appears first alphabetically
    return  # variable chosen


def least_constrained_value(variable, domain):
    # Sort values in domain by their number of constraints
    # values = domain[variable]
    # sorted_values = sort_by_constraints(variable, values)

    return  # sorted_values


def sort_by_constraints(variable, values):
    # Count the number of constraints for each value
    # constraint_counts = []
    # for value in values:
        # count = 0
        # for constraint in constraints:
            # if constraint.involves(variable) and constraint.is_violated(value):
                # count += 1
        # constraint_counts[value] = count

    # Sort values by their constraint count
    # sorted_values = sort(values, key=lambda value: constraint_counts[value])

    return  # sorted_values


''' RUNTIME FUNCTIONS '''


def checkConstraintViolations(csp):
    # loop through csp constraints
        # if variable is not null in state:
            # violation = getViolated(constraint, state)
    return


def backtrackToPreviousVariable(csp):
    # take variable to repeal
    # unassign it
    # unassign variable that we are assigning now
    # increment / decrement value by 1 if possible
    return


''' MAIN LOOP '''


def solveCSP(csp):
    # while states not all filled
        # var heuristic choice
        # choose value based on heuristic (consider forward checking if enabled)
        # assign value
        # check for constraint violations
        # while constraint violated, and values still left to try
            # try next value possible
        # if finish loop and no values left to try
            # backtrack to previously assigned value, and try next value assignment

    return  # state assignment


''' Main Code: '''
variable_file = sys.argv[1]
constraint_file = sys.argv[2]

readInputFile(variable_file, processVariablesFile)
readInputFile(constraint_file, processConstraintFile)

print(csp)
