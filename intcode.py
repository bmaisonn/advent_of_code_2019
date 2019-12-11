class UnknownOpCode(Exception):
    pass

class HaltExecution(Exception):
    pass

class MissingInput(Exception):
    pass

class InvalidParameterMode(Exception):
    pass

class IntCode:
    """
    Interpret the program given in constructor
    """
    def __init__(self, program_path, program_inputs, program_outputs):
        with open(program_path) as f:
            self.program = [int(x) for x in f.read().split(',') if x]
            self.program_size = len(self.program)
        self.program_inputs = program_inputs
        self.program_outputs = program_outputs
        self.curr_pos = 0
        self.relative_base = 0

    def store_value(self, pos, v):
        len(self.program)
        if pos >= len(self.program):
            missing_nb_elements = pos - len(self.program) + 1
            self.program.extend([None]*missing_nb_elements)
        self.program[pos] = v

    def read_input(self):
        """
        Read value from the input
        """
        if not self.program_inputs:
            raise MissingInput()
        return self.program_inputs.pop(0)

    def output(self, v):
        """
        outputs the value
        """
        return self.program_outputs.append(v)

    @classmethod
    def parameter_mode(cls, instruction, nth):
        # parameter modes
        # 0 position mode (default)
        # 1 immediate mode
        # 2 relative mode
        try:
            return int(instruction[-(2+nth)])
        except IndexError:
            return 0

    def expected_idx(self, parameter_mode, nth):
        if parameter_mode == 0:
            return self.program[self.curr_pos+nth]
        elif parameter_mode == 1:
            return self.curr_pos+nth
        elif parameter_mode == 2:
            return self.program[self.curr_pos+nth] + self.relative_base
        else:
            raise InvalidParameterMode(f'Parameter mode {parameter_mode} doesn\'t exist')

    def read_parameter(self, instruction, nth):
        """
        Read nth parameter based on the instruction
        parameter mode
        """
        curr_parameter_mode = IntCode.parameter_mode(instruction, nth)
        try:
            idx = self.expected_idx(curr_parameter_mode, nth)
            return self.program[idx]
        except IndexError:
            return 0 # any index error should return

    def process_opcode1(self, instruction):
        """
        Processes opcode1 
        1 1 2 4
        sum(prog[1],prog[2]) and save the result in
        prog[4]
        """
        v1 = self.read_parameter(instruction, 1)
        v2 = self.read_parameter(instruction, 2)
        res = v1 + v2  

        curr_parameter_mode = IntCode.parameter_mode(instruction, 3)
        idx = self.expected_idx(curr_parameter_mode, 3)
        self.store_value(idx, res)
        self.curr_pos += 4

    def process_opcode2(self, instruction):
        """
        Processes opcode1 
        1 1 2 4
        mul(prog[1],prog[2]) and save the result in
        prog[4]
        """
        v1 = self.read_parameter(instruction, 1)
        v2 = self.read_parameter(instruction, 2)
        res = v1 * v2  
        curr_parameter_mode = IntCode.parameter_mode(instruction, 3)
        idx = self.expected_idx(curr_parameter_mode, 3)
        self.store_value(idx, res)
        self.curr_pos += 4

    def process_opcode3(self, instruction):
        """
        Opcode 3 takes a single integer 
        as input and saves it to the position given by its only parameter.
        For example, the instruction 3,50 would take an 
        input value and store it at address 50.
        """
        program_input = self.read_input()

        curr_parameter_mode = IntCode.parameter_mode(instruction, 1)
        idx = self.expected_idx(curr_parameter_mode, 1)
        self.store_value(idx, program_input)

        self.curr_pos += 2

    def process_opcode4(self, instruction):
        """
        Opcode 4 outputs the value of its only parameter. 
        For example, the instruction 4,50 would output the 
        value at address 50
        """
        v1 = self.read_parameter(instruction, 1)
        self.output(v1)
        self.curr_pos += 2

    def process_opcode5(self, instruction):
        """
        Opcode 5 is jump-if-true: if the first parameter is non-zero, 
        it sets the instruction pointer to the value from the second parameter. 
        Otherwise, it does nothing.
        """
        v1 = self.read_parameter(instruction, 1)
        v2 = self.read_parameter(instruction, 2)
        if v1 != 0:
            self.curr_pos = v2
        else:
            self.curr_pos += 3

    def process_opcode6(self, instruction):
        """
        Opcode 6 is jump-if-false: if the first parameter is zero, 
        it sets the instruction pointer to the value from the second parameter. 
        Otherwise, it does nothing.
        """
        v1 = self.read_parameter(instruction, 1)
        v2 = self.read_parameter(instruction, 2)
        if v1 == 0:
            self.curr_pos = v2
        else:
            self.curr_pos += 3

    def process_opcode7(self, instruction):
        """
        Opcode 7 is less than: if the first parameter is less than the second parameter, 
        it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        """
        v1 = self.read_parameter(instruction, 1)
        v2 = self.read_parameter(instruction, 2)
        
        curr_parameter_mode = IntCode.parameter_mode(instruction, 3)
        idx = self.expected_idx(curr_parameter_mode, 3)
        self.store_value(idx, 1 if v1 < v2 else 0)
        self.curr_pos += 4

    def process_opcode8(self, instruction):
        """
        Opcode 8 is equals: if the first parameter is equal to the second parameter, 
        it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        """
        v1 = self.read_parameter(instruction, 1)
        v2 = self.read_parameter(instruction, 2)
        curr_parameter_mode = IntCode.parameter_mode(instruction, 3)
        idx = self.expected_idx(curr_parameter_mode, 3)
        self.store_value(idx, 1 if v1 == v2 else 0)
        self.curr_pos += 4

    def process_opcode9(self, instruction):
        """"
        Opcode 9 adjusts the relative base by the value of its only parameter.
        The relative base increases (or decreases, if the value is negative) 
        by the value of the parameter.
        """
        v1 = self.read_parameter(instruction, 1)
        self.relative_base += v1
        self.curr_pos += 2

    def process_opcode99(self, instruction):
        """
        Halt the program
        raise HaltExecution exception
        """
        raise HaltExecution()

    def process_instruction(self, instruction):
        opcode = int(instruction[-2:])

        # all method are formatted as "process_opcode1"
        # so we can generate method calls instead of using
        # a big switch
        method_name = f"process_opcode{opcode}"
        obj_method = getattr(self, method_name)
        obj_method(instruction)

    def run(self):
        """
        Starting from position 0 run the program
        """
        while self.curr_pos < self.program_size:
            instruction = str(self.program[self.curr_pos])
            try:
                self.process_instruction(instruction)
            except HaltExecution:
                break

if __name__ == '__main__':
    program_path = '/mnt/c/temp/perso/advent_of_code/input.txt'

    outputs = []
    intcode_program = IntCode(program_path, [2], outputs)
    intcode_program.run()
    print(outputs)