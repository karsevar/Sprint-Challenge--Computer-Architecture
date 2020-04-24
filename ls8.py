#!/usr/bin/env python3

"""Main."""
import re
import sys
from cpu import *

# write a load function that will take a file path 
# as an argument file path is sys.argv[1]

# def load(file_path):
#     with open(file_path, 'r', newline=None) as f:
#         commands = f.readlines()
#         new_commands = []
#         for instruction in commands:
#             # print(instruction.rstrip('\n'))
#             if instruction.startswith('0') or instruction.startswith('1'):
#                 instruction_mod = instruction.split()
#                 new_commands.append(instruction_mod[0])

#     return new_commands

# new_commands = load(sys.argv[1])

# create a function that will iterate through the 
# loaded in values from an external file and save them 
# into the cpu's ram.
    # use a for loop to iterate through the command array 
        # use cpu.ram_write() to write the value into the 
        # cpu's ram 

# def add_to_ram(instructions, cpu):
#     for address in range(len(instructions)):
#         value = int(instructions[address], 2)
#         # print(value)
#         cpu.ram_write(value, address)

# print(new_commands)

cpu = CPU()

# add_to_ram(new_commands, cpu)
cpu.load(sys.argv[1])

cpu.run()