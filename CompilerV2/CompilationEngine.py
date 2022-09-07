from constants import (
    TokenType,
    OPERATORS,
    KEYWORD_CONSTANTS,
    UNARY_OPERATORS,
    OPERATOR_COMMAND_MAP,
)
from SymbolTable import SymbolTable


class CompilationEngine:
    def __init__(self, input, output) -> None:
        """Creates a new compilation engine with the given input and output.
        The next routine called by the JackAnalyzer module must be compile_class."""
        self.tokenizer = input
        self.outfile = output
        self._count = -1

    @property
    def count(self):
        """Returns the value of a counter which is incremented each time it is accessed."""
        self._count += 1
        return self._count

    def _write_line(self, val):
        self.outfile.write(val + "\n")

    def _compile_symbol(self, done=False):
        tk = self.tokenizer
        if not done:
            tk.advance()

    def _compile_keyword(self):
        tk = self.tokenizer
        temp = tk.key_word()
        tk.advance()
        return temp

    def _compile_identifier(self):
        tk = self.tokenizer
        temp = tk.identifier()
        tk.advance()
        return temp

    def _compile_type(self) -> None:
        tk = self.tokenizer
        if tk.token_type() == TokenType.KEYWORD:
            temp = tk.key_word()
        elif tk.token_type() == TokenType.IDENTIFIER:
            temp = tk.identifier()
        tk.advance()
        return temp

    def _compile_subroutine_call(self) -> None:
        tk = self.tokenizer
        subroutine_name = self._compile_identifier()
        if tk.current_token.value == ".":
            self._compile_symbol()
            subroutine_name = ".".join((subroutine_name, self._compile_identifier()))
        self._compile_symbol()
        arg_count = self.compile_expression_list()
        self._write_line(f"call {subroutine_name} {arg_count}")
        self._compile_symbol()

    def _compile_string_const(self, string):
        length = len(string)
        # Save `this` somewhere
        self._write_line("push pointer 0")
        self._write_line("pop temp 0")
        # Call to create new string object
        self._write_line(f"push constant {length}")
        self._write_line("call String.new 1")
        # Update `this` to address of new string obj
        self._write_line("pop pointer 0")
        for ch in string[::-1]:
            self._write_line(f"push constant {ord(ch)}")
            self._write_line("call String.appendChar 1")
            # Rather than dumping the return value, I chose to update `this` which is fine
            self._write_line("pop pointer 0")

    def _compile_int_const(self, int_val):
        self._write_line(f"push constant {int_val}")

    def _compile_keyword_const(self, keyword):
        if keyword == "true":
            self._write_line("push constant 1")
            self._write_line("neg")
        elif keyword in ("false", "null"):
            self._write_line("push constant 0")
        else:
            raise RuntimeError(
                f"Invalid keyword. Expected true, fall, this, null. Got {keyword}."
            )

    def _lookup_identifier(self, identifier):
        """Returns a tuple of (kind, index) for a particular identifier
        Looks up first in Subroutine level symbol table then in Class level symbol table."""
        if kind := self._subroutine_table.kind_of(identifier):
            return (kind, self._subroutine_table.index_of(identifier))
        elif kind := self._class_table.kind_of(identifier):
            return (kind, self._subroutine_table.index_of(identifier))
        else:
            raise RuntimeError(f"Undefined identifier {identifier}.")

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self._class_table = SymbolTable()
        self._subroutine_table = SymbolTable()
        tk = self.tokenizer
        tk.advance()
        self._compile_keyword()
        self._class_name = self._compile_identifier()
        self._compile_symbol()
        while tk.current_token.value in ("static", "field"):
            self.compile_class_var_dec()
        while tk.current_token.value in ("constructor", "function", "method"):
            self.compile_subroutine()
        self._compile_symbol(True)

    def compile_class_var_dec(self) -> None:
        """Compiles a static variable declaration, or a field declaration."""
        tk = self.tokenizer
        kind = self._compile_keyword()
        symbol_type = self._compile_type()
        name = self._compile_identifier()
        self._class_table.define(name, symbol_type, kind)
        while tk.current_token.value != ";":
            self._compile_symbol()
            name = self._compile_identifier()
            self._class_table.define(name, symbol_type, kind)
        # print(self._class_table._table)
        self._compile_symbol()

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self._subroutine_table.reset()
        tk = self.tokenizer
        keyword = self._compile_keyword()
        if keyword == "method":
            self._subroutine_table.define("this", self._class_name, "argument")
        if tk.current_token.value == "void":
            self._compile_keyword()
        else:
            self._compile_type()
        subroutine_name = self._class_name + "." + self._compile_identifier()
        self._compile_symbol()
        self.compile_parameter_list()
        self._compile_symbol()
        self.compile_subroutine_body(subroutine_name)

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list. Does not handle the closing
        parenthesis tokens `(` and `)` ."""
        tk = self.tokenizer
        # Handle empty parameter list
        if tk.current_token.value == ")":
            return
        # Handle single parameter
        symbol_type = self._compile_type()
        name = self._compile_identifier()
        self._subroutine_table.define(name, symbol_type, "argument")
        # Handle all other parameters
        while tk.current_token.value != ")":
            self._compile_symbol()
            symbol_type = self._compile_type()
            name = self._compile_identifier()
            self._subroutine_table.define(name, symbol_type, "argument")

    def compile_subroutine_body(self, subroutine_name) -> None:
        """Compiles a subroutine's body."""
        tk = self.tokenizer
        self._compile_symbol()
        while tk.current_token.value == "var":
            self.compile_var_dec()
        local_var_count = self._subroutine_table.var_count("local")
        self._write_line(f"function {subroutine_name} {local_var_count}")
        self.compile_statements()
        self._compile_symbol()

    def compile_var_dec(self) -> None:
        """Compiles a `var` declaration."""
        tk = self.tokenizer
        self._compile_keyword()
        symbol_type = self._compile_type()
        name = self._compile_identifier()
        self._subroutine_table.define(name, symbol_type, "local")
        while tk.current_token.value != ";":
            self._compile_symbol()
            name = self._compile_identifier()
            self._subroutine_table.define(name, symbol_type, "local")
        self._compile_symbol()

    def compile_statements(self) -> None:
        """Compiles a sequence of statements. Does not handle the enclosing curly
        braces, `{` and `}` ."""
        tk = self.tokenizer
        while tk.current_token.value != "}":
            # print(self.token)
            if tk.current_token.value == "let":
                self.compile_let()
            elif tk.current_token.value == "if":
                self.compile_if()
            elif tk.current_token.value == "while":
                self.compile_while()
            elif tk.current_token.value == "do":
                self.compile_do()
            elif tk.current_token.value == "return":
                self.compile_return()

    def compile_let(self) -> None:
        """Compiles  a let statement."""
        tk = self.tokenizer
        self._compile_keyword()
        target = self._compile_identifier()
        kind, index = self._lookup_identifier(target)
        if tk.current_token.value == "[":
            self._compile_symbol()
            self.compile_expression()
            self._compile_symbol()
        self._compile_symbol()
        self.compile_expression()
        self._write_line(f"pop {kind} {index}")
        self._compile_symbol()

    def compile_if(self) -> None:
        """Compiles an if statement possibly with a trailing `else` clause."""
        tk = self.tokenizer
        self._compile_keyword()
        self._compile_symbol()
        self.compile_expression()
        self._compile_symbol()
        self._write_line("not")
        L1 = f"LABEL_{self._count}"
        L2 = f"LABEL_{self._count}"
        self._write_line(f"if-goto {L1}")
        self._write_line(f"goto {L2}")
        self._write_line(f"label {L1}")
        self._compile_symbol()
        self.compile_statements()
        self._compile_symbol()
        self._write_line(f"label {L2}")
        if tk.current_token.value == "else":
            self._compile_keyword()
            self._compile_symbol()
            self.compile_statements()
            self._compile_symbol()

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self._compile_keyword()
        L1 = f"LABEL_{self.count}"
        L2 = f"LABEL_{self.count}"
        self._write_line(f"label {L1}")
        self._compile_symbol()
        self.compile_expression()
        self._write_line("not")
        self._write_line(f"if-goto {L2}")
        self._compile_symbol()
        self._compile_symbol()
        self.compile_statements()
        self._compile_symbol()
        self._write_line(f"goto {L1}")
        self._write_line(f"label {L2}")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        tk = self.tokenizer
        self._compile_keyword()
        self._compile_subroutine_call()
        self._compile_symbol()
        # Discard return value from subroutine.
        # We use do statements only for their side effects.
        self._write_line("pop temp 0")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        tk = self.tokenizer
        self._compile_keyword()
        if tk.current_token.value == ";":
            self._write_line("return")
            self._compile_symbol()
            return
        self.compile_expression()
        self._write_line("return")
        self._compile_symbol()

    def compile_expression(self) -> None:
        """Compiles an expression."""
        tk = self.tokenizer
        self.compile_term()
        while (operator := tk.current_token.value) in OPERATORS:
            self._compile_symbol()
            self.compile_term()
            self._write_line(f"{OPERATOR_COMMAND_MAP[operator]}")

    def compile_term(self) -> None:
        """Compiles a term. If the current token is an identifier, the routine
        must resolve it into a variable, an array element, or a subroutine call.
        A single lookahead token, which may be `[`, `(`, or `.` suffices to distinguish
        between possibilities. Any other token is not part of this term and should not be
        advanced over."""
        tk = self.tokenizer
        if tk.token_type() == TokenType.STRING_CONST:
            self._compile_string_const(tk.string_val())
            tk.advance()
        elif tk.token_type() == TokenType.INT_CONST:
            self._compile_int_const(tk.int_val())
            tk.advance()
        elif tk.current_token.value in KEYWORD_CONSTANTS:
            self._compile_keyword_const(tk.current_token.value)
            tk.advance()
        elif tk.token_type() == TokenType.IDENTIFIER:
            next = tk._get_next_token().value
            # Array access
            if next == "[":
                self._compile_identifier()
                self._compile_symbol()
                self.compile_expression()
                self._compile_symbol()
            # Subroutine call
            elif next in (".", "("):
                self._compile_subroutine_call()
            # Variable
            else:
                identifier = self._compile_identifier()
                (kind, index) = self._lookup_identifier(identifier)
                self._write_line(f"push {kind} {index}")
        elif tk.current_token.value == "(":
            self._compile_symbol()
            self.compile_expression()
            self._compile_symbol()
        elif tk.current_token.value in UNARY_OPERATORS:
            self._compile_symbol()
            self.compile_term()
        else:
            raise RuntimeError(f"Invalid term. Got {tk.current_token.value}")

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma separated list of expressions. Returns the
        number of expressions in the list"""
        count = 0
        tk = self.tokenizer
        if tk.current_token.value == ")":
            return count
        self.compile_expression()
        count += 1
        while tk.current_token.value != ")":
            self._compile_symbol()
            self.compile_expression()
            count += 1
        return count
