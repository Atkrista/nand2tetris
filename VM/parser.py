import constants


class Parser:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.file = open(self.file_name, "r")
        self.lines = self.file.read().splitlines()
        self.lines = self._clean(self.lines)
        self.current_command = []

    def __del__(self) -> None:
        self.file.close()

    def __repr__(self):
        return f"<Parser {self.file_name}>"

    def _clean(self, lines):
        # Remove comments and newlines
        return [line for line in lines if not line.startswith("//") and line]

    def has_more_lines(self) -> bool:
        return len(self.lines) != 0

    def advance(self) -> None:
        self.current_command = self.lines.pop(0).split()

    def command_type(self):
        return constants.COMMAND_TYPE_MAP[self.current_command[0]]

    def arg1(self):
        if self.command_type() == constants.TYPE_ARITHMETIC:
            return self.current_command[0]
        else:
            return self.current_command[1]

    def arg2(self):
        return self.current_command[2]
