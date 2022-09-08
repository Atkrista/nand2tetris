from enum import Enum


class TokenType(Enum):
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STRING_CONST = "stringConstant"


class KeyWord(Enum):
    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"
    CONSTRUCTOR = "constructor"
    INT = "int"
    BOOLEAN = "boolean"
    CHAR = "char"
    VOID = "void"
    VAR = "var"
    STATIC = "static"
    FIELD = "field"
    LET = "let"
    DO = "do"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    THIS = "this"


token_keyword_map = {e.value: e for e in KeyWord}

SYMBOLS = (
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ".",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
    "~",
)

OPERATORS = ("+", "-", "*", "&", "|", "<", ">", "=", "/")
UNARY_OPERATORS = ("-", "~")

OPERATOR_COMMAND_MAP = {
    "+": "add",
    "-": "sub",
    "&": "and",
    "|": "or",
    "<": "lt",
    ">": "gt",
    "=": "eq",
    "/": "call Math.divide 2",
    "*": "call Math.multiply 2",
}

UNARY_OPERATOR_COMMAND_MAP = {
    "-": "neg",
    "~": "not",
}


KEYWORD_CONSTANTS = ("true", "false", "null", "this")
