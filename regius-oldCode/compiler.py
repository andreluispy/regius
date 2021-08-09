#!/usr/bin/env python3

######################################################################
#             Regius Transpiler for Linux Asm x86                    #
######################################################################
#                             To Do:                                 #
#                                                                    #
# - Use C code in asm | gcc -S script.c                              #
# - Use Python compiled in asm | Cython(python > c); gcc -S script.c #
#                                                                    #
######################################################################

from os import system, remove
from sys import argv

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
read_lib = False
lib = []
asmcodes = []

def transpiler():
    global script, line, data, label_start, labels, actual_data, actual_mode, actual_var, actual_skip, lenght, comps, read_lib, lib, asmcodes

    modo = 0
    split = line.split()

    if line[0:1] == '//':
        line = ''
    elif '//' in line:
        line = line[0:line.find('//')]

    if line[0] == '$':
        # if manipule system mode (eax)
        if line[1] == 'm':
            modo = (split[2])[0:-1] # mode
            label_start.append(f'    mov eax, {modo}') # append eax
            
            # globals to control
            actual_mode = modo
        elif line[1] == 'n': # ebx
            modo = (split[2])[0:-1]
            label_start.append(f'    mov ebx, {modo}')
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
                bss[value] = f'resb 1' # create bss var
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
                    try:
                        label_start.append(f'    mov edx, {lenght[value]}')
                    except:
                        label_start.append(f'    mov edx, {10}') 
    elif split[0] == 'label':
        label_name = split[1] # label name

        if read_lib == False:
            # get label code and update script code
            arq = script[script.index(line)+1:script.index('end '+label_name)]
            # script.index(line)+1:script.index('end '+label_name)
            startl = script.index(line)
            endl = script.index('end '+label_name)
            for _lline in range(startl, endl):
                script[_lline] = ''
        else:
            arq = lib[lib.index(line)+1:lib.index('end '+label_name)]
            
            startl = lib.index(line)
            endl = lib.index('end '+label_name)
            for _lline in range(startl, endl):
                lib[_lline] = ''
            
            read_lib = False

        lssave = label_start.copy()
        label_start = []

        for _llines in arq:
            line = _llines
            if line == '':
                pass
            else:
                transpiler()

        labels[label_name] = label_start.copy() # add label to labels(dict)
        label_start = lssave.copy()
    elif split[0] == 'call': # call functions
        # call kernel(int 0x80)
        if split[1] == 'kernell;':
            label_start.append(f'    int 0x80\n')
        # call functions
        else:
            label_start.append(f'    call {split[1]}\n')
    elif split[0] == 'var':
        vtype = split[1]
        vname = split[2]
        value = line[line.find('=')+2:]
        data[vname] = f'{vtype} {value}'
    elif split[0] == 'if':
        v1, v2 = split[1], split[3]
        cmptype = split[2]
        cmpfunction = split[4]

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
    elif split[0] == 'exit': # exit
        try:
            returnvalue = split[1]
        except IndexError:
            returnvalue = '0'
        
        line = '$m = 1;'
        transpiler()
        line = f'$v = {returnvalue};'
        transpiler()
        line = 'call kernell;'
        transpiler()
    elif split[0] == 'print': # print
        # check if use ' or "
        if "'" in line:
            value = line[line.find("'"):]
        elif '"' in line:
            value = line[line.find('"'):]
        elif split[1] == '/n':
            value = "'', 0xA"
        else:
            value = split[1]

            if value+'buffer:' in bss.keys():
                value = value+'buffer'
            else:
                pass
        line = '$m = 4;'
        transpiler()
        line = '$n = 1;'
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
        line = '$n = 0;'
        transpiler()
        line = f'$v = {varn};'
        transpiler()
        line = f'$i = {size};'
        transpiler()
        line = 'call kernell;'
        transpiler()
    elif split[0] == 'conv': # converter
        convtype = split[1]
        value = split[2]

        if convtype == 'int':
            '''
            lea esi, [v1]
            mov ecx, 3
            call string_to_int
            '''
            if 'string_to_int' in labels.keys():
                pass
            else:
                labels['string_to_int'] = ['    xor ebx, ebx;','.prox_digito:','    movzx eax, byte[esi]','    inc esi',"    sub al, '0'",'    imul ebx, 10','    add ebx, eax','    loop .prox_digito','    mov eax, ebx']

            if value in data.keys():
                vlen = len((data[value].split())[1])-2
            else:
                vlen = 2

            label_start.append(f'    lea esi, [{value}]')
            label_start.append(f'    mov ecx, {vlen}')
            label_start.append(f'    call string_to_int\n')
        elif convtype == 'string':
            '''
            ; convert to string
            lea esi, [buffer]
            call int_to_string
            '''
            if 'int_to_string' in labels.keys():
                pass
            else:
                labels['int_to_string'] = ['    add esi, 9','    mov byte [esi], 0','    mov ebx, 10','.prox_digito:','    xor edx, edx','    div ebx',"    add dl, '0'",'    dec esi','    mov [esi], dl','    test eax, eax','    jnz .prox_digito','    mov eax, esi']
            label_start.append(f'    lea esi, [{value}buffer]')
            label_start.append(f'    call int_to_string\n')
            bss[f'{value}buffer:'] = 'resb 10'
    elif split[0] == 'add': # add
        '''
        mov eax, [n1]
	    sub eax, '0'  ;Converte para int
	    add eax, '0'  ;Converte para string
	    mov [n1], eax
        '''
        varn = split[1]
        value = split[2]

        label_start.append(f'    add eax, {value}\n')
    elif split[0] == 'import': # import externals codes
        file = split[1]
        lib = open(file, 'r', encoding='utf-8').readlines()
        for _line in lib:
            lib[lib.index(_line)] = _line.replace('\n', '')
        
        for _indice in range(0, len(lib)):
            line = lib[_indice]
            if line.isspace() or line == '\n' or line == '':
                pass
            else:
                read_lib = True
                transpiler()

    elif split[0] == 'include': # import externals asm codes
        asmcodes.append(f"%include '{split[1]}'")

if __name__ == '__main__':
    # interpreter
    args = argv
    file = args[1]
    file_name = file[0:file.rfind(".")]
    script = open(file, 'r', encoding='utf-8').readlines()
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
    export = open(f'{file_name}.asm', 'w', encoding='utf-8')

    # write asm codes
    for _lib in asmcodes:
        export.write(f'{_lib}\n')
    export.write(f'\n')

    # write section .text
    for _line in label_start:
        export.write(_line+'\n')
    
    for k, v in labels.items():
        export.write(f'{k}:\n')
        label_start = v

        # write label code
        for _line in label_start:
            export.write(f'{_line}\n')
        
        export.write(f'    ret\n\n') # return to main code

    # write section .data
    export.write('section .data\n')
    for k, v in data.items():
        v = v.replace('/n', '0xA')
        export.write(f'    {k} {v}'+'\n')
    export.write('\n')

    # write section .bss
    export.write('section .bss\n')
    for k, v in bss.items():
        # name resb 1
        export.write(f'    {k} {v}\n')
    
    export.close()
    # local test
    print('Testing:\n')
    system(f'nasm -f elf64 {file_name}.asm')
    system(f'ld -s -o {file_name} {file_name}.o')
    remove(f'./{file_name}.o')
    system(f'./{file_name}')
