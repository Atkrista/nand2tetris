from constants import TokenType, OPERATORS, KEYWORD_CONSTANTS, UNARY_OPERATORS


class CompilationEngine:
    def __init__(self, input, output) -> None:
        """Creates a new compilation engine with the given input and output.
        The next routine called by the JackAnalyzer module must be compile_class."""
        self.tokenizer = input
        self.outfile = output

    def _write_line(self, val):
        self.outfile.write(val + "\n")

    def _write_tags(self, tag, val):
        self._write_line(f"<{tag}>{val}</{tag}>")

    def _open_tag(self, tag):
        self._write_line(f"<{tag}>")

    def _close_tag(self, tag):
        self._write_line(f"</{tag}>")

    def _compile_symbol(self, done=False):
        tk = self.tokenizer
        self._write_tags("symbol", tk.symbol())
        if not done:
            tk.advance()

    def _compile_keyword(self):
        tk = self.tokenizer
        self._write_tags("keyword", tk.key_word())
        tk.advance()

    def _compile_identifier(self):
        tk = self.tokenizer
        self._write_tags("identifier", tk.identifier())
        tk.advance()

    def _compile_type(self) -> None:
        tk = self.tokenizer
        if tk.token_type == TokenType.KEYWORD:
            self._write_tags("keyword", tk.key_word())
        elif tk.token_type == TokenType.IDENTIFIER:
            self._write_tags("identifier", tk.identifier())
        tk.advance()

    def _compile_subroutine_call(self) -> None:
        tk = self.tokenizer
        self._compile_identifier()
        if tk.current_token.value == ".":
            self._compile_symbol()
            self._compile_identifier()
        self._compile_symbol()
        self.compile_expression_list()
        self._compile_symbol()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        tk = self.tokenizer
        tk.advance()
        self._write_line("<class>")
        self._compile_keyword()
        self._compile_identifier()
        self._compile_symbol()
        while tk.current_token.value in ("static", "field"):
            self.compile_class_var_dec()
        while tk.current_token.value in ("constructor", "function", "method"):
            self.compile_subroutine()
        self._compile_symbol(True)
        self._write_line("</class>")

    def compile_class_var_dec(self) -> None:
        """Compiles a static variable declaration, or a field declaration."""
        tk = self.tokenizer
        self._open_tag("classVarDec")
        self._compile_keyword()
        self._compile_type()
        self._compile_identifier()
        while tk.current_token.value != ";":
            self._compile_symbol()
            self._compile_identifier()
        self._compile_symbol()
        self._close_tag("classVarDec")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        tk = self.tokenizer
        self._open_tag("subRoutineDec")
        self._compile_keyword()
        if tk.current_token.value == "void":
            self._compile_keyword()
        else:
            self._compile_type()
        self._compile_identifier()
        self._compile_symbol()
        self.compile_parameter_list()
        self._compile_symbol()
        self.compile_subroutine_body()
        self._close_tag("subRoutineDec")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list. Does not handle the closing
        parenthesis tokens `(` and `)` ."""
        tk = self.tokenizer
        self._open_tag("parameterList")
        # Handle empty parameter list
        if tk.current_token.value == ")":
            self._close_tag("parameterList")
            return
        # Handle single parameter
        self._compile_type()
        self._compile_identifier()
        # Handle all other parameters
        while tk.current_token.value != ")":
            self._compile_symbol()
            self._compile_type()
            self._compile_identifier()
        self._close_tag("parameterList")

    def compile_subroutine_body(self) -> None:
        """Compiles a subroutine's body."""
        tk = self.tokenizer
        self._open_tag("subroutineDec")
        self._compile_symbol()
        while tk.current_token.value == "var":
            self.compile_var_dec()
        self.compile_statements()
        self._compile_symbol()
        self._close_tag("subroutineDec")

    def compile_var_dec(self) -> None:
        """Compiles a `var` declaration."""
        tk = self.tokenizer
        self._open_tag("varDec")
        self._compile_keyword()
        self._compile_type()
        self._compile_identifier()
        while tk.current_token.value != ";":
            self._compile_symbol()
            self._compile_identifier()
        self._compile_symbol()
        self._close_tag("varDec")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements. Does not handle the enclosing curly
        braces, `{` and `}` ."""
        tk = self.tokenizer
        while tk.current_token.value != "}":
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
        self._open_tag("letStatement")
        self._compile_keyword()
        self._compile_identifier()
        if tk.current_token.value == "[":
            self._compile_symbol()
            self.compile_expression()
            self._compile_symbol()
        self._compile_symbol()
        self.compile_expression()
        self._compile_symbol()
        self._close_tag("letStatement")

    def compile_if(self) -> None:
        """Compiles an if statement possibly with a trailing `else` clause."""
        tk = self.tokenizer
        self._open_tag("ifStatement")
        self._compile_keyword()
        self._compile_symbol()
        self.compile_expression()
        self._compile_symbol()
        self._compile_symbol()
        self.compile_statements()
        self._compile_symbol()
        if tk.current_token.value == "else":
            self._compile_keyword()
            self._compile_symbol()
            self.compile_statements
            self._compile_symbol()
        self._open_tag("ifStatement")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        tk = self.tokenizer
        self._open_tag("whileStatement")
        self._compile_keyword()
        self._compile_symbol()
        self.compile_expression()
        self._compile_symbol()
        self._compile_symbol()
        self.compile_statements()
        self._compile_symbol()
        self._close_tag("whileStatement")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        tk = self.tokenizer
        self._open_tag("doStatement")
        self._compile_keyword()
        self._compile_subroutine_call()
        self._compile_symbol()
        self._close_tag("doStatement")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        tk = self.tokenizer
        self._open_tag("returnStatement")
        self._compile_keyword()
        if tk.current_token.value == ";":
            self._compile_symbol
            return
        self.compile_expression
        self._compile_symbol()
        self._close_tag("returnStatement")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        tk = self.tokenizer
        self._open_tag("expression")
        self.compile_term()
        while tk._get_next_token().value in OPERATORS:
            self._compile_symbol()
            self.compile_term()
        self._close_tag("expression")

    def compile_term(self) -> None:
        """Compiles a term. If the current token is an identifier, the routine
        must resolve it into a variable, an array element, or a subroutine call.
        A single lookahead token, which may be `[`, `(`, or `.` suffices to distinguish
        between possibilities. Any other token is not part of this term and should not be
        advanced over."""
        tk = self.tokenizer
        self._open_tag("term")
        next = tk._get_next_token()
        if tk.token_type() == TokenType.STRING_CONST:
            self._write_tags("stringConstant", tk.string_val())
            tk.advance()
        elif tk.token_type() == TokenType.INT_CONST:
            self._write_tags("integerConstant", tk.int_val())
            tk.advance()
        elif tk.current_token.value in KEYWORD_CONSTANTS:
            self._write_tags("keywordConstant", tk.current_token.value)
            tk.advance()
        elif tk.token_type() == TokenType.IDENTIFIER:
            self._compile_identifier()
            if tk.current_token.value == "[":
                self._compile_symbol()
                self.compile_expression()
                self._compile_symbol()
        elif tk.current_token.value == "(":
            self._compile_symbol()
            self.compile_expression()
            self._compile_symbol()
        elif tk.current_value in UNARY_OPERATORS:
            self._compile_symbol()
            self.compile_term()
        else:
            self._compile_subroutine_call()

        self._close_tag("term")

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma separated list of expressions. Returns the
        number of expressions in the list"""
        count = 0
        tk = self.tokenizer
        self._open_tag("expressionList")
        if tk.current_token.value == ")":
            self._close_tag("expressionList")
            return count
        self.compile_expression()
        count += 1
        while tk.current_token.value != ")":
            self._compile_symbol()
            self.compile_expression()
            count += 1
        self._close_tag("expressionList")
        return count
