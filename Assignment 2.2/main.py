import sys

csp = {
    "variable_domains": {},
    "constraints": [],
    "state": {}
}

DEFAULT_VAR_DOMAINS = {}
PREV_VAR_DOMAINS = {}
IS_FC = False


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
        # print(f"most constrained variable: {mcv}")
        # find most constraining variable (return array with corresponding constraining values)
        mcv = getMostConstrainingVariable(csp, mcv)
        # print(f"most constraining variable: {mcv}")

        # if there is a tie, sort alphabetically, choose first
        if len(mcv) > 1:
            mcv.sort()
    return mcv[0]  # variable chosen


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
    # print(f"most constrained variable: {mcv}")
    return mcv


def getMostConstrainingVariable(csp, var_choices):
    mcv = []
    max_constraints = -1

    for var in var_choices:
        num_constraints = 0
        for constraint in csp["constraints"]:
            # if current variable involved in current constraint AND other var in constraint is unassigned
            other_var = [x for x in constraint.values() if x.isalpha()
                         and x != var]
            other_var = other_var[0]
            if var in constraint.values() and other_var not in csp["state"].keys():
                num_constraints += 1

        if num_constraints > max_constraints:
            mcv = []
            mcv.append(var)
            max_constraints = num_constraints
        elif num_constraints == max_constraints:
            mcv.append(var)
    return mcv


def getLeastConstrainedValue(csp, var):
    return sortByConstraints(csp, var)  # sortByRemainingDomain(csp, var)


def getDomainAfterAssignment(csp, var, val, unassigned_var):
    remaining_domain = csp["variable_domains"][unassigned_var].copy()

    # loop through constraints
    for constraint in csp["constraints"]:
        # if both current var and unassigned_var involved in constraint
        if var in constraint.values() and unassigned_var in constraint.values():
            # loop through remaining domain for the unassigned variable
            for potential_val in remaining_domain:
                curr_state = {var: val, unassigned_var: potential_val}

                # if constraint is violated with potential val
                if checkConstraintViolation(constraint, curr_state):
                    # remove potential val from remaining domain
                    remaining_domain.remove(potential_val)

    return remaining_domain


def sortByRemainingDomain(csp, var):
    domain = csp["variable_domains"][var]
    unassigned_variables = getUnassignedVariables(csp)
    unassigned_variables.remove(var)

    remaining_choices = {}

    # loop through domain of current variable
    for val in domain:
        # for each remaining unassigned variable
        for unassigned_var in unassigned_variables:
            # if var is assigned to current val
            # how large is remaining domain
            remaining_choices[val] = len(
                getDomainAfterAssignment(csp, var, val, unassigned_var))

    sorted_values = sorted(remaining_choices.items(), key=lambda x: x[1])
    sorted_values = [val[0] for val in sorted_values]
    # print(sorted_values)
    return sorted_values

# sort values in domain by their number of constraints


def sortByConstraints(csp, var):
    potential_values = csp["variable_domains"][var]
    constraints = csp["constraints"]

    constraint_counts = {}  # num constraints per value

    for val in potential_values:
        count = 0
        for constraint in constraints:
            # if consraint is violated by value, increase count
            if var in constraint.values() and not checkConstraintViolations(csp):
                count += 1
        constraint_counts[val] = count

    # sort values by their constraint count
    sorted_values = sorted(constraint_counts.items(), key=lambda x: x[1])
    sorted_values = [val[0] for val in sorted_values]
    return sorted_values


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


def checkConstraintViolations(csp, var=None, val=None):
    violated = False
    state = csp["state"].copy()

    state[var] = val
    # if var != None:
    #     print(f"Checking for constraint with new state {state}")

    # loop through csp constraints that involve var (we only bother checking most recently assigned variable, assuming previous set values are valid)
    for constraint in csp["constraints"]:
        # if current variable is a part of the constraint we're looking at
        if var in constraint.values():
            # check for violation
            violated = checkConstraintViolation(constraint, state)

            if violated:  # if at any point we make a violation, return then that it occurred
                # print(f"violation occured with {var}={val}")
                return violated
    return violated


def updateDomain(csp, var, val):
    # if IS_FC:
    #     # loop through the domain of each unassigned variable
    #     for unassigned_var in getUnassignedVariables(csp):
    #         for unassigned_val in csp["variable_domains"][unassigned_var]:

    #             # loop through all constraints
    #             for constraint in csp["constraints"]:
    #                 # if constraint involves var and violation occurs
    #                 if var in constraint.values() and checkConstraintViolation(csp, var, val):
    #                 print()
    # else:
    csp["variable_domains"][var].remove(val)
    return


def resetVariableDomain(csp, var):
    csp["variable_domains"][var] = DEFAULT_VAR_DOMAINS[var].copy()
    return


def checkComplete(csp):  # return true if no constraints violated, and all variables assigned
    constraints_violated = checkConstraintViolations(csp)
    unassigned_variable_cnt = len(getUnassignedVariables(csp))
    return ((not constraints_violated) and (unassigned_variable_cnt == 0))


def outputCurrentBranch(csp, complete, failed_assignment=None):
    output_str = ""
    total_variable_cnt = len(DEFAULT_VAR_DOMAINS.keys())
    unassigned_variable_cnt = len(getUnassignedVariables(csp))
    assigned_variable_cnt = total_variable_cnt - unassigned_variable_cnt
    cnt = 0
    state = csp["state"].copy()

    if failed_assignment:
        state[failed_assignment[0]] = failed_assignment[1]
        assigned_variable_cnt += 1

    # loop through current state
    for var, val in state.items():
        if(val != None):
            output_str += f"{var}={val}"

            # if not last item
            if(cnt < assigned_variable_cnt - 1):
                output_str += ", "
            else:
                output_str += "  solution" if (complete) else "  failure"

        cnt += 1
    print(output_str)
    return


''' MAIN LOOP '''


def solveCSP(csp):
    complete = checkComplete(csp)
    if complete:
        outputCurrentBranch(csp, complete)
        return True

    var = selectVariable(csp)

    for val in getLeastConstrainedValue(csp, var):
        # print(f"trying {var}={val}")
        # if no constraints violated with assignment
        if not checkConstraintViolations(csp, var, val):
            csp["state"][var] = val

            # update domain following assignment
            updateDomain(csp, var, val)
            # print(f"updated domains: {csp['variable_domains']}")

            result = solveCSP(csp)

            if result == True:
                return result

            # remove var assignment
            csp["state"].pop(var)
        else:
            failed_assignment = (var, val)
            outputCurrentBranch(csp, False, failed_assignment)
    return False


''' Main Code: '''
if __name__ == "__main__":
    # read in command line arguments
    variable_file = sys.argv[1]
    constraint_file = sys.argv[2]
    IS_FC = True if (sys.argv[3] == "fc") else False

    # read in files
    readInputFile(variable_file, processVariablesFile)
    readInputFile(constraint_file, processConstraintFile)

    # the domains will be modified if using forward checking, we'll need to reset the domains on backtrack
    DEFAULT_VAR_DOMAINS = csp["variable_domains"]

    # main code
    solveCSP(csp)
