import constants


class Writer:

    segment_map = {
        "local": "R1",
        "argument": "R2",
        "this": "R3",
        "that": "R4",
        "pointer": ("R3", "R4"),
        "temp": ("R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12"),
    }

    def __init__(self, file_name) -> None:
        self.file_name = file_name.stem
        self.file = open(file_name, "w")
        self._count = 0

    def _get_base_address(self, segment):
        return self.segment_map[segment]

    @property
    def count(self):
        return self._count

    def _inc_count(self):
        self._count += 1

    def close(self):
        self.file.close()

    def _fetch_two_and_operate(self, operation):
        self.file.write(
            f"""@R0
AM=M-1
D=M
@R0
A=M-1
M=M{operation}D\n"""
        )

    def _fetch_one_and_operate(self, operation):
        self.file.write(
            f"""@R0
A=M-1
M={operation}M\n"""
        )

    def _write_add(self):
        self._fetch_two_and_operate("+")

    def _write_sub(self):
        self._fetch_two_and_operate("-")

    def _write_neg(self):
        self._fetch_one_and_operate("-")

    def _write_eq(self):
        self._write_conditional("JEQ")

    def _write_not(self):
        self._fetch_one_and_operate("!")

    def _write_or(self):
        self._fetch_two_and_operate("|")

    def _write_and(self):
        self._fetch_two_and_operate("&")

    def _write_conditional(self, condition):
        self.file.write(
            f"""@R0
AM=M-1
D=M
@R0
A=M-1
D=M-D
@TRUE{self.count}
D;{condition}
D=0
@SET{self.count}
0;JMP
(TRUE{self.count})
D=-1
(SET{self.count})
@R0
A=M-1
M=D\n"""
        )
        self._inc_count()

    def _write_lt(self):
        self._write_conditional("JLT")

    def _write_gt(self):
        self._write_conditional("JGT")

    def write_arithmetic(self, command):
        self.file.write(f"// {command} \n")
        if command == constants.C_ADD:
            self._write_add()
        elif command == constants.C_SUB:
            self._write_sub()
        elif command == constants.C_EQ:
            self._write_eq()
        elif command == constants.C_NEG:
            self._write_neg()
        elif command == constants.C_NOT:
            self._write_not()
        elif command == constants.C_OR:
            self._write_or()
        elif command == constants.C_AND:
            self._write_and()
        elif command == constants.C_LT:
            self._write_lt()
        elif command == constants.C_GT:
            self._write_gt()
        else:
            pass

    def write_push_pop(self, command, segment, index):
        self.file.write(f"//{command} {segment} {index}\n")
        if command == constants.C_PUSH:
            self._write_push(segment, int(index))
        else:
            self._write_pop(segment, int(index))

    def _write_push_static(self, index):
        self.file.write(
            f"""@{self.file_name}.{index}
D=M
@R0
A=M
M=D
@R0
M=M+1\n"""
        )

    def _write_push_constant(self, index):
        self.file.write(
            f"""@{index}
D=A
@R0
A=M
M=D
@R0
M=M+1\n"""
        )

    def _write_push_temp(self, index):
        self.file.write(
            f"""@{self._get_base_address('temp')[index]}
D=M
@R0
A=M
M=D
@R0
M=M+1\n"""
        )

    def _write_push_pointer(self, index):
        self.file.write(
            f"""@{self._get_base_address('pointer')[index]}
D=M
@R0
A=M
M=D
@R0
M=M+1\n"""
        )

    def _write_push_segment(self, segment, index):
        self.file.write(
            f"""@{index}
D=A
@{self._get_base_address(segment)}
A=M+D
D=M
@R0
A=M
M=D
@R0
M=M+1\n"""
        )

    def _write_push(self, segment, index):
        if segment == "static":
            self._write_push_static(index)
        elif segment == "constant":
            self._write_push_constant(index)
        elif segment == "temp":
            self._write_push_temp(index)
        elif segment == "pointer":
            self._write_push_pointer(index)
        else:
            self._write_push_segment(segment, index)

    def _write_pop_static(self, index):
        self.file.write(
            f"""@R0
AM=M-1
D=M
@{self.file_name}.{index}
M=D\n"""
        )

    def _write_pop_temp(self, index):
        self.file.write(
            f"""@R0
AM=M-1
D=M
@{self._get_base_address('temp')[index]}
M=D\n"""
        )

    def _write_pop_pointer(self, index):
        self.file.write(
            f"""@R0
AM=M-1
D=M
@{self._get_base_address('pointer')[index]}
M=D\n"""
        )

    def _write_pop_segment(self, segment, index):
        self.file.write(
            f"""@{self._get_base_address(segment)}
D=M
@{index}
D=A+D
@R13
M=D
@R0
AM=M-1
D=M
@R13
A=M
M=D\n"""
        )

    def _write_pop(self, segment, index):
        if segment == "static":
            self._write_pop_static(index)
        elif segment == "temp":
            self._write_pop_temp(index)
        elif segment == "pointer":
            self._write_pop_pointer(index)
        else:
            self._write_pop_segment(segment, index)

    def _write_loop(self):
        self.file.write(
            """(LOOP)
@LOOP
0;JMP"""
        )
