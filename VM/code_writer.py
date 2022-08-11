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

    _current_function = ""

    def __init__(self, file_name, is_dir=False) -> None:
        if is_dir:
            self.file_name = file_name.split("/")[-1]
        else:
            self.file_name = file_name.split("/")[-1][:-3]
        self.file = open(file_name, "w")
        self._count = 0
        self._ret_count = 0

    def set_file_name(self, name):
        self._current_file_name = name

    def _get_base_address(self, segment):
        return self.segment_map[segment]

    def _get_current_label(self, label):
        return f"{self._current_file_name + '.' + self._current_function + '$' + label}"

    @property
    def ret_count(self):
        self._ret_count += 1
        return self._ret_count

    @property
    def count(self):
        return self._count

    def _inc_count(self):
        self._count += 1

    def close(self):
        self.file.close()

    def _fetch_two_and_operate(self, operation):
        self.file.write(
            f"""@SP
AM=M-1
D=M
@SP
A=M-1
M=M{operation}D\n"""
        )

    def _fetch_one_and_operate(self, operation):
        self.file.write(
            f"""@SP
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
            f"""@SP
AM=M-1
D=M
@SP
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
@SP
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

    def write_push_pop(self, command_type, segment, index):
        self.file.write(
            f"//{constants.TYPE_COMMAND_MAP[command_type]} {segment} {index}\n"
        )
        if command_type == constants.TYPE_PUSH:
            self._write_push(segment, int(index))
        else:
            self._write_pop(segment, int(index))

    def write_branching(self, command_type, label):
        self.file.write(f"//{constants.TYPE_COMMAND_MAP[command_type]} {label}\n")
        if command_type == constants.TYPE_LABEL:
            self._write_label(label)
        elif command_type == constants.TYPE_GOTO:
            self._write_goto(label)
        else:
            self._write_if_goto(label)

    def _write_push_static(self, index):
        self.file.write(
            f"""@{self.file_name}.{index}
D=M
@SP
A=M
M=D
@SP
M=M+1\n"""
        )

    def _write_push_constant(self, index):
        self.file.write(
            f"""@{index}
D=A
@SP
A=M
M=D
@SP
M=M+1\n"""
        )

    def _write_push_temp(self, index):
        self.file.write(
            f"""@{self._get_base_address('temp')[index]}
D=M
@SP
A=M
M=D
@SP
M=M+1\n"""
        )

    def _write_push_pointer(self, index):
        self.file.write(
            f"""@{self._get_base_address('pointer')[index]}
D=M
@SP
A=M
M=D
@SP
M=M+1\n"""
        )

    def _write_push_segment(self, segment, index):
        self.file.write(
            f"""@{index}
D=A
@{self._get_base_address(segment)}
A=M+D
D=M
@SP
A=M
M=D
@SP
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
            f"""@SP
AM=M-1
D=M
@{self.file_name}.{index}
M=D\n"""
        )

    def _write_pop_temp(self, index):
        self.file.write(
            f"""@SP
AM=M-1
D=M
@{self._get_base_address('temp')[index]}
M=D\n"""
        )

    def _write_pop_pointer(self, index):
        self.file.write(
            f"""@SP
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
@SP
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
0;JMP\n"""
        )

    def _write_label(self, label):
        self.file.write(
            f"({self._current_file_name + '.' + self._current_function + '$' + label})\n"
        )

    def _write_goto(self, label):
        self.file.write(
            f"""@{self._current_file_name + '.' + self._current_function + '$' + label}
0;JMP\n"""
        )

    def _write_if_goto(self, label):
        self.file.write(
            f"""@SP
AM=M-1
D-M
@{label}
D;JNE
"""
        )

    def _write_function(self, func_name, n_vars):
        self._current_function = func_name
        self.file.write(
            f"""({self._current_file_name + '.' + func_name})
@{self._get_base_address('local')[0]}
A=M\n"""
        )
        for _ in range(n_vars):
            self.file.write(
                f"""M=0
A=A+1
"""
            )

    def _generate_return_address(self):
        return f"{self._current_file_name + '.' + self._current_function + '$' + 'ret' + self._ret_count }"

    def _write_call(self, function_name, n_args):
        ret_addr = self._generate_return_address()
        self.file.write(f"({ret_addr})")
        for val in ("local", "arg", "this", "that"):
            self.file.write(
                f"""@{self._get_base_address(val)[0]}
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1
    """
            )
        self.file.write(
            f"""@SP
D=A
@{self._get_base_address('arg')}
"""
        )
        for _ in range(5 + n_args):
            self.file.write(f"M=D-1\n")

        self.file.write(
            f"""@{self._get_base_address('local')}
M=D
@{self._current_file_name + '.' + function_name}
0;JMP
"""
        )
        self.file.write(f"({ret_addr})\n")

    def _write_return(self):
        self.file.write(
            f"""@{self._get_base_address('local')[0]}
D=M
@R13
M=D
D=D-1
D=D-1
D=D-1
D=D-1
A=D-1
D=M
@R14
M=D
@SP
AM=M-1
D=M
@{self._get_base_address('arg')[0]}
A=M
M=D
@{self._get_base_address('arg')[0]}
D=M
@SP
M=D+1
@R13
A=M-1
D=M
@{self._get_base_address('that')[0]}
M=D
@R13
A=M-1
A=A-1
D=M
@{self._get_base_address('this')[0]}
M=D
@R13
A=M-1
A=A-1
A=A-1
D=M
@{self._get_base_address('arg')[0]}
M=D
@R13
A=M-1
A=A-1
A=A-1
A=A-1
D=M
@{self._get_base_address('local')[0]}
M=D
@R14
A=M
0;JMP
"""
        )
