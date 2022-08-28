import sys
import os
from Compiler.constants import TokenType
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


class JackAnalyzer:
    def __init__(self, input) -> None:
        self.input = input

    def out_file(self, infile):
        """Name of the xml file to write into."""
        return infile.split[:5] + "T.xml"

    def is_jack_file(self):
        """Checks if `name` is a jack file i.e file_name.jack ."""
        return self.input.split(".")[1] == "jack"

    def compile_file(self) -> None:
        with open(self.input, "r") as infile, open(
            self.out_file(self.input), "w"
        ) as outfile:
            tokenizer = JackTokenizer(infile)
            token = ""
            tag = ""
            while tokenizer.has_more_tokens():
                if tokenizer.token_type == TokenType.KEYWORD:
                    token = tokenizer.key_word()
                    tag = TokenType.KEYWORD.value
                elif tokenizer.token_type == TokenType.SYMBOL:
                    token = tokenizer.symbol()
                    tag = TokenType.SYMBOL.value
                elif tokenizer.token_type == TokenType.IDENTIFIER:
                    token = tokenizer.identifier()
                    tag = TokenType.IDENTIFIER.value
                elif tokenizer.token_type == TokenType.INT_CONST:
                    token = tokenizer.int_val()
                    tag = TokenType.INT_CONST.value
                elif tokenizer.token_type == TokenType.STRING_CONST:
                    token = tokenizer.string_val()
                    tag = TokenType.STRING_CONST.value
                outfile.write(f"<{tag}>{token}</{tag}>")
                tokenizer.advance()

    def compile_dir(self) -> None:
        pass

    def compile(self) -> None:
        if self.is_jack_file():
            self.compile_file()
        else:
            self.compile_dir()


if __name__ == "__main__":
    arg1 = sys.argv[1]
    JackAnalyzer(arg1).compile()
