import sys
addedClauses = []  # ~p q    q ~p  are logically equivalent

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    KBFile = open(sys.argv[1], "r")
    KB = []
    for line in KBFile.readlines():
        KB.append(line.strip())
    print(KB)
    INITIAL_KB = KB[0:-1]
    negation = negateClause(KB[-1])  # negation contains array of negated clauses
#  for every clause in KB after

    # currentClause = resolve(clause) resolves with all previous KB entries
    # this is where we decide if we add to KB or not
    removeRepeatedLiterals(currentClause)
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
