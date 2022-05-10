import os
import sys

with open(os.path.join(sys.path[0], "day5.txt")) as f:
    puzzle_input = f.read()

opcode_param_count = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    99: 0
}

class IntCodeProgram:
    def __init__(self, memory) -> None:
        self.cursor = 0
        self.memory = memory

    def get_num(self, param, mode):
        if mode == 0:
            return self.memory[param]
        elif mode == 1:
            return param

    def run(self, input):
        outputs = []
        while True:
            opcode = self.memory[self.cursor] % 100
            params = self.memory[self.cursor + 1 : self.cursor + 1 + opcode_param_count[opcode]]
            param_modes = [
                int(mode) for mode in reversed(str(self.memory[self.cursor] // 100).zfill(len(params)))
            ]

            self.cursor += len(params) + 1
            match opcode:
                case 1:
                    self.memory[params[2]] = self.get_num(params[0], param_modes[0]) \
                                             + self.get_num(params[1], param_modes[1])
                case 2:
                    self.memory[params[2]] = self.get_num(params[0], param_modes[0]) \
                                             * self.get_num(params[1], param_modes[1])
                case 3:
                    self.memory[params[0]] = input
                case 4:
                    outputs.append(self.get_num(params[0], param_modes[0]))
                case 99:
                    break
        return outputs

numbers = [int(x) for x in puzzle_input.split(",")]

program = IntCodeProgram(numbers)
print(program.run(1))