import sys, os

line = ''
actual_data = 0
actual_mode = 1
actual_var = ''
data = {}
bss = {}
label_start = ['section .text', 'global _start', '_start:']
lenght = {}

def transpiler():
    global line, data, label_start, actual_data, actual_mode, actual_var, lenght

    modo = 0
    split = line.split()

    # if manipule system vars
    if line[0] == '$':
        # if manipule system mode
        if line[1] == 'm':
            modo = line[line.find("=")+2:line.find(";")] # mode
            label_start.append(f'    mov eax, {modo}') # append eax
            
            # ebx
            if modo == '4':
                label_start.append(f'    mov ebx, 1')
            if modo == '3':
                label_start.append(f'    mov ebx, 0')
            
            # globals to control
            actual_mode = modo
        # if manipule system i(secundary)
        elif line[1] == 'i':
            value = line[line.find("=")+2:line.find(";")]
            label_start.append(f'    mov edx, '+value)
            lenght[actual_var] = value
        # if manipule system value
        elif line[1] == 'v':
            value = line[line.find("=")+2:line.find(";")]

            # if mode == 1
            if actual_mode == '1':
                label_start.append(f'    mov ebx, {value}')
            # if mode == 3
            elif actual_mode == '3':
                label_start.append(f'    mov ecx, '+value) # create ecx
                bss[value] = value # create bss var
                actual_var = value
            # if mode == 4
            elif actual_mode == '4':
                # if print a string
                if '"' in value or "'" in value:
                    igual = False
                    for k, v in data.items():
                        if value in v:
                            igual = True
                            label_start.append(f'    mov ecx, {k}')
                            label_start.append(f'    mov edx, {"len"+k[-1]}')

                    if igual == False:
                        # create ecx
                        label_start.append(f'    mov ecx, {"data"+str(actual_data)}')
                    
                        # control data automation
                        data['data'+str(actual_data)] = value
                        data['len'+str(actual_data)] = 'equ $ - '+'data'+str(actual_data)

                        # create edx
                        label_start.append(f'    mov edx, {"len"+str(actual_data)}')
                    
                        actual_data += 1 # control data automation
                    else:
                        pass
                else: # if data is a var
                    label_start.append(f'    mov ecx, {value}')
                    label_start.append(f'    mov edx, {lenght[value]}')
    elif split[0] == 'call': # call functions
        # call kernel(int 0x80)
        if split[1] == 'kernell;':
            label_start.append(f'    int 0x80\n')
    # hight level syntax
    elif split[0] == 'pause;': # pause
        line = '$m = 3;'
        transpiler()
        line = '$v = sys;'
        transpiler()
        line = '$i = 1;'
        transpiler()
        line = 'call kernell;'
        transpiler()
    elif split[0] == 'exit;': # exit
        line = '$m = 1;'
        transpiler()
        line = '$v = 0;'
        transpiler()
        line = 'call kernell;'
        transpiler()
    elif split[0] == 'print': # print
        # check if use ' or "
        if "'" in line:
            value = line[line.find("'"):-1]
        elif '"' in line:
            value = line[line.find('"'):-1]
        else:
            value = split[1]
        line = '$m = 4;'
        transpiler()
        line = f'$v = {value};'
        transpiler()
        line = 'call kernell;'
        transpiler()
    elif split[0] == 'input': # input
        varn = split[1]
        size = split[2]
        line = '$m = 3;'
        transpiler()
        line = f'$v = {varn};'
        transpiler()
        line = f'$i = {size};'
        transpiler()
        line = 'call kernell;'
        transpiler()

if __name__ == '__main__':
    # interpreter
    for _line in open('script.rgs', 'r', encoding='utf-8'):
        line = _line.replace('\n', '')
        
        if line.isspace() or line == '\n' or line == '':
            pass
        else:
            transpiler()

    # write file
    export = open('script.asm', 'w', encoding='utf-8')

    # write section .data
    export.write('section .data\n')
    for k, v in data.items():
        if k[0:4] == 'data':
            v = v.replace('/n', '0xA')
            export.write(f'    {k} db {v}'+'\n')
        elif k[0:3] == 'len':
            export.write(f'    {k} {v}'+'\n')
    export.write('\n')

    # write section .bss
    export.write('section .bss\n')
    for k, v in bss.items():
        #    name resb 1
        export.write('    '+v+' resb 1\n')
    export.write('\n')

    # write section .text
    for _line in label_start:
        export.write(_line+'\n')
    
    export.close()

    # local test
    print('Testing:\n')
    os.system('nasm -f elf64 script.asm')
    os.system('ld -s -o script script.o')
    os.remove('./script.o')
    os.system('./script')
