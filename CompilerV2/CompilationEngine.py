from constants import (
    TokenType,
    OPERATORS,
    KEYWORD_CONSTANTS,
    UNARY_OPERATORS,
)
from SymbolTable import SymbolTable
from VMWriter import VMWriter


class CompilationEngine:
    def __init__(self, input, output) -> None:
        """Creates a new compilation engine with the given input and output.
        The next routine called by the JackAnalyzer module must be compile_class."""
        self.tokenizer = input
        self.writer = VMWriter(output)
        self._count = -1

    @property
    def count(self):
        """Returns the value of a counter which is incremented each time it is accessed."""
        self._count += 1
        return self._count

    @property
    def token(self):
        return self.tokenizer.current_token.value

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
        # handle calls like Square.new() or game.run() or Output.printString()
        if tk._get_next_token().value == ".":
            self._compile_explicit_method_call()
        # handle implicit method calls like do draw()
        else:
            self._compile_implicit_method_call()

    def _compile_explicit_method_call(self) -> None:
        tk = self.tokenizer
        # Name of object
        first = self._compile_identifier()
        kind = self._subroutine_table.kind_of(first) or self._class_table.kind_of(first)
        # An identifier we can't find in the two symbol tables must be an OS subroutine like
        # Memory.alloc() or Output.printString()
        if not kind:
            self._compile_symbol()
            second = self._compile_identifier()
            self._compile_symbol()
            n_args = self.compile_expression_list()
            self._compile_symbol()
            self.writer.write_call(".".join((first, second)), n_args)
            return
        kind, idx, first_type = self._lookup_identifier(first)
        # Push the object as arg 0
        self.writer.write_push(kind, idx)
        self._compile_symbol()
        second = self._compile_identifier()
        self._compile_symbol()
        n_args = self.compile_expression_list() + 1
        self._compile_symbol()
        self.writer.write_call(".".join((first_type, second)), n_args)

    def _compile_implicit_method_call(self) -> None:
        tk = self.tokenizer
        name = self._compile_identifier()
        # Push the object as arg 0
        self.writer.write_push("pointer", 0)
        self._compile_symbol()
        n_args = self.compile_expression_list() + 1
        self._compile_symbol()
        self.writer.write_call(".".join((self._class_name, name)), n_args)

    def _compile_string_const(self, string):
        length = len(string)
        self.writer.write_push("constant", length)
        self.writer.write_call("String.new", 1)
        for ch in string:
            self.writer.write_push("constant", ord(ch))
            self.writer.write_call("String.appendChar", 2)

    def _compile_int_const(self, int_val):
        self.writer.write_push("constant", int_val)

    def _compile_keyword_const(self, keyword):
        # print("HERE")
        if keyword == "true":
            self.writer.write_push("constant", 1)
            self.writer.write_arithmetic("-", True)
        elif keyword in ("false", "null"):
            self.writer.write_push("constant", 0)
        elif keyword == "this":
            self.writer.write_push("pointer", 0)
        else:
            raise RuntimeError(
                f"Invalid keyword. Expected true, fall, this, null. Got {keyword}."
            )

    def _lookup_identifier(self, identifier):
        """Returns a tuple of (kind, index, type) for a particular identifier
        Looks up first in Subroutine level symbol table then in Class level symbol table."""
        if kind := self._subroutine_table.kind_of(identifier):
            return (
                kind,
                self._subroutine_table.index_of(identifier),
                self._subroutine_table.type_of(identifier),
            )
        elif kind := self._class_table.kind_of(identifier):
            return (
                kind,
                self._class_table.index_of(identifier),
                self._class_table.type_of(identifier),
            )
        else:
            raise RuntimeError(f"Undefined identifier {identifier}.")

    def _compile_array(self, fetch_value=True) -> None:
        """Compiles an entire array expression array[expression] and puts it on the top of the stack.
        Optionally skips fetching value of array element."""
        tk = self.tokenizer
        arr_name = self._compile_identifier()
        kind, index, _ = self._lookup_identifier(arr_name)
        self._compile_symbol()
        self.compile_expression()
        self._compile_symbol()
        self.writer.write_push(kind, index)
        self.writer.write_arithmetic("+")
        if fetch_value:
            self.writer.write_pop("pointer", 1)
            self.writer.write_push("that", 0)

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
        self._compile_symbol()
        while tk.current_token.value == "var":
            self.compile_var_dec()
        local_var_count = self._subroutine_table.var_count("local")
        self.writer.write_function(subroutine_name, local_var_count)
        # Code to generate the object in memory
        if keyword == "constructor":
            size = self._class_table.var_count("this")
            self.writer.write_push("constant", size)
            self.writer.write_call("Memory.alloc", 1)
            self.writer.write_pop("pointer", 0)
        if keyword == "method":
            # Align the `this` segment of object for this method
            self.writer.write_push("argument", 0)
            self.writer.write_pop("pointer", 0)
        self.compile_subroutine_body()

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

    def compile_subroutine_body(self) -> None:
        """Compiles a subroutine's body."""
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
        if tk._get_next_token().value == "[":
            # Handle arrays as targets
            # ex: arr[expr] = expr;
            self._compile_array(fetch_value=False)
            self._compile_symbol()
            self.compile_expression()
            self._compile_symbol()
            # Save value of RHS
            self.writer.write_pop("temp", 0)
            self.writer.write_pop("pointer", 1)
            self.writer.write_push("temp", 0)
            self.writer.write_pop("that", 0)

        else:
            # Handle normal variables as targets
            var_name = self._compile_identifier()
            self._compile_symbol()
            self.compile_expression()
            self._compile_symbol()
            kind, index, _ = self._lookup_identifier(var_name)
            self.writer.write_pop(kind, index)

    def compile_if(self) -> None:
        """Compiles an if statement possibly with a trailing `else` clause."""
        tk = self.tokenizer
        L1 = f"LABEL_{self.count}"
        L2 = f"LABEL_{self.count}"
        self._compile_keyword()
        self._compile_symbol()
        self.compile_expression()
        self._compile_symbol()
        self.writer.write_arithmetic("~", True)
        self.writer.write_if(L1)
        self._compile_symbol()
        self.compile_statements()
        self.writer.write_goto(L2)
        self._compile_symbol()
        self.writer.write_label(L1)
        if tk.current_token.value == "else":
            self._compile_keyword()
            self._compile_symbol()
            self.compile_statements()
            self._compile_symbol()
        self.writer.write_label(L2)

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self._compile_keyword()
        L1 = f"LABEL_{self.count}"
        L2 = f"LABEL_{self.count}"
        self.writer.write_label(L1)
        self._compile_symbol()
        self.compile_expression()
        self.writer.write_arithmetic("~", True)
        self.writer.write_if(L2)
        self._compile_symbol()
        self._compile_symbol()
        self.compile_statements()
        self._compile_symbol()
        self.writer.write_goto(L1)
        self.writer.write_label(L2)

    def compile_do(self) -> None:
        """Compiles a do statement."""
        tk = self.tokenizer
        self._compile_keyword()
        self._compile_subroutine_call()
        self._compile_symbol()
        # Discard return value from subroutine.
        # We use do statements only for their side effects.
        self.writer.write_pop("temp", 0)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        tk = self.tokenizer
        self._compile_keyword()
        if tk.current_token.value == ";":
            self.writer.write_return()
            self._compile_symbol()
            return
        self.compile_expression()
        self.writer.write_return()
        self._compile_symbol()

    def compile_expression(self) -> None:
        """Compiles an expression."""
        tk = self.tokenizer
        self.compile_term()
        while (operator := tk.current_token.value) in OPERATORS:
            self._compile_symbol()
            self.compile_term()
            self.writer.write_arithmetic(operator)

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
                self._compile_array()
            # Subroutine call
            elif next in (".", "("):
                self._compile_subroutine_call()
            # Variable
            else:
                identifier = self._compile_identifier()
                kind, index, _ = self._lookup_identifier(identifier)
                self.writer.write_push(kind, index)
        elif tk.current_token.value == "(":
            self._compile_symbol()
            self.compile_expression()
            self._compile_symbol()
        elif (operator := tk.current_token.value) in UNARY_OPERATORS:
            self._compile_symbol()
            self.compile_term()
            self.writer.write_arithmetic(operator, True)
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
