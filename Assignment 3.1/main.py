import sys
addedClauses = ()  # ~p q    q ~p  are logically equivalent
# to hold the line # in the KB, to be able to check resolution rule against
clausesChecked = ()


def readInKB():
    KBFile = open(sys.argv[1], "r")
    KB = []
    for line in KBFile.readlines():
        KB.append(line.strip())

    return KB


def removeClausesThatCancel(clause):
    clause = clause.copy()
    for literal in clause:
        if "~" in literal:
            if literal[1:] in clause:
                # remove both literals that cancel
                clause = clause.remove(literal[1:])
                clause = clause.remove(literal)
        else:
            if f"~{literal}" in clause:
                clause = clause.remove(f"~{literal}")
                clause = clause.remove(literal)
    return clause


def resolve(clause):
    resolvedClause = removeClausesThatCancel(clause)
    return resolvedClause


def removeRepeatedLiterals(clause):
    # convert list clause into a set to remove duplicates, reconverted into a list
    literals = set(clause)
    return literals.copy()


def negateClause(clause):
    literals = clause.split()  # split at every space, leaving conjunctions and literals

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
    # if and, assume false
    for literal in currentClause:
        if "~" in literal:
            if literal[1:] in currentClause:
                return True  # we found the negation as well
        else:
            if f"~{literal}" in currentClause:
                return True
    return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    KB = readInKB()
    INITIAL_KB = KB[0:-1]

    # negation contains array of negated clauses
    negation = negateClause(KB[-1])
    # TODO: add negation to KB?

    ''' Resolution should proceed as follows: 
        
        For each clause i[1,n] (where n is the last clause in the KB), 
            attempt to resolve clause i with every previous clause j[1,i) (in order). 
        
        If a new clause is generated, it is added to the end of the KB (therefore the value of n changes). 
        Your system should continue trying to resolve the next clause (i+1) with all previous clauses until
            1) a contradiction is found (in which case ’Contradiction’ should be added to the KB) or 
            2) all possible resolutions have been performed.
    '''

    for i in range(len(KB)):
        for j in range(0, i):
            # resolve clause
            clause = resolve(clause)
            clause = removeRepeatedLiterals(clause)
            if isRedundant(clause):
                pass
            elif isTrue(clause):
                pass
            else:
                KB.append(clause)
#  end for
