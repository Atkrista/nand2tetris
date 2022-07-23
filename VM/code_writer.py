import constants


class Writer:
    def __init__(self, file_name) -> None:
        self.file = open(file_name, "w")

    def close(self):
        self.file.close()

    def _write_add(self):
        self.file.writelines("@0\nA=M\n")

    def _fetch_two_and_operate(self, operation):
        # Fetch SP
        self.file.write("@0\nA=M\n")
        # fetch first operand to D
        self.file.write("A=A-1\nD=M\n")
        # point M to second operand
        self.file.write("A=A-1\n")
        # Write correct operation
        self.file.write(f"M=M{operation}D\n")
        # Set SP properly
        self.file.write("@0\nM=M-1\n")

    def _fetch_one_and_operate(self, operation):
        # Fetch SP
        self.file.write("@0\nA=M\n")
        # fetch first operand to D
        self.file.write("A=A-1\nD=M\n")
        # Write correct operation
        self.file.write(f"M={operation}M\n")
        # SP doesn't change here

    def _write_sub(self):
        self._fetch_two_and_operate("-")

    def _write_neg(self):
        self._fetch_one_and_operate("-")

    def _write_eq(self):
        self._fetch_two_and_operate("=")

    def _write_not(self):
        self._fetch_one_and_operate("!")

    def _write_or(self):
        self._fetch_two_and_operate("|")

    def _write_and(self):
        self._fetch_two_and_operate("&")

    def _write_conditional(self, condition):
        self.file.write(
            f"""@0
D=M
// Compute final value of SP right now
@R13
M=D
M=M-1
@0
A=M
A=A-1
D=M
A=A-1
D=M-D
D;{condition}
(TRUE)
@R13
M=-1
@END
0;JMP
(FALSE)
@R13
M=0
(END)
D=A
@0
M=D\n"""
        )

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
        self.file.write(f"// {command} {segment} {index}\n")
        pass

    def _write_loop(self):
        pass
