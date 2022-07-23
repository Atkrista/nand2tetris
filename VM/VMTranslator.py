import sys
import constants
from parser import Parser
from code_writer import Writer

class VmTranslator:
    def __init__(self, parser, writer) -> None:
       self.parser = parser
       self.writer = writer

    def translate_file(self):
        while self.parser.has_more_lines():
            self.parser.advance()
            if self.parser.command_type() == constants.C_ARITHMETIC:
                self.writer.write_arithmetic(self.parser.arg1())
            elif self.parser.command_type() == constants.C_PUSH or self.parser.command_type() == constants.C_POP:
                self.writer.write_push_pop(self.parser.command_type(), self.parser.arg1(), self.parser.arg2())
        self.writer._write_loop()
        self.writer.close()


if __name__ == "__main__":
    file_name = sys.argv[1]
    output_filename = file_name.split(".")[0] + ".asm"
    translator = VmTranslator(Parser(file_name), Writer(output_filename))
    translator.translate_file()
