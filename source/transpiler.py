import sys, os

line = ''
actual_data = 0
actual_mode = 1
actual_var = ''
actual_skip = 0
data = {}
bss = {}
label_start = ['section .text', 'global _start', '_start:']
lenght = {}
labels = {}
comps = {'>':'jg', '<':'jl', '==':'je'}

def transpiler():
    global script, line, data, label_start, labels, actual_data, actual_mode, actual_var, actual_skip, lenght, comps

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
                        data['data'+str(actual_data)] = f'db {value}'
                        data['len'+str(actual_data)] = 'equ $ - '+'data'+str(actual_data)

                        # create edx
                        label_start.append(f'    mov edx, {"len"+str(actual_data)}')
                    
                        actual_data += 1 # control data automation
                    else:
                        pass
                else: # if data is a var
                    label_start.append(f'    mov ecx, {value}')
                    label_start.append(f'    mov edx, {lenght[value]}')
    
    elif split[0] == 'label':
        label_name = split[1] # label name

        # get label code and update script code
        arq = script[script.index(line)+1:script.index('end '+label_name)]
        # script.index(line)+1:script.index('end '+label_name)
        startl = script.index(line)
        endl = script.index('end '+label_name)
        for _lline in range(startl, endl):
            script[_lline] = ''

        labels[label_name] = arq # add label to labels(dict)

    elif split[0] == 'call': # call functions
        # call kernel(int 0x80)
        if split[1] == 'kernell;':
            label_start.append(f'    int 0x80\n')
        
        # call functions
        elif (split[1])[0:-1] in labels.keys():
            label_start.append(f'    call {(split[1])[0:-1]}')

    # vars
    elif split[0] == 'var':
        vtype = split[1]
        vname = split[2]
        value = line[line.find('=')+2:-1]
        data[vname] = f'{vtype} {value}'
    
    # if
    elif split[0] == 'if':
        v1, v2 = split[1], split[3]
        cmptype = split[2]
        cmpfunction = (split[4])[0:-1]

        # dword
        label_start.append(f'    mov eax, DWORD[{v1}]')
        label_start.append(f'    mov ebx, DWORD[{v2}]')
        label_start.append(f'    cmp eax, ebx')

        if cmptype == '==':
            label_start.append(f'    jne skip{actual_skip}')
        elif cmptype == '!=':
            label_start.append(f'    je skip{actual_skip}')
        else:
            for k, v in comps.items():
                if k != cmptype:
                    label_start.append(f'    {v} skip{actual_skip}')
        
        label_start.append(f'    call {cmpfunction}\n')
        label_start.append(f'skip{actual_skip}:')
        actual_skip += 1

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
    script = open('script.rgs', 'r', encoding='utf-8').readlines()
    for _line in script:
        script[script.index(_line)] = _line.replace('\n', '')

    try:
        for indice in range(0, len(script)):
            line = script[indice]
            if line.isspace() or line == '\n' or line == '':
                pass
            else:
                transpiler()
    except IndexError:
        pass

    # write file
    export = open('script.asm', 'w', encoding='utf-8')

    # write section .text
    for _line in label_start:
        export.write(_line+'\n')
    
    for k, v in labels.items():
        export.write(f'{k}:\n')
        label_start = []

        for i in v:
            line = i
            if line.isspace() or line == '\n' or line == '':
                pass
            else:
                transpiler()

        # write label code
        for _line in label_start:
            export.write(f'{_line}\n')
        
        export.write(f'    ret\n') # return to main code

    # write section .data
    export.write('\nsection .data\n')
    for k, v in data.items():
        v = v.replace('/n', '0xA')
        export.write(f'    {k} {v}'+'\n')
    export.write('\n')

    # write section .bss
    export.write('section .bss\n')
    for k, v in bss.items():
        #    name resb 1
        export.write('    '+v+' resb 1\n')
    export.write('\n')
    
    export.close()

    # local test
    print('Testing:\n')
    os.system('nasm -f elf64 script.asm')
    os.system('ld -s -o script script.o')
    os.remove('./script.o')
    os.system('./script')
