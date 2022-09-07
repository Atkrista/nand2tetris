class VMWriter:
    def __init__(self) -> None:
        pass

    def write_push(self, segment, index) -> None:
        """Writes a VM push command."""
        pass

    def write_pop(self, segment, index) -> None:
        """Writes a VM pop command."""
        pass

    def write_arithmetic(self, command) -> None:
        """Writes a VM arithmetic-logical command."""
        pass

    def write_label(self, label) -> None:
        """Writes a VM label command."""
        pass

    def write_goto(self, label) -> None:
        """Writes a VM goto command."""
        pass

    def write_if(self, label) -> None:
        """Writes a VM if-goto command."""
        pass

    def write_call(self, name, n_args) -> None:
        """Writes a VM call command."""
        pass

    def write_function(self, name, n_vars) -> None:
        """Writes a VM function command."""
        pass

    def write_return(self) -> None:
        """Writes a VM return command."""
        pass

    def close(self):
        """Closes the output file/stream."""
        pass
