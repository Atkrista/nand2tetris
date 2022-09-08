from constants import OPERATOR_COMMAND_MAP, UNARY_OPERATOR_COMMAND_MAP


class VMWriter:
    def __init__(self, out) -> None:
        self.out = out

    def _write_line(self, string):
        self.out.write(string + "\n")

    def write_push(self, segment, index) -> None:
        """Writes a VM push command."""
        self._write_line(f"push {segment} {index}")

    def write_pop(self, segment, index) -> None:
        """Writes a VM pop command."""
        self._write_line(f"pop {segment} {index}")

    def write_arithmetic(self, command, unary=False) -> None:
        """Writes a VM arithmetic-logical command."""
        if unary:
            self._write_line(UNARY_OPERATOR_COMMAND_MAP[command])
        else:
            self._write_line(OPERATOR_COMMAND_MAP[command])

    def write_label(self, label) -> None:
        """Writes a VM label command."""
        self._write_line(f"label {label}")

    def write_goto(self, label) -> None:
        """Writes a VM goto command."""
        self._write_line(f"goto {label}")

    def write_if(self, label) -> None:
        """Writes a VM if-goto command."""
        self._write_line(f"if-goto {label}")

    def write_call(self, name, n_args) -> None:
        """Writes a VM call command."""
        self._write_line(f"call {name} {n_args}")

    def write_function(self, name, n_vars) -> None:
        """Writes a VM function command."""
        self._write_line(f"function {name} {n_vars}")

    def write_return(self) -> None:
        """Writes a VM return command."""
        self._write_line("return")

    def close(self):
        """Closes the output file/stream."""
        pass
