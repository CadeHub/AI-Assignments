import sys

variable_domains = {}
current_constraints = []  # format: {var1: str, op: op, var2: str}


def readInputFile(filename: str, callback):
    file = open(filename, "r")

    for line in file:
        callback(line)
    return []


def processVariablesFile(line: str):
    current_variable = line[0:1]
    domain = [int(x) for x in line[1:].split() if x.isnumeric()]
    variable_domains[current_variable] = domain
    return  # this will return json object of var with it's domain as values


def processConstraintFile(line: str):
    line = line.split()
    current_constraint = {"VAR1": line[0], "OP": line[1], "VAR2": line[2]}
    current_constraints.append(current_constraint)
    return  # this will return an array of constraints


'''
function most_constraining_variable(assignment, csp):
    unassigned_variables = csp.variables - set(assignment.keys())
    mcv = None
    max_constraints = -1
    
    for variable in unassigned_variables:
        num_constraints = 0
        for constraint in csp.constraints:
            if variable in constraint.scope and all(v in assignment for v in constraint.scope):
                num_constraints += 1
        if num_constraints > max_constraints:
            mcv = variable
            max_constraints = num_constraints
            
    return mcv

'''

'''
function most_constrained_variable(csp):
    variables = csp.variables
    unassigned_variables = [var for var in variables if not csp.is_assigned(var)]
    most_constrained_variable = None
    smallest_domain_size = float('inf')
    
    for var in unassigned_variables:
        domain_size = csp.domain_size(var)
        if domain_size < smallest_domain_size:
            smallest_domain_size = domain_size
            most_constrained_variable = var
    
    return most_constrained_variable
'''

'''
function least_constrained_value(variable, domain):
    // Sort values in domain by their number of constraints
    values = domain[variable]
    sorted_values = sort_by_constraints(variable, values)
    
    return sorted_values

function sort_by_constraints(variable, values):
    // Count the number of constraints for each value
    constraint_counts = []
    for value in values:
        count = 0
        for constraint in constraints:
            if constraint.involves(variable) and constraint.is_violated(value):
                count += 1
        constraint_counts[value] = count
    
    // Sort values by their constraint count
    sorted_values = sort(values, key=lambda value: constraint_counts[value])
    
    return sorted_values
'''

''' Main Code: '''
variable_file = sys.argv[1]
constraint_file = sys.argv[2]

readInputFile(variable_file, processVariablesFile)
readInputFile(constraint_file, processConstraintFile)

print(current_constraints)
