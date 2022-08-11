TYPE_ARITHMETIC = "ARITHMETIC"
TYPE_PUSH = "PUSH"
TYPE_POP = "POP"
TYPE_LABEL = "LABEL"
TYPE_GOTO = "GOTO"
TYPE_IF_GOTO = "IF_GOTO"

C_POP = "pop"
C_PUSH = "push"
C_ADD = "add"
C_SUB = "sub"
C_NEG = "neg"
C_EQ = "eq"
C_GT = "gt"
C_LT = "lt"
C_AND = "and"
C_OR = "or"
C_NOT = "not"
C_LABEL = "label"
C_GOTO = "goto"
C_IF_GOTO = "if-goto"
C_FUNC = "function"
C_CALL = "call"
C_RET = "return"

COMMAND_TYPE_MAP = {
    C_POP: TYPE_POP,
    C_PUSH: TYPE_PUSH,
    C_LABEL: TYPE_LABEL,
    C_GOTO: TYPE_GOTO,
    C_IF_GOTO: TYPE_IF_GOTO,
    C_ADD: TYPE_ARITHMETIC,
    C_SUB: TYPE_ARITHMETIC,
    C_NEG: TYPE_ARITHMETIC,
    C_EQ: TYPE_ARITHMETIC,
    C_GT: TYPE_ARITHMETIC,
    C_LT: TYPE_ARITHMETIC,
    C_AND: TYPE_ARITHMETIC,
    C_OR: TYPE_ARITHMETIC,
    C_NOT: TYPE_ARITHMETIC,
}

TYPE_COMMAND_MAP = {
    TYPE_POP: C_POP,
    TYPE_PUSH: C_PUSH,
    TYPE_LABEL: C_LABEL,
    TYPE_IF_GOTO: C_IF_GOTO,
    TYPE_GOTO: C_GOTO,
}


def get_branching_types():
    return (TYPE_LABEL, TYPE_GOTO, TYPE_IF_GOTO)


def get_push_pop_types():
    return (TYPE_PUSH, TYPE_POP)
