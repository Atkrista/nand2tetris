import sys
import constants
from code_writer import Writer
from parser import Parser
from os import listdir
from os.path import isfile


class VmTranslator:
    def __init__(self, parsers, writer) -> None:
        self.parsers = parsers
        self.writer = writer

    def translate(self):
        for parser in self.parsers:
            while parser.has_more_lines():
                parser.advance()
                if parser.command_type() == constants.C_ARITHMETIC:
                    self.writer.write_arithmetic(parser.arg1())
                elif (
                    parser.command_type() == constants.C_PUSH
                    or parser.command_type() == constants.C_POP
                ):
                    self.writer.write_push_pop(
                        parser.command_type(), parser.arg1(), parser.arg2()
                    )
        self.writer._write_loop()
        self.writer.close()


if __name__ == "__main__":
    input_path = sys.argv[1]
    is_dir = not isfile(input_path)
    parsers = []
    output = None
    # input_path = Path(sys.argv[1])
    if is_dir:
        parsers.extend([Parser(f) for f in listdir(input_path) if f.endswith(".vm")])
        output = input_path + ".asm"
    else:
        parsers.append(Parser(input_path))
        output = input_path[:-3] + ".asm"
    translator = VmTranslator(parsers, Writer(output, is_dir))
    translator.translate()
