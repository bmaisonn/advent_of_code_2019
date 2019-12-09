class UnknownOpCode(Exception):
    pass

class HaltExecution(Exception):
    pass

class MissingInput(Exception):
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
        try:
            return int(instruction[-(2+nth)])
        except IndexError:
            return 0

    def read_parameter(self, instruction, nth):
        """
        Read nth parameter based on the instruction
        parameter mode
        """
        curr_parameter_mode = IntCode.parameter_mode(instruction, nth)
        if curr_parameter_mode == 0:
            return self.program[self.program[self.curr_pos+nth]]
        else:
            return self.program[self.curr_pos+nth]


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
        self.store_value(self.program[self.curr_pos+3], res)
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
        self.store_value(self.program[self.curr_pos+3], res)
        self.curr_pos += 4

    def process_opcode3(self, instruction):
        """
        Opcode 3 takes a single integer 
        as input and saves it to the position given by its only parameter.
        For example, the instruction 3,50 would take an 
        input value and store it at address 50.
        """
        program_input = self.read_input()
        self.store_value(self.program[self.curr_pos+1], program_input)
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
        self.store_value(self.program[self.curr_pos+3], 1 if v1 < v2 else 0)
        self.curr_pos += 4

    def process_opcode8(self, instruction):
        """
        Opcode 8 is equals: if the first parameter is equal to the second parameter, 
        it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        """
        v1 = self.read_parameter(instruction, 1)
        v2 = self.read_parameter(instruction, 2)
        self.store_value(self.program[self.curr_pos+3], 1 if v1 == v2 else 0)
        self.curr_pos += 4

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

def generate_5uple():
    return ((i,j,k,l,m) for i in range(5,10)\
                        for j in range(5,10) if j != i\
                        for k in range(5,10) if k not in (i,j)\
                        for l in range(5,10) if l not in (i,j,k)\
                        for m in range(5,10) if m not in (i,j,k,l))

if __name__ == '__main__':
    max_result = None
    program_path = '/mnt/c/Users/Bertrand/Documents/advent/input4_intcode_program_day7.txt'


    for (i,j,k,l,m) in generate_5uple():
        program_inputs = [0]
        program_outputs = []
        programs = {x:IntCode(program_path, program_inputs, program_outputs) for x in ('A','B','C','D','E')}

        if (i,j,k,l,m) == (9,8,7,6,5):
            print("toto")

        last_E_output = None
        initialized = {x:False for x in programs.keys()}

        while program_inputs:
            for amp, new_input in zip(programs.keys(),(i,j,k,l,m)):
                if not initialized[amp]:
                    program_inputs.insert(0, new_input)
                    initialized[amp] = True
                if not program_inputs:
                    break
                try:
                    programs[amp].run()
                except MissingInput:
                    pass
                
                if amp == 'E' and program_outputs:
                    last_E_output = program_outputs[0]
                program_inputs.clear()
                program_inputs.extend(program_outputs)
                program_outputs.clear()

        thurster_value = last_E_output

        if not max_result or thurster_value > max_result:
            max_result = thurster_value

    print(max_result)