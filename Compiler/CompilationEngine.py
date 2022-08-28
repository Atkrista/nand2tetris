class CompilationEngine:
    def __init__(self, input, output) -> None:
        """Creates a new compilation engine with the given input and output.
        The next routine called by the JackAnalyzer module must be compile_class."""
        pass

    def compile_class(self) -> None:
        """Compiles a complete class."""
        pass

    def compile_class_var_dec(self) -> None:
        """Compiles a static variable declaration, or a field declaration."""
        pass

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        pass

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list. Does not handle the closing
        parenthesis tokens `(` and `)` ."""
        pass

    def compile_subroutine_body(self) -> None:
        """Compiles a subroutine's body."""
        pass

    def compile_var_dec(self) -> None:
        """Compiles a `var` declaration."""
        pass

    def compile_statements(self) -> None:
        """Compiles a sequence of statements. Does not handle the enclosing curly
        braces, `{` and `}` ."""
        pass

    def compile_let(self) -> None:
        """Compiles  a let statement."""
        pass

    def compile_if(self) -> None:
        """Compiles an if statement possibly with a trailing `else` clause."""
        pass

    def compile_while(self) -> None:
        """Compiles a while statement."""
        pass

    def compile_do(self) -> None:
        """Compiles a do statement."""
        pass

    def compile_return(self) -> None:
        """Compiles a return statement."""
        pass

    def compile_expression(self) -> None:
        """Compiles an expression."""
        pass

    def compile_term(self) -> None:
        """Compiles a term. If the current token is an identifier, the routine
        must resolve it into a variable, an array element, or a subroutine call.
        A single lookahead token, which may be `[`, `(`, or `.` suffuces to distinguish
        between possibilities. Any other token is not part of this term and should not be
        advanced over."""
        pass

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma separated list of expressions. Returns the
        number of expressions in the list"""
        pass
