from enum import Enum, auto
import os
import sys

opcode_param_count = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0}


class ExitCode(Enum):
    """Represents the status of a computer that has stopped running.

    HALTED: No issues, program is just paused.
    TERMINATE: The program is finished running.
    NEED_INPUT: The program needed to read an input and there were none."""

    HALTED = auto()
    TERMINATE = auto()
    NEED_INPUT = auto()


class IntCodeProgram:
    def __init__(self, memory: list[int] | str) -> None:
        """Creates an intcode computer with the program passed into memory.

        Memory can either be a list of ints, the memory of the program, or a string of a file with memory.
        """
        if isinstance(memory, list):
            self._memory = memory
        if isinstance(memory, str):
            with open(os.path.join(sys.path[0], memory)) as f:
                self._memory = [int(x) for x in f.read().split(",")]

        self._start_memory = self._memory.copy()

        self._cursor = 0
        self._inputs = []
        self._relative_base = 0

    def _write_num(self, param_mode: tuple[int, int], to_write: int) -> None:
        param, mode = param_mode
        match mode:
            case 0:  # position mode
                if param >= len(self._memory):
                    for _ in range(param - len(self._memory) + 1):
                        self._memory.append(0)
                self._memory[param] = to_write
            case 1:  # immediate mode
                raise Exception("Write was in 1")
            case 2:  # relative mode
                if param + self._relative_base >= len(self._memory):
                    for _ in range(param + self._relative_base - len(self._memory) + 1):
                        self._memory.append(0)
                self._memory[param + self._relative_base] = to_write

    def _read_num(self, param_mode: tuple[int, int]) -> int:
        param, mode = param_mode
        match mode:
            case 0:  # position mode
                if param >= len(self._memory):
                    return 0
                return self._memory[param]
            case 1:  # immediate mode
                return param
            case 2:  # relative mode
                if param + self._relative_base >= len(self._memory):
                    return 0
                return self._memory[param + self._relative_base]

    def run(self, inputs: list[int] = None) -> list[int]:
        """Runs the program with the given set of inputs.

        This is to be used when the program can be run from start to finish without
        issue, and all the inputs are known ahead of time. The program is reset
        after it has exited.

        Returns a list of the outputs of the program."""
        if inputs is None:
            inputs = []
        self._inputs = inputs

        outputs = []
        while True:
            cur_output, _ = self.get_one_output()
            if cur_output is None:
                break
            outputs.append(cur_output)

        self.reset()
        return outputs

    def set_mem(self, n, new_val) -> None:
        """Set the memory at value `n` to `new_val`."""
        self._memory[n] = new_val

    def get_n_outputs(self, n) -> tuple[list[int], ExitCode]:
        """Runs the program until n outputs have been produced or until the program exits.

        Returns the outputs produced and the exit code.

        If the program exits before n outputs have been produced, only those
        outputs will be returned."""
        outputs = []
        for _ in range(n):
            cur_output, exit_code = self.get_one_output()
            if cur_output is None:
                break
            outputs.append(cur_output)
        return outputs, exit_code

    def reset(self) -> None:
        """Resets the program to its initial state."""
        self._inputs = []
        self._memory = self._start_memory
        self._cursor = 0

    def add_input(self, input: int) -> None:
        """Adds an input to the program."""
        self._inputs.append(input)

    def get_one_output(self) -> tuple[int | None, ExitCode]:
        """Runs the program until an output has been produced or until the program exits.

        Returns the output produced and the exit code.

        If the program exits before an outputs have been produced, None is returned for the output."""
        while True:
            opcode = self._memory[self._cursor] % 100
            params = self._memory[
                self._cursor + 1 : self._cursor + 1 + opcode_param_count[opcode]
            ]
            modes = [
                int(mode)
                for mode in reversed(
                    str(self._memory[self._cursor] // 100).zfill(len(params))
                )
            ]
            param_modes = list(zip(params, modes))

            cursor_changed = False
            match opcode:
                case 1:  # add
                    left_num, right_num, destination = param_modes
                    self._write_num(
                        destination,
                        self._read_num(left_num) + self._read_num(right_num),
                    )
                case 2:  # multiply
                    left_num, right_num, destination = param_modes
                    self._write_num(
                        destination,
                        self._read_num(left_num) * self._read_num(right_num),
                    )
                case 3:  # input
                    (destination,) = param_modes
                    if len(self._inputs) == 0:
                        return None, ExitCode.NEED_INPUT
                    self._write_num(destination, self._inputs[0])
                    self._inputs = self._inputs[1:]
                case 4:  # output
                    self._cursor += 2  # because we are returning, gotta do this now

                    (to_return,) = param_modes
                    return self._read_num(to_return), ExitCode.HALTED
                case 5:  # jump-if-true
                    to_check, destination = param_modes
                    if self._read_num(to_check) != 0:
                        self._cursor = self._read_num(destination)
                        cursor_changed = True
                case 6:  # jump-if-false
                    to_check, destination = param_modes
                    if self._read_num(to_check) == 0:
                        self._cursor = self._read_num(destination)
                        cursor_changed = True
                case 7:  # less than
                    left_num, right_num, destination = param_modes
                    if self._read_num(left_num) < self._read_num(right_num):
                        self._write_num(destination, 1)
                    else:
                        self._write_num(destination, 0)
                case 8:  # equals
                    left_num, right_num, destination = param_modes
                    if self._read_num(left_num) == self._read_num(right_num):
                        self._write_num(destination, 1)
                    else:
                        self._write_num(destination, 0)
                case 9:  # change relative base offset
                    (adjust_by,) = param_modes
                    self._relative_base += self._read_num(adjust_by)
                case 99:  # terminate
                    return None, ExitCode.TERMINATE
            if not cursor_changed:
                self._cursor += len(params) + 1
