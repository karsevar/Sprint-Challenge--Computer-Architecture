"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # create the ram array that will have a total of 256 
        # spaces because of the structure of the cpu in the spec 
        self.ram = [0] * 256 

        # create a register array that will carry all variables 
        # that need to be executed for every opcode instruction 
        self.reg = [0] * 8 

        # stack pointer starts at index position 243 of the ram 
        # pointer saved in reg[7]

        # modify self.reg at position 7 to store the stack pointer 
        # within self.ram.
        self.reg[7] = 243

        # create a pc counter variable that will be initialized to
        # zero
        self.pc = 0

        # flag register 8 bit binary code where Less then is the bit in the 8th place, greater than 
        # is the bit in the 2nd place, and E is the bit in the 1s place.
        # initialized to a binary number of 0 
        self.FL = 0b00000000

        ## moving the run instruction logic to the constructor:
        # opicode designations of functionality currently built out.
        LDI = 0b10000010 # used to save a specific value into the register 
        PRN = 0b01000111 # used to print a specific value in the register 
        MUL = 0b10100010 # used to multply two values using the alu.
        POP = 0b01000110 # used to pop the value at the top of the stack
        PUSH = 0b01000101 # used to push the value at the top of the stack
        CALL = 0b01010000 # used to call subroutine at the address stored in the register
        RET = 0b00010001 # used to return from subroutine
        ADD = 0b10100000
        CMP = 0b10100111 # used to compare two registers (used for greater than, less than, 
        # or equal to operations)
        JEQ = 0b01010101 # used to jump to an address if the E in the flag register is true 
        JNE = 0b01010110 # used to jump to an address if the E in the flag register is not true
        JMP = 0b01010100 # used to jump to the address specified by the input register


        # initialize the instruction_branch dictionary that will hold all the 
        # opcode functions indexed by the specific opcode.
        self.instruction_table = {}

        # place the helper methods into the instruction_table using the opcode 
        # variable values as the keys.
        self.instruction_table[LDI] = self.handle_LDI
        self.instruction_table[PRN] = self.handle_PRN
        self.instruction_table[MUL] = self.handle_MUL
        self.instruction_table[POP] = self.handle_pop
        self.instruction_table[PUSH] = self.handle_push
        self.instruction_table[CALL] = self.handle_CALL 
        self.instruction_table[RET] = self.handle_RET
        self.instruction_table[ADD] = self.handle_ADD
        self.instruction_table[CMP] = self.handle_CMP
        self.instruction_table[JEQ] = self.handle_JEQ
        self.instruction_table[JMP] = self.handle_JMP
        self.instruction_table[JNE] = self.handle_JNE

    def handle_JNE(self):
        flag_command = self.FL & 0b00000001

        if flag_command == 0b00000000:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            self.pc += 2

    def handle_JMP(self):
        self.pc = self.reg[self.ram[self.pc + 1]]

    def handle_JEQ(self):
        # print('Flag value', self.FL == 0b00000001)
        flag_command = self.FL & 0b00000001

        if flag_command == 0b00000001:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            self.pc += 2

    def handle_CMP(self):
        # print(f'CMP command has been called values to compare {self.reg[self.ram[self.pc + 1]]} {self.reg[self.ram[self.pc + 2]]}')
        self.alu('CMP', self.ram[self.pc + 1], self.ram[self.pc + 2])

    def handle_CALL(self):
        # first copy the current self.pc memory address and increment it by one address 
        # store the incremented self.pc address in the stack

        # set the self.pc variable to the address of the subroutine 

        return_address = self.pc + 2

        # place the return address onto the stack unable to use the handle_push function 
        self.reg[7] -= 1
        self.ram[self.reg[7]] = return_address

        # overwrite the self.pc variable to the address of the subroutine:
        self.pc = self.reg[self.ram[self.pc + 1]]

    def handle_RET(self):
        # pop the address before the subroutine off of the stack 
        # increment stack pointer 
        # overwrite self.pc with the address popped off of the stack 
        stack_head = self.ram[self.reg[7]]
        self.pc = stack_head 
        self.reg[7] += 1
        # print('stack head', stack_head)

    def handle_LDI(self):
        # write value in self.ram[self.pc + 2] into self.reg[self.pc + 1]
        # increment self.pc by three since command was three bytes.
        self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
        # print('value from ram at pc + 1', self.ram[self.pc + 1])
        # print('value from ram at pc + 2', self.ram[self.pc + 2])
        # self.pc += 3

    def handle_PRN(self):
        # find value in position self.pc + 1 in the register 
        # print the value as a decimal.
        # increment self.pc by two since command was two bytes.
        execute_value = self.reg[self.ram[self.pc + 1]]
        print(execute_value)
        # self.pc += 2

    def handle_MUL(self):
        # call the alu function within the cpu class 
        # self.alu(instruction, self.reg[self.ram[self.pc+1]], self.reg[self.ram[self.pc+1]])
        # pass the alu() method the opcode MUL, and both of the values in the 
        # register you would like to multiply
        self.alu('MUL', self.ram[self.pc + 1], self.ram[self.pc + 2])
        # self.pc += 3

    def handle_ADD(self):
        self.alu('ADD', self.ram[self.pc + 1], self.ram[self.pc + 2])

    def handle_pop(self):
        # pop the value at the top of the stack into the given register
        # check if the pointer is at the end of the stack (position 243)
            # if not
                # copy the value from the address pointed to by stack pointer to the
                # given register 
                # increment stack pointer 
            # if so:
                # print a message that says stack is empty
        if self.reg[7] != 243:
            stack_head = self.ram[self.reg[7]]
            self.reg[self.ram[self.pc + 1]] = stack_head 
            self.reg[7] += 1
        else:
            print('~~~~~Stack is empty~~~~~~')
        # self.pc += 2

    def handle_push(self):
        # Push the value in the given register on the stack 
            # Decrement the sp 
            # copy the value in the given register to the address pointed 
            # to by stack pointer 
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.reg[self.ram[self.pc + 1]]
        # print('ram after push', self.ram)
        # self.pc += 2

    def load(self, file_path):
        """Load a program into memory."""

        address = 0
        
        with open(file_path, 'r', newline=None) as f:
            commands = f.readlines()
            new_commands = []
            for instruction in commands:
                # print(instruction.rstrip('\n'))
                if instruction.startswith('0') or instruction.startswith('1'):
                    instruction_mod = instruction.split()
                    new_commands.append(instruction_mod[0])

        # add the new_commands array into the cpu's ram:
        for address in range(len(new_commands)):
            value = int(new_commands[address], 2)
            self.ram_write(value, address)

        # print('program ram', self.ram)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = self.FL | 0b00000001
            elif self.reg[reg_a] != self.reg[reg_b]:
                self.FL = self.FL & 0b00000110
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        # self.pc = 0

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_write(self, value, address):
        # this function accepts a value and an address to which the 
        # value will be stored in the ram array.

        # store the value into self.ram through self.ram[address] = value 

        # return a message that the insertion was a success

        self.ram[address] = value 
        # print(f'value {value} has been stored at ram position {address}') 

    def ram_read(self, address):
        # This function will take in an address (either in binary or 
        # base 10) and return the value stored in the ram in that specific 
        # adress 

        return self.ram[address]

    def run(self):
        """Run the CPU."""

        # specify the instruction variables (initial instructions LDI, HLT, PRN)
        HLT = 0b00000001 # used to stop the program 
        # create a while loop that will only terminate once the command 
        # HLT is read from the ram.
            # create an instruction variable (since the assumption is the 
            # first value in the ram is an instruction) initialize it to 
            # first index in ram.
            # create an instruction length variable that will be used to increment 
            # self.pc according to the first two values in the opcode.

            # if instruction is in the dictionary self.instruction_table:
                # run self.instruction_table[instruction]()
            # elif command is HLT:
                # terminate the while loop 
            # else:
                # print an error message

            # increment self.pc by instruction length

        while True:
            instruction = self.ram[self.pc] 
            instruction_length = ((instruction & 0b11000000) >> 6) + 1

            # obtain incrementation boolean flag from the binary opcode 
            # 5th place is the incrementation flag 
            instruction_increment = (instruction & 0b00010000) >> 4
            if instruction in self.instruction_table:

                if instruction_increment == 0b1:
                    self.instruction_table[instruction]()
                else:
                    self.instruction_table[instruction]()
                    self.pc += instruction_length
            elif instruction == HLT:
                break
            else:
                print(f'~~~~~Invalid Instruction~~~~~ at position {self.pc} {instruction}')
                break
                

        self.trace()