import sys
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


class JackCompiler:
    def __init__(self) -> None:
        pass

    def out_file(self, infile):
        """Name of the xml file to write into."""
        return infile[:-5] + ".vm"

    def is_jack_file(self, input):
        """Checks if `name` is a jack file i.e `file_name.jack` ."""
        # return input.endswith(".jack")
        return os.path.splitext(input)[1] == ".jack"

    def compile_file(self, file_name) -> None:
        with open(file_name, "r") as infile, open(
            self.out_file(file_name), "w"
        ) as outfile:
            tokenizer = JackTokenizer(infile)
            engine = CompilationEngine(tokenizer, outfile)
            engine.compile_class()

    def compile_dir(self, dir_name) -> None:
        jack_files = list(filter(lambda f: f.endswith(".jack"), os.listdir(dir_name)))
        for f in jack_files:
            self.compile_file(dir_name + "/" + f)

    def compile(self, input) -> None:
        if self.is_jack_file(input):
            self.compile_file(input)
        else:
            self.compile_dir(input)


if __name__ == "__main__":
    arg1 = sys.argv[1]
    JackCompiler().compile(arg1)
