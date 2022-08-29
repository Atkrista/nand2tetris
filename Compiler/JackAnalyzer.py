import sys
import os
from constants import TokenType
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


class JackAnalyzer:
    def __init__(self) -> None:
        pass

    def out_file(self, infile):
        """Name of the xml file to write into."""
        print(infile[:-5] + "T.xml")
        return infile[:-5] + "T.xml"

    def is_jack_file(self, input):
        """Checks if `name` is a jack file i.e `file_name.jack` ."""
        return os.path.splitext(input)[1] == ".jack"

    def compile_file(self, file_name) -> None:
        with open(file_name, "r") as infile, open(
            self.out_file(file_name), "w"
        ) as outfile:
            tokenizer = JackTokenizer(infile)
            token = ""
            tag = ""
            while tokenizer.has_more_tokens():
                if tokenizer.token_type() == TokenType.KEYWORD:
                    token = tokenizer.key_word()
                    tag = TokenType.KEYWORD.value
                elif tokenizer.token_type() == TokenType.SYMBOL:
                    token = tokenizer.symbol()
                    tag = TokenType.SYMBOL.value
                elif tokenizer.token_type() == TokenType.IDENTIFIER:
                    token = tokenizer.identifier()
                    tag = TokenType.IDENTIFIER.value
                elif tokenizer.token_type() == TokenType.INT_CONST:
                    token = tokenizer.int_val()
                    tag = TokenType.INT_CONST.value
                elif tokenizer.token_type() == TokenType.STRING_CONST:
                    token = tokenizer.string_val()
                    tag = TokenType.STRING_CONST.value
                outfile.write(f"<{tag}>{token}</{tag}>\n")
                tokenizer.advance()

    def compile_dir(self, dir_name) -> None:
        for file_name in os.listdir(dir_name):
            self.compile_file(file_name)

    def compile(self, input) -> None:
        if self.is_jack_file(input):
            self.compile_file(input)
        else:
            self.compile_dir(input)


if __name__ == "__main__":
    arg1 = sys.argv[1]
    JackAnalyzer().compile(arg1)
