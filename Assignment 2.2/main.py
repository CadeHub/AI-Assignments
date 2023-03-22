import sys

csp = {
    "variable_domains": {},
    "constraints": [],
    "state": {}
}

DEFAULT_VAR_DOMAINS = {}


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


def getUnassignedVariables(csp):
    return DEFAULT_VAR_DOMAINS.keys() - csp["state"].keys()


def selectVariable(csp):
    unassigned_variables = getUnassignedVariables(csp)

    mcv = getMostConstrainedVariable(csp, unassigned_variables)
    if len(mcv) > 1:  # tie between values
        print(mcv)
        # find most constraining variable (return array with corresponding constraining values)
        mcv = getMostConstrainingVariable(csp, mcv)
        # if there is a tie, sort alphabetically, choose first
    return mcv  # variable chosen


def getMostConstrainedVariable(csp, var_choices):
    num_constraints = 9999
    mcv = []  # array in case they tie
    # loop through choices
    for var in var_choices:
        curr_domain_len = len(csp["variable_domains"][var])

        # if number of constraints for var is less than previous min
        if curr_domain_len < num_constraints:
            num_constraints = curr_domain_len
            # clear the array and add this variable as the mcv
            mcv = []
            mcv.append(var)
        # if there is a tie
        elif curr_domain_len == num_constraints:
            mcv.append(var)

    return mcv


def getMostConstrainingVariable(csp, var_choices):
    unassigned_variables = list(
        {var for var in csp["state"] if csp["state"][var]})
    mcv = None
    max_constraints = -1

    # for variable in unassigned_variables:
    # num_constraints = 0
    # for constraint in csp.constraints:
    # if variable in constraint.scope and all(v in assignment for v in constraint.scope):
    # num_constraints += 1
    # if num_constraints > max_constraints:
    # mcv = variable
    # max_constraints = num_constraints

    return mcv


def breakTieAlphabetically(csp):
    # if 2 variables have the same constrained and constraining level
        # choose variable that appears first alphabetically
    return  # variable chosen


def selectValue(csp, v):
    # find least constraining value for variable v # if forward checking enabled, make sure to choose from that list
    # if tie exists between values:
        # choose smaller value
    return  # value chosen (if none available, return null)


def getLeastConstrainedValue(variable, domain):
    # Sort values in domain by their number of constraints
    # values = domain[variable]
    # sorted_values = sortByConstraints(variable, values)

    return  # sorted_values


def sortByConstraints(variable, values):
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


# return false if no constraint has been violated, true if violation occurs
def checkConstraintViolation(constraint, state):
    violated = False
    var1 = constraint["VAR1"]
    var2 = constraint["VAR2"]
    operation = constraint["OP"]

    # if one of the values is unassigned, return false
    if (var1 not in state.keys()) or (var2 not in state.keys()):
        return False
    else:
        var1 = state[var1]
        var2 = state[var2]

    if operation == "<":
        violated = var1 < var2
    elif operation == ">":
        violated = var1 > var2
    elif operation == "=":
        violated = var1 == var2
    elif operation == "!":
        violated = var1 != var2
    else:
        print("ERROR: Unknown constraint")
        exit()
    return not violated


def checkConstraintViolations(csp):
    violated = False

    # loop through csp constraints that involve var (we only bother checking most recently assigned variable, assuming previous set values are valid)
    for var in csp["state"].keys():
        for constraint in csp["constraints"]:
            # if current variable is a part of the constraint we're looking at
            if constraint["VAR1"] == var or constraint["VAR2"] == var:
                # check for violation
                violated = checkConstraintViolation(constraint, csp["state"])

                if violated:  # if at any point we make a violation, return then that it occurred
                    return violated
    return violated


def checkComplete(csp):  # return true if no constraints violated, and all variables assigned
    constraints_violated = checkConstraintViolations(csp)
    unassigned_variable_cnt = len(getUnassignedVariables(csp))
    return ((not constraints_violated) and (unassigned_variable_cnt == 0))


def outputCurrentBranch(csp, complete):
    output_str = ""
    total_variable_cnt = len(DEFAULT_VAR_DOMAINS.keys())
    unassigned_variable_cnt = len(getUnassignedVariables(csp))
    assigned_variable_cnt = total_variable_cnt - unassigned_variable_cnt
    cnt = 0

    # loop through current state
    for var, val in csp["state"].items():
        if(val != None):
            output_str += f"{var}={val}"

            # if not last item
            if(cnt < assigned_variable_cnt - 1):
                output_str += ", "
            else:
                output_str += "\tsolution" if (complete) else "\tfailure"

        cnt += 1
    print(output_str)
    return


''' MAIN LOOP '''


def solveCSP(csp):
    complete = checkComplete(csp)
    if complete:
        # TODO: remove
        print("COMPLETED!")
        return

    # var <- Select-Unassigned-Variable(assignment, constraints)
    # note, we'll need to update domain accordingly after choice
    var = selectVariable(csp)

    # for value in Order-Domain-Values(var, assignment, constraints):
    #     if value satisfies constraints with assignment:
    #         assignment[var] <- value
    #         inference <- Inference(assignment, constraints, var, value)
    #         if inference is not failure:
    #             result <- Backtracking-Search(assignment + inference, constraints)
    #             if result is not failure:
    #                 return result
    #     assignment[var] <- unassigned
    #     Restore-Domain-Values(var)
    #     outputCurrentBranch(csp, complete)

    # return failure
    return


''' Main Code: '''
variable_file = sys.argv[1]
constraint_file = sys.argv[2]
isForwardChecking = True if (len(sys.argv) == "fc") else False

readInputFile(variable_file, processVariablesFile)
readInputFile(constraint_file, processConstraintFile)
# the domains will be modified if using forward checking, we'll need to reset the domains on backtrack
DEFAULT_VAR_DOMAINS = csp["variable_domains"]

# print(csp)
# print(isForwardChecking)
# csp["state"]["Z"] = 1
# csp["state"]["X"] = 0
# csp["state"]["Y"] = 0

# outputCurrentBranch(csp, False)
# print(f"Violations: {checkConstraintViolations(csp)}")
# print(f"Complete: {checkComplete(csp)}")
print(selectVariable(csp))
