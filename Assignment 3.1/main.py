import sys


def readInKB(OUTPUT_CNT):
    KBFile = open(sys.argv[1], "r")
    KB = []

    for line in KBFile.readlines():
        KB.append(line.strip())

    for clause in KB[:-1]:
        print(f"{OUTPUT_CNT}. {clause} " + "{}")
        OUTPUT_CNT += 1

    return KB, OUTPUT_CNT


def add_negation(kb, clause_list, OUTPUT_CNT):
    kb = kb.copy()

    for literal in clause_list:
        if isRedundant(literal, kb):
            pass
        else:
            kb.append(literal)
            output_line(kb, OUTPUT_CNT)
            OUTPUT_CNT += 1
    return kb.copy(), OUTPUT_CNT


def resolutionApplicable(current_clause, clause_j):
    for literal in current_clause.split(" "):
        if literalNegation(literal) in clause_j.split(" "):
            return True, literal
    return False, None


def resolve(clause1, clause2, literal):
    c1 = set(clause1.split(" "))
    c2 = set(clause2.split(" "))
    c1.remove(literal)
    c2.remove(literalNegation(literal))
    resolvedClause = c1.union(c2)
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


# return a string representing the negation of a particular literal
def literalNegation(literal_to_negate):
    if "~" in literal_to_negate:
        new_literal = literal_to_negate[1:]
    else:
        new_literal = "~" + literal_to_negate
    return new_literal


def format_clause(clause):
    clause_str = ""
    cnt = len(clause)
    for literal in clause:
        clause_str += literal
        clause_str += " " if cnt > 1 else ""
        cnt -= 1
    return clause_str


def output_line(KB, OUTPUT_CNT, i=None, j=None, isNew=False):
    index_str = ("{" + f"{i+1}, {j+1}" "}") if isNew else ""
    output = f"{OUTPUT_CNT}. {KB[-1]} " + index_str
    print(output)
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    OUTPUT_CNT = 1
    KB, OUTPUT_CNT = readInKB(OUTPUT_CNT)

    # negation contains array of negated clauses
    negation = negateClause(KB[-1])
    KB = KB[0:-1]
    KB, OUTPUT_CNT = add_negation(KB, negation, OUTPUT_CNT)

    i = 0
    while i < len(KB):
        for j in range(0, i):
            applicable, literal = resolutionApplicable(KB[i], KB[j])
            if applicable:
                clause = resolve(KB[i], KB[j], literal)
                clause = removeRepeatedLiterals(clause)

                if isRedundant(clause, KB):
                    pass
                elif isTrue(clause):
                    pass
                else:
                    if len(clause) == 0:
                        print("Contradiction {" + f"{i+1}, {j+1}" + "}")
                        print("Valid")
                        exit()

                    KB.append(format_clause(clause))
                    output_line(KB, OUTPUT_CNT, i, j, True)
                    OUTPUT_CNT += 1
        i += 1
#  end for
