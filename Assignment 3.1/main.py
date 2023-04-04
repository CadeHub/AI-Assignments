import sys


def negateClause(clause):
    literals = clause.split()  # split at every space, leaving conjunctions and literals
    print(literals)
    for l in range(len(literals)):  # negate every individual literal, if it has a ~, remove it and if not, add it
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

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    KBFile = open(sys.argv[1], "r")
    KB = []
    for line in KBFile.readlines():
        KB.append(line.strip())
    print(KB)
    negation = negateClause(KB[-1])
    # if negation has '&' split and add separately to KB from left to right

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
