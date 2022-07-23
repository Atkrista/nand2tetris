C_ARITHMETIC = "arithmetic"
C_PUSH = "push"
C_POP = "pop"
# C_GOTO = "goto"
# C_IF = "if"
# C_FUNCTION = "func"
# C_RETURN = "ret"
# C_CALL = "call"

C_ADD = "add"
C_PUSH = "push"
C_POP = "pop"
C_SUB = "sub"
C_NEG = "neg"
C_EQ = "eq"
C_GT = "gt"
C_LT = "lt"
C_AND = "and"
C_OR = "or"
C_NOT = "not"

COMMAND_TYPE_MAP = {
    C_POP: C_POP,
    C_PUSH: C_PUSH,
    C_ADD: C_ARITHMETIC,
    C_SUB: C_ARITHMETIC,
    C_NEG: C_ARITHMETIC,
    C_EQ: C_ARITHMETIC,
    C_GT: C_ARITHMETIC,
    C_LT: C_ARITHMETIC,
    C_AND: C_ARITHMETIC,
    C_OR: C_ARITHMETIC,
    C_NOT: C_ARITHMETIC,
}
