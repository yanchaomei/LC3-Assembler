import binascii
import re


class asm_flie(object):
    # 这是汇编文件对象 存着原文件的每一行
    def __init__(self, asmname):
        self.asmfile_list = []
        with open(f"./{asmname}", 'r', encoding='utf-8') as f:
            for line in f:
                if line.find('\n') is not -1:
                    line = line[:line.find('\n')]
                self.asmfile_list.append(line)


class asm_code(object):

    def __init__(self, asmfile):
        self.asmcode = []
        for line in asmfile:
            if line.find(';') is not -1:
                line = line[:line.find(';')]
                if line is not '':
                    self.asmcode.append(line)
            else:
                if line is not '':
                    self.asmcode.append(line)
                else:
                    pass
            if line is '\t':
                self.asmcode.pop(self.asmcode.index(line))


class Shared(object):

    def __init__(self):
        self.opcode_operate = ['ADD', 'AND', 'NOT']
        self.opcode_data = ['LD', 'LDI', 'LDR', 'LEA', 'RIT', 'ST', 'STI', 'STR']
        self.opcode_control = ['BR', 'BRn', 'BRz', 'BRp', 'BRnz', 'BRnp', 'BRnzp', 'BRzp', 'JMP', 'JSR', 'JSRR', 'TRAP',
                               'RET', 'HALT']
        self.pseudoOps = ['.ORIG', '.FILL', '.BLKW', 'STRINGZ', '.END']


class Table(object):

    def __init__(self, file):
        number = file[0].find('x')
        number = '0x' + file[0][number + 1:]
        number = int(number, 16)
        counter = number
        self.number = number
        self.laber_map = {}
        for line in file:
            if line[0] is not '\t':
                laber = line[:line.find('\t')].strip()
                self.laber_map[laber] = hex(counter)[2:]
            else:
                pass
            counter = counter + 1
        print(self.laber_map)


