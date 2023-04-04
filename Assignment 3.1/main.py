import sys


def negateClause(clause):
    literals = clause.split()  # split at every space, leaving conjunctions and literals
    print(literals)
    # negate every individual literal, if it has a ~, remove it and if not, add it
    for l in range(len(literals)):
        if "~" in literals[l]:
            literals[l] = literals[l].strip("~")
        else:
            literals[l] = "~" + literals[l]

    negation = ""
    for l in range(len(literals)-1):
        negation += literals[l] + "&"
    negation += literals[-1]
    print(negation)
    return negation


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    KBFile = open(sys.argv[1], "r")
    KB = []
    for line in KBFile.readlines():
        KB.append(line.strip())
    print(KB)
    negation = negateClause(KB[-1])
    # if negation has '&' split and add separately to KB from left to right
