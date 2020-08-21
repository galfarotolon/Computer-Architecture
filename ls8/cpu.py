"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111 
JEQ = 0b01010101 
JMP = 0b01010100
JNE = 0b01010110

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
        self.ops[CALL] = self.CALL
        self.ops[RET] = self.RET
        self.ops[ADD] = self.ADD
        self.ops[CMP] = self.CMP
        self.ops[JEQ] = self.JEQ
        self.ops[JMP] = self.JMP
        self.ops[JNE] = self.JNE
        # Flag
        # init to 0, if not, change to 1 in alu
        self.E = 0
        self.L = 0
        self.G = 0 
        
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
    
    ## Need the ADD so call.ls8 works since its using the add in its program
    def ADD(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('ADD', reg_a, reg_b)
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
        
    def CALL(self):
        # Push return address
        return_address = self.pc + 2
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = return_address
        
        # call subroutine
        reg_num = self.ram[self.pc + 1]
        self.pc = self.reg[reg_num]
    
    def RET(self):
      
        # pop the return addr off the stack
        ret_addr = self.ram[self.reg[SP]]
        self.reg[SP] += 1
        
        #set pc  to it
        
        self.pc = ret_addr
        
    def CMP(self):
        
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        # print(reg_a)
        # print(reg_b)
        self.alu("CMP", reg_a, reg_b)
        self.pc += 3
    
    def JMP(self):
        reg_num = self.ram[self.pc + 1]

        self.pc = self.reg[reg_num]
        
    def JEQ(self):
    # Jump if equal to 1
        
    # If equal (i.e. E) flag is set (true) (i.e 1), jump to the address stored in the given register.
       if self.E == 1:
           self.pc = self.reg[self.ram[self.pc + 1]]
       else:
           self.pc += 2
    
    def JNE(self):
    # jump if equal to 0
    
    # If `E` flag is clear (i.e 0), jump to the address stored in the given register.
        if self.E == 0:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
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
        elif op == 'CMP':
            
            # If they are equal, set the Equal E flag to 1, otherwise set it to 0.
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
            # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.L = 1
            # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.G = 1
            
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
        
  