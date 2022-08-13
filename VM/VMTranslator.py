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
            self.writer.set_file_name(parser.file_name.split("/")[-1][:-3])
            while parser.has_more_lines():
                parser.advance()
                command_type = parser.command_type()
                if command_type == constants.TYPE_ARITHMETIC:
                    self.writer.write_arithmetic(parser.arg1())
                elif command_type in constants.get_push_pop_types():
                    self.writer.write_push_pop(
                        command_type, parser.arg1(), parser.arg2()
                    )
                elif command_type in constants.get_branching_types():
                    self.writer.write_branching(command_type, parser.arg1())
                elif command_type in constants.get_function_types():
                    self.writer.write_function(
                        command_type, parser.arg1(), parser.arg2()
                    )
                elif command_type == constants.TYPE_RETURN:
                    self.writer.write_function(command_type, None, None)
        self.writer._write_loop()
        self.writer.close()


if __name__ == "__main__":
    input_path = sys.argv[1]
    is_dir = not isfile(input_path)
    parsers = []
    output = None
    if is_dir:
        dir_name = input_path.split("/")[-1]
        parsers.extend(
            [
                Parser(input_path + "/" + f)
                for f in listdir(input_path)
                if f.endswith(".vm")
            ]
        )
        output = input_path + "/" + dir_name + ".asm"
    else:
        parsers.append(Parser(input_path))
        output = input_path[:-3] + ".asm"
    translator = VmTranslator(parsers, Writer(output, is_dir))
    translator.translate()
