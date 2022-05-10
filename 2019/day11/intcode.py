import os
import sys

opcode_param_count = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 1,
    99: 0
}

class IntCodeProgram:
    # memory can be a list of ints, which is the memory, or a string, which is a file with memory
    def __init__(self, memory: list[int] | str) -> None:
        if isinstance(memory, list):
            self.memory = memory
        if isinstance(memory, str):
            with open(os.path.join(sys.path[0], memory)) as f:
                self.memory = [int(x) for x in f.read().split(",")]

        self.start_memory = self.memory.copy()

        self.cursor = 0
        self.inputs = []
        self.relative_base = 0

    def write_num(self, param_mode, to_write):
        param, mode = param_mode
        match mode:
            case 0: # position mode
                if param >= len(self.memory):
                    for _ in range(param - len(self.memory) + 1):
                        self.memory.append(0)
                self.memory[param] = to_write
            case 1: # immediate mode
                raise Exception('Write was in 1')
            case 2: # relative mode
                if param + self.relative_base >= len(self.memory):
                    for _ in range(param + self.relative_base - len(self.memory) + 1):
                        self.memory.append(0)
                self.memory[param + self.relative_base] = to_write

    def read_num(self, param_mode):
        param, mode = param_mode
        match mode:
            case 0: # position mode
                if param >= len(self.memory):
                    return 0
                return self.memory[param]
            case 1: # immediate mode
                return param
            case 2: # relative mode
                if param + self.relative_base >= len(self.memory):
                    return 0
                return self.memory[param + self.relative_base]

    def run(self, inputs):
        outputs = []
        self.inputs = inputs

        while True:
            cur_output = self.get_one_output()
            if cur_output is None:
                break
            outputs.append(cur_output)

        self.reset()
        return outputs

    def reset(self):
        self.inputs = []
        self.memory = self.start_memory
        self.cursor = 0

    def add_input(self, input):
        self.inputs.append(input)

    def get_one_output(self):
        while True:
            opcode = self.memory[self.cursor] % 100
            params = self.memory[self.cursor + 1 : self.cursor + 1 + opcode_param_count[opcode]]
            modes = [
                int(mode) for mode in reversed(str(self.memory[self.cursor] // 100).zfill(len(params)))
            ]
            param_modes = list(zip(params, modes))

            cursor_changed = False
            match opcode:
                case 1: # add
                    left_num, right_num, destination = param_modes
                    self.write_num(destination, self.read_num(left_num) \
                                                + self.read_num(right_num))
                case 2: # multiply
                    left_num, right_num, destination = param_modes
                    self.write_num(destination, self.read_num(left_num) \
                                                * self.read_num(right_num))
                case 3: # input
                    destination, = param_modes
                    self.write_num(destination, self.inputs[0])
                    self.inputs = self.inputs[1:]
                case 4: # output
                    self.cursor += 2 # because we are returning, gotta do this now

                    to_return, = param_modes
                    return self.read_num(to_return)
                case 5: # jump-if-true
                    to_check, destination = param_modes
                    if self.read_num(to_check) != 0:
                        self.cursor = self.read_num(destination)
                        cursor_changed = True
                case 6: # jump-if-false
                    to_check, destination = param_modes
                    if self.read_num(to_check) == 0:
                        self.cursor = self.read_num(destination)
                        cursor_changed = True
                case 7: # less than
                    left_num, right_num, destination = param_modes
                    if self.read_num(left_num) < self.read_num(right_num):
                        self.write_num(destination, 1)
                    else:
                        self.write_num(destination, 0)
                case 8: # equals
                    left_num, right_num, destination = param_modes
                    if self.read_num(left_num) == self.read_num(right_num):
                        self.write_num(destination, 1)
                    else:
                        self.write_num(destination, 0)
                case 9: # change relative base offset
                    adjust_by, = param_modes
                    self.relative_base += self.read_num(adjust_by)
                case 99: # terminate
                    return None
            if not cursor_changed:
                self.cursor += len(params) + 1