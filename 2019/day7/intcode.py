opcode_param_count = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    99: 0
}

class IntCodeProgram:
    def __init__(self, memory: list[int]) -> None:
        self.cursor = 0
        self.memory = memory
        self.start_memory = memory.copy()
        self.inputs = []

    def get_num(self, param, mode):
        if mode == 0:
            return self.memory[param]
        elif mode == 1:
            return param

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
            param_modes = [
                int(mode) for mode in reversed(str(self.memory[self.cursor] // 100).zfill(len(params)))
            ]

            cursor_changed = False
            match opcode:
                case 1:
                    self.memory[params[2]] = self.get_num(params[0], param_modes[0]) \
                                             + self.get_num(params[1], param_modes[1])
                case 2:
                    self.memory[params[2]] = self.get_num(params[0], param_modes[0]) \
                                             * self.get_num(params[1], param_modes[1])
                case 3:
                    self.memory[params[0]] = self.inputs[0]
                    self.inputs = self.inputs[1:]
                case 4:
                    self.cursor += 2
                    return self.get_num(params[0], param_modes[0])
                case 5:
                    if self.get_num(params[0], param_modes[0]) != 0:
                        self.cursor = self.get_num(params[1], param_modes[1])
                        cursor_changed = True
                case 6:
                    if self.get_num(params[0], param_modes[0]) == 0:
                        self.cursor = self.get_num(params[1], param_modes[1])
                        cursor_changed = True
                case 7:
                    if self.get_num(params[0], param_modes[0]) < self.get_num(params[1], param_modes[1]):
                        self.memory[params[2]] = 1
                    else:
                        self.memory[params[2]] = 0
                case 8:
                    if self.get_num(params[0], param_modes[0]) == self.get_num(params[1], param_modes[1]):
                        self.memory[params[2]] = 1
                    else:
                        self.memory[params[2]] = 0
                case 99:
                    break
            if not cursor_changed:
                self.cursor += len(params) + 1