class second_scan(object):

    def __init__(self, asmcode, table, shared):

        def process_opcodeOperate(self, opcode, line):
            # 正则匹配出寄存器对应机器码
            pattern = re.compile(r'R\d')
            Registers_list = re.findall(pattern, line)
            Registers_machine_list = []
            machine_code = ''
            for register in Registers_list:
                a = int(register[1:])
                b = '{:03b}'.format(a)
                Registers_machine_list.append(b)
            # 操作码是ADD的情况
            if opcode == 'ADD':
                if line.find('#') is not -1:
                    imm = int(line[line.find('#') + 1:])
                    if imm < 0:
                        imm = ((-imm) ^ 0b1111) + 1
                        machine_code = '0001' + Registers_machine_list[0] + Registers_machine_list[
                            1] + '1' + '1' + '{:04b}'.format(imm)
                    else:
                        machine_code = '0001' + Registers_machine_list[0] + Registers_machine_list[
                            1] + '1' + '{:05b}'.format(imm)
                else:
                    machine_code = '0001' + Registers_machine_list[0] + Registers_machine_list[1] + '000' + \
                                   Registers_machine_list[2]

                self.code.append(machine_code)
            # 操作码是NOT的情况
            if opcode == 'NOT':
                machine_code = '1001' + Registers_machine_list[0] + Registers_machine_list[1] + '111111'

                self.code.append(machine_code)
            # 操作码是AND的情况
            if opcode == 'AND':
                if line.find('#') is not -1:
                    imm = int(line[line.find('#') + 1:])
                    if imm < 0:
                        imm = ((-imm) ^ 0b1111) + 1
                        machine_code = '0101' + Registers_machine_list[0] + Registers_machine_list[
                            1] + '1' + '1' + '{:04b}'.format(imm)
                    else:
                        machine_code = '0101' + Registers_machine_list[0] + Registers_machine_list[
                            1] + '1' + '{:05b}'.format(imm)
                else:
                    machine_code = '0101' + Registers_machine_list[0] + Registers_machine_list[1] + '000' + \
                                   Registers_machine_list[2]
                self.code.append(machine_code)

        def process_opcodeData(self, opcode, line):
            # 正则匹配出寄存器对应机器码
            pattern = re.compile(r'R\d')
            Registers_list = re.findall(pattern, line)
            Registers_machine_list = []
            for register in Registers_list:
                a = int(register[1:])
                b = '{:03b}'.format(a)
                Registers_machine_list.append(b)
            machine_code = ''
            if opcode == 'LD':
                label = line[line.find(',') + 1:].strip()
                temp = int(self.table[label], 16)  # 获取标签对应的地址
                machine_code = '0010' + Registers_machine_list[0] + '{:09b}'.format(temp - self.counter - 1)
                self.code.append(machine_code)
            if opcode == 'LDI':
                label = line[line.find(',') + 1:].strip()
                temp = int(self.table[label], 16)  # 获取标签对应的地址
                machine_code = '1010' + Registers_machine_list[0] + '{:09b}'.format(temp - self.counter - 1)
                self.code.append(machine_code)
            if opcode == 'LDR':
                imm = line[line.find('#') + 1:]
                imm = int(imm)
                if imm < 0:
                    imm = ((-imm) ^ 0b11111) + 1
                    machine_code = '0110' + Registers_machine_list[0] + Registers_machine_list[
                        1] + '1' + '{:05b}'.format(imm)
                else:
                    machine_code = '0110' + Registers_machine_list[0] + Registers_machine_list[1] + '{:06b}'.format(imm)
                self.code.append(machine_code)
            if opcode == 'LEA':
                label = line[line.find(',') + 1:].strip()
                temp = int(self.table[label], 16)  # 获取标签对应的地址
                machine_code = '1110' + Registers_machine_list[0] + '{:09b}'.format(temp - self.counter - 1)
                self.code.append(machine_code)
            if opcode == 'RTI':
                machine_code = '1000000000000000'
                self.code.append(machine_code)
            if opcode == 'ST':
                label = line[line.find(',') + 1:].strip()
                temp = int(self.table[label], 16)  # 获取标签对应的地址
                machine_code = '0111' + Registers_machine_list[0] + '{:09b}'.format(temp - self.counter - 1)
                self.code.append(machine_code)
            if opcode == 'STI':
                label = line[line.find(',') + 1:].strip()
                temp = int(self.table[label], 16)  # 获取标签对应的地址
                machine_code = '1011' + Registers_machine_list[0] + '{:09b}'.format(temp - self.counter - 1)
                self.code.append(machine_code)
            if opcode == 'STR':
                imm = line[line.find('#') + 1:]
                imm = int(imm)
                if imm < 0:
                    imm = ((-imm) ^ 0b11111) + 1
                    machine_code = '0111' + Registers_machine_list[0] + Registers_machine_list[
                        1] + '1' + '{:05b}'.format(imm)
                else:
                    machine_code = '0111' + Registers_machine_list[0] + Registers_machine_list[1] + '{:06b}'.format(imm)
                self.code.append(machine_code)

        def process_opcodeControl(self, opcode, line):
            # 正则匹配出寄存器对应机器码
            if line.find('R') is not -1:

                pattern = re.compile(r'R\d')
                Registers_list = re.findall(pattern, line)
                Registers_machine_list = []

                for register in Registers_list:
                    a = int(register[1:])
                    b = '{:03b}'.format(a)
                    Registers_machine_list.append(b)
            machine_code = ''
            if re.match(r'BR\w*', opcode):
                label = line[line.find(' ') + 1:].strip()
                temp = int(self.table[label], 16)  # 获取标签对应的地址
                if (temp - self.counter - 1) < 0:
                    a = temp - self.counter - 1
                    a = ((-a) ^ 0b11111111) + 1
                    PCoffset = '1' + '{:08b}'.format(a)
                else:
                    PCoffset = '{:09b}'.format(temp - self.counter - 1)
                if opcode == 'BRn':
                    machine_code = '0000' + '100' + PCoffset
                if opcode == 'BRz':
                    machine_code = '0000' + '010' + PCoffset
                if opcode == 'BRp':
                    machine_code = '0000' + '001' + PCoffset
                if opcode == 'BRnz':
                    machine_code = '0000' + '110' + PCoffset
                if opcode == 'BRnp':
                    machine_code = '0000' + '101' + PCoffset
                if opcode == 'BRnzp':
                    machine_code = '0000' + '111' + PCoffset
                if opcode == 'BRzp':
                    machine_code = '0000' + '011' + PCoffset
                if opcode == 'BR':
                    machine_code = '0000' + '000' + PCoffset
                self.code.append(machine_code)
            if opcode == 'JMP':
                machine_code = '1100000' + Registers_machine_list[0] + '000000'
                self.code.append(machine_code)
            if opcode == 'RET':
                machine_code = '1100000111000000'
                self.code.append(machine_code)
            if opcode == 'JSR':
                label = line[line.find(' ') + 1:].strip()
                temp = int(self.table[label], 16)  # 获取标签对应的地址
                PCoffset = '{:011b}'.format(temp - self.counter - 1)
                machine_code = '0100' + '1' + PCoffset
                self.code.append(machine_code)
            if opcode == 'JSRR':
                machine_code = '0100000' + Registers_machine_list[0] + '000000'
                self.code.append(machine_code)
            if opcode == 'TRAP':
                number = line[line.find('x') + 1:].strip()
                number = int(number, 16)
                trapvect8 = '{:08b}'.format(number)
                machine_code = '11110000' + trapvect8
                self.code.append(machine_code)
            if opcode == 'HALT':
                machine_code = '11110000' + '{:08b}'.format(int('25', 16))
                self.code.append(machine_code)

        def process_pseudoOps(self, pseudoOps, line):
            if pseudoOps == '.ORIG':
                temp = line[line.find('x') + 1:]
                temp = int(temp, 16)
                machine_code = '{:016b}'.format(temp)
                self.code.append(machine_code)
            if pseudoOps == '.FILL':
                pattern = re.compile(r'x\d+')
                my_list = re.findall(pattern, line)
                my_list[0] = my_list[0][1:]
                number = int(my_list[0], 16)
                machine_code = '{:016b}'.format(number)
                self.code.append(machine_code)
            if pseudoOps == '.BLKW':
                pass
            if pseudoOps == '.STRINGZ':
                pass

        self.counter = table.number
        self.code = []
        self.table = table.laber_map
        for line in asmcode:
            opcode = line[line.find('\t') + 1:line.find(' ')]
            print(opcode)
            if opcode in shared.opcode_operate:
                process_opcodeOperate(self, opcode, line)
            elif opcode in shared.opcode_data:
                process_opcodeData(self, opcode, line)
            elif opcode in shared.opcode_control:
                process_opcodeControl(self, opcode, line)
            elif opcode in shared.pseudoOps:
                if opcode is '.END':
                    break
                process_pseudoOps(self, opcode, line)
            self.counter = self.counter + 1


if __name__ == "__main__":
    asmname = input("Please input name:\n")
    asmfile = asm_flie(asmname)  # 取得原文件
    asmcodes = asm_code(asmfile.asmfile_list)  # 去除了注释

    table = Table(asmcodes.asmcode)  # 创建了一个字典 存储laber和对应地址

    shared = Shared()
    code = second_scan(asmcodes.asmcode, table, shared)
    binname = asmname[:asmname.find('.')] + '.bin'
    with open(f"./{binname}", 'w', encoding='utf-8') as f:
        for line in code.code:
            f.write(line + '\n')

