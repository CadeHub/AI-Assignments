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

def add_negation(kb, clause_list):
    kb = kb.copy()
    for literal in clause_list:
        if isRedundant(literal, kb):
            pass
        else:
            kb.append(literal)
    return kb.copy()


def resolutionApplicable(current_clause, clause_j):
    if type(current_clause) == str:
        current_clause = current_clause.split(" ")
    if type(clause_j) == str:
        clause_j = clause_j.split(" ")
    for literal in current_clause:
        if literalNegation(literal) in clause_j:
            return True, literal
    return False, None

def resolve(clause1, clause2, literal):
    print(f"1: {clause1}, 2: {clause2}, literal: {literal}")
    if type(clause1) == str:
        clause1 = clause1.split(" ")
    if type(clause2) == str:
        clause2 = clause2.split(" ")
    c1 = set(clause1)
    c2 = set(clause2)
    c1.remove(literal)
    c2.remove(literalNegation(literal))
    print(f"c1: {c1}, c2: {c2}, literal: {literal}")
    resolvedClause = c1.union(c2)
    print(resolvedClause)
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


def isRedundant(currentClause, KB):
    # loop thru current clauses, and see if any of them match, regardless of order
    for clause in KB:
        if type(clause) == str:
            clause = clause.split(" ")

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

def literalNegation(literal_to_negate):  # return a string representing the negation of a particular literal
    if "~" in literal_to_negate:
        new_literal = literal_to_negate[1:]
    else:
        new_literal = "~"+literal_to_negate
    return new_literal

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    KB = readInKB()

    # negation contains array of negated clauses
    negation = negateClause(KB[-1])

    KB = KB[0:-1]
    # TODO: add negation to KB?
    KB = add_negation(KB, negation)
    print(KB)

    ''' Resolution should proceed as follows: 
        
        For each clause i[1,n] (where n is the last clause in the KB), 
            attempt to resolve clause i with every previous clause j[1,i) (in order). 
        
        If a new clause is generated, it is added to the end of the KB (therefore the value of n changes). 
        Your system should continue trying to resolve the next clause (i+1) with all previous clauses until
            1) a contradiction is found (in which case ’Contradiction’ should be added to the KB) or 
            2) all possible resolutions have been performed.
    '''

    # MAIN_LOOP
    # main for loop tries to find a j in order 0 to j that can be resolved with i
    # then, resolve i with all j that can be resolved
    # resolution should return one of 2: new clause, Fail
    # seemingly expensive algorithm to find a j that can be resolved:
    #   1. for all literals in i, see if literalNegation(literal) is in j
    #   2. if not, resolution cannot be applied
    #   3. if so, apply resolution and derive either failure or a new clause
    #   4. if at any point there is a FAILURE, proof by negation has occurred and we can finish
    i = 0
    while i < len(KB):
        for j in range(0, i):
            # resolve clause
            # print("I, J: " + KB[i]+", " + KB[j])

            applicable, literal = resolutionApplicable(KB[i], KB[j])
            if applicable:
                print(f"index 1: {i}, index 2: {j}")
                clause = resolve(KB[i], KB[j], literal)  # resolve should likely have 2 parameters, clause i an clause j
                # if clause == FAILURE, proof by negation successful, finish
                clause = removeRepeatedLiterals(clause)
                if isRedundant(clause, KB):
                    pass
                elif isTrue(clause):
                    pass
                else:
                    if len(clause) == 0:
                        print("Contradiction Found")
                        exit()
                    KB.append(clause)
                    print(f"new KB: {KB}\n")
        i += 1
#  end for
