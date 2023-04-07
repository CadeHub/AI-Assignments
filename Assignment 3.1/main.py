import sys
addedClauses = []  # ~p q    q ~p  are logically equivalent


def removeRepeatedLiterals(clause):
    # convert list clause into a set to remove duplicates, reconverted into a list
    literals = list(set(clause))
    return literals.copy()


def negateClause(clause):
    literals = clause.split()  # split at every space, leaving conjunctions and literals
    print(literals)
    # negate every individual literal, if it has a ~, remove it and if not, add it
    for l in range(len(literals)):
        if "~" in literals[l]:
            literals[l] = literals[l].strip("~")
        else:
            literals[l] = "~" + literals[l]

    return literals.copy()


def isRedundant(currentClause):
    # loop thru current clauses, and see if any of them match, regardless of order
    for clause in addedClauses:
        if set(currentClause) == set(clause):
            return True
    return False


def isTrue(currentClause):
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    KBFile = open(sys.argv[1], "r")
    KB = []
    for line in KBFile.readlines():
        KB.append(line.strip())
    print(KB)
    INITIAL_KB = KB[0:-1]
    # negation contains array of negated clauses
    negation = negateClause(KB[-1])
#  for every clause in KB after

    # currentClause = resolve(clause) resolves with all previous KB entries
    # this is where we decide if we add to KB or not
    currentClause = removeRepeatedLiterals(currentClause)
    if isRedundant(currentClause):
        pass
    elif isTrue(currentClause):
        pass
    else:
        KB.append(currentClause)
#  end for

    # check redudndancy
    # check repeated literals
    # check if it evaluates to true
    # if all pass, add to KB
