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

    def __init__(self, file_name, is_dir=False) -> None:
        if is_dir:
            self.file_name = file_name.split("/")[-1]
        else:
            self.file_name = file_name.split("/")[-1][:-3]
        self.file = open(file_name, "w")
        # _count is used to generate unique labels for conditionals
        self._count = 0
        self._ret_count = 0
        # The function translator is currently translating
        self._current_function = ""
        self._current_file_name = "GLOBAL"
        if is_dir:
            self._bootstrap_program()

    def close(self):
        self.file.close()

    def set_file_name(self, name):
        self._current_file_name = name

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
            raise ValueError("Invalid Command")

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

    def write_function(self, command_type, func_name, n):
        if n:
            n = int(n)
        self.file.write(
            f"//{constants.TYPE_COMMAND_MAP[command_type]} {func_name} {n}\n"
        )
        if command_type == constants.TYPE_FUNCTION:
            self._write_function(func_name, n)
        elif command_type == constants.TYPE_CALL:
            self._write_call(func_name, n)
        elif command_type == constants.TYPE_RETURN:
            self._write_return()
        else:
            pass

    @property
    def ret_count(self):
        self._ret_count += 1
        return self._ret_count

    @property
    def current_function(self):
        # Currently processing function
        return self._current_function

    @property
    def count(self):
        self._count += 1
        return self._count

    def _set_current_function(self, function):
        self._current_function = function

    def _bootstrap_program(self):
        self.file.write(
            f"""// Bootstrap Code
@256
D=A
@SP
M=D
"""
        )

        self.file.write(f"// Call Sys.init 0\n")
        self._write_call("Sys.init", 0)

    def _generate_label(self, label):
        return f"{self._current_file_name}.{self.current_function}${label}"

    def _generate_return_address(self):
        return f"{self._current_file_name}.{self.current_function}$ret.{self.ret_count}"

    def _get_base_address(self, segment):
        return self.segment_map[segment]

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
        count = self.count
        self.file.write(
            f"""@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@TRUE{count}
D;{condition}
D=0
@SET{count}
0;JMP
(TRUE{count})
D=-1
(SET{count})
@SP
A=M-1
M=D\n"""
        )

    def _write_lt(self):
        self._write_conditional("JLT")

    def _write_gt(self):
        self._write_conditional("JGT")

    def _write_push_static(self, index):
        self.file.write(
            f"""@{self._current_file_name}.{index}
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
            f"""@{self._get_base_address(segment)}
D=M
@{index}
A=A+D
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
@{self._current_file_name}.{index}
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
M=D
"""
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
        self.file.write(f"({self._generate_label(label)})\n")

    def _write_goto(self, label):
        self.file.write(
            f"""@{self._generate_label(label)}
0;JMP\n"""
        )

    def _write_if_goto(self, label):
        self.file.write(
            f"""@SP
AM=M-1
D=M
@{self._generate_label(label)}
D;JNE
"""
        )

    def _write_function(self, func_name, n_vars):
        self._set_current_function(func_name)
        self.file.write(f"({func_name})\n")
        # Need to init the local variables to zero
        for _ in range(n_vars):
            self.file.write(
                f"""@SP
A=M
M=0
@SP
M=M+1
"""
            )

    def _write_call(self, function_name, n_args):
        ret_addr = self._generate_return_address()
        # Generate and push the return address on the stack
        self.file.write(
            f"""@{ret_addr}
D=A
@SP
A=M
M=D
@SP
M=M+1
"""
        )

        # Save memory segments of caller
        for val in ("local", "argument", "this", "that"):
            self.file.write(
                f"""@{self._get_base_address(val)}
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
            )

        # Reposition the ARG segment for the callee
        self.file.write(
            f"""@SP
D=M
"""
        )

        for _ in range(5 + n_args):
            self.file.write(f"D=D-1\n")

        self.file.write(
            f"""@{self._get_base_address('argument')}
M=D
"""
        )

        # Reposition the Local segment
        self.file.write(
            f"""@SP
D=M
@{self._get_base_address('local')}
M=D
"""
        )

        # Only using function_name since (?) that fn names
        # are unique across diff. *.vm files
        self.file.write(
            f"""@{function_name}
0;JMP
"""
        )

        # Inject the return address directly into the code
        self.file.write(f"({ret_addr})\n")

    def _write_return(self):
        # Saves the pointer to local segment in R13
        self.file.write(
            f"""@{self._get_base_address('local')}
D=M
@R13
M=D
"""
        )
        # Saves the return address to R14
        for _ in range(5):
            self.file.write(f"D=D-1\n")

        self.file.write(
            f"""A=D
D=M
"""
        )

        self.file.write(
            f"""@R14
M=D
"""
        )

        # Repositions the return value for caller
        self.file.write(
            f"""@SP
A=M-1
D=M
@{self._get_base_address('argument')}
A=M
M=D
"""
        )

        # Repositions SP for caller
        self.file.write(
            f"""@{self._get_base_address('argument')}
D=M
@SP
M=D+1
"""
        )

        # Restores THAT, THIS, ARG, LCL for caller
        for val in ("that", "this", "argument", "local"):
            self.file.write(
                f"""@R13
AM=M-1
D=M
@{self._get_base_address(val)}
M=D
"""
            )

        # GOTO return address
        self.file.write(
            f"""@R14
A=M
0;JMP
"""
        )
