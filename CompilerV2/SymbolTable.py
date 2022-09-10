from typing import NamedTuple


class Symbol(NamedTuple):
    name: str
    symbol_type: str
    kind: str
    index: int


class SymbolTable:
    def __init__(self) -> None:
        """Creates a new symbol table."""
        self._table = []
        self._static_count = 0
        self._field_count = 0

    def reset(self) -> None:
        """Empties the symbol table, and resets the four indexes to 0. Should be called when starting to
        compile a subroutine declaration."""
        self._table = []
        self._arg_count = 0
        self._var_count = 0

    def define(self, name, symbol_type, kind) -> None:
        """Defines(adds to the table) a new variable of the given name, type, and kind. Assigns to
        it the index value of that kind, and adds 1 to the index."""
        if kind == "static":
            self._table.append(Symbol(name, symbol_type, "static", self._static_count))
            self._static_count += 1
        elif kind == "field":
            self._table.append(Symbol(name, symbol_type, "this", self._field_count))
            self._field_count += 1
        elif kind == "argument":
            self._table.append(Symbol(name, symbol_type, "argument", self._arg_count))
            self._arg_count += 1
        elif kind == "local":
            self._table.append(Symbol(name, symbol_type, "local", self._var_count))
            self._var_count += 1
        else:
            raise RuntimeError("kind must be one of static, field, argument, or local.")

    def var_count(self, kind) -> int:
        """Returns the number of variables of the given kind already defined in the table"""
        if kind in ("static", "this", "argument", "local"):
            return len(list(filter(lambda x: x.kind == kind, self._table)))
        else:
            raise RuntimeError("kind must be one of static, field, arg, or var.")

    def kind_of(self, name):
        """Returns the kind of the named identifier. If the identifier is not found, returns NONE."""
        if found := list(filter(lambda x: x.name == name, self._table)):
            return found[0].kind
        else:
            return None

    def type_of(self, name) -> str:
        """Returns the type of the named variable."""
        return list(filter(lambda x: x.name == name, self._table))[0].symbol_type

    def index_of(self, name) -> int:
        """Returns the index of the named variable."""
        return list(filter(lambda x: x.name == name, self._table))[0].index
