"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
# CALL = 0b01010000
# RET = 0b00010001
# ADD = 0b10100000

# Stack Pointer
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.running = False
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.reg[SP] = 0xf4
        self.ops = {}
        self.ops[LDI] = self.LDI
        self.ops[PRN] = self.PRN
        self.ops[HLT] = self.HLT
        self.ops[MUL] = self.MUL
        self.ops[PUSH] = self.PUSH
        self.ops[POP] = self.POP
        # self.ops[ADD] = self.ADD
        # self.ops[CALL] = self.CALL
        # self.ops[RET] = self.RET

    def LDI(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.ram_write(address, value)
        self.pc += 3

    def PRN(self):
        address = self.ram[self.pc + 1]
        self.ram_read(address)
        self.pc += 2
        
    
    def MUL(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('MUL', reg_a, reg_b)
        self.pc += 3
        
    def PUSH(self):
        # pushing the val moves indicator 1 below, or -1
        self.reg[SP] -= 1
        # Get the value we want to store from the register
        reg_num = self.ram[self.pc + 1]
        # set value to the actual value that is being pushed
        value = self.reg[reg_num]  
        # Copy the value in the given register to the address pointed to by SP.
        top_of_stack_addr = self.reg[SP]
        # Store it
        self.ram[top_of_stack_addr] = value
        self.pc += 2
        
        

    def POP(self):
    
        # get the register address
        reg_addr = self.ram[self.pc + 1]
        # Copy the value from the address pointed to by SP to the given register
        self.reg[reg_addr] = self.ram[self.reg[SP]]

        # as val is being popped, shift the indicator by +1
        self.reg[SP] += 1
        self.pc += 2

    
    def HLT(self):
        self.running = False

    def ram_read(self, address):
        print(self.reg[address])

    def ram_write(self, address, value):
        self.reg[address] = value
        

    def load(self):
        """Load a program into memory."""

        address = 0

        try:
            with open('examples/' + sys.argv[1]) as f:
                
                for line in f:
                    line = line.strip()
                    temp = line.split()
                    

                    if len(temp) == 0:
                        continue
                    elif temp[0][0] == '#':
                        continue

                    try:
                        self.ram[address] = int(temp[0], 2)
                    except ValueError:
                        print(f"Invalid number: {temp[0]}")
                        sys.exit(1)

                    address += 1

        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)
        except IndexError:
            print("Usage: First enter ls8.py followed by the file name: ls8.py filename")
            sys.exit(1)
    



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

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

    def run(self):
        self.running = True

        while self.running:
            ## Branch table
            ir = self.ram[self.pc]
            self.ops[ir]()
            
      
        # if ir in self.ops:
        #     self.ops[ir]()

        #     # show error message
        # else:
        #     print(f"Unknown expression {ir} at address {self.pc}")
        #     sys.exit(1)