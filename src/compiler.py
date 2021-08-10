#! /bin/python3

# language types
STRING = "STRING"
INT = "INT"
IDENTIFY = "IDENTIFY"
NULL = "NULL"

def error(line, error):
    print(f"Error in line {line}: {error}")

class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class compiler:
    def __init__(self):
        self.function = {}
        self.includes = []
        self.ccode = []
        self.vars = {}
        self.actual_line = 0

    def main(self, line):
        self.i = 0  # line index
        self.c = '' # actual char
        self.line = line # actual line
        self.actual_token = token(NULL, '')
        self.tokens = []
        self.args = []
        self.in_string = False # bool controler to strings
        
        self.actual_line += 1
        while True:
            try:
                self.c = self.line[self.i]
            except:
                return

            if self.c == ';':
                break
            elif self.c.isdigit() and self.actual_token.type == INT or self.c.isdigit() and self.actual_token.type == NULL: # se a char atual é um numero ou estamos em um numero INT ou começando um token
                self.actual_token.type = INT
                self.actual_token.value = self.actual_token.value + self.c # atualizar numero

                if self.line[self.i+1].isdigit(): # se o proximo char for um numero
                    pass
                else:
                    self.tokens.append(self.actual_token)
                    self.actual_token = token(NULL, '')
            elif self.c == '"':
                if self.in_string:
                    self.in_string = False
                    self.tokens.append(self.actual_token)
                    self.actual_token = token(NULL, '')
                else:
                    self.actual_token.type = STRING
                    self.in_string = True
            elif self.c.isalnum() or self.c in ["\\", ":", "%", ",", "_"]:
                if self.in_string: # se está em uma string
                    self.actual_token.value = self.actual_token.value + self.c
                else:
                    if self.c in [" ", ';', ","]:
                        self.tokens.append(self.actual_token)
                        self.actual_token = token(NULL, '')
                    else:
                        self.actual_token.type = IDENTIFY
                        self.actual_token.value = self.actual_token.value + self.c
                    
                    if self.line[self.i + 1] in [" ", ';', ","]:
                        self.tokens.append(self.actual_token)
                        self.actual_token = token(NULL, '')

            elif self.c == ' ' and self.in_string:
                self.actual_token.value = self.actual_token.value + self.c
            elif self.c == "(" or self.c == ")":
                if self.actual_token.type == IDENTIFY:
                    self.tokens.append(self.actual_token)
                    self.actual_token = token(NULL, "")

            self.i += 1

        #for _token in self.tokens:
            #print(_token.type, _token.value)

        # Note: token.type; token.value; self.ccode
        # Code generate
        if self.tokens[0].value in self.function.keys():
            args = (self.function[self.tokens[0].value])["args"]
            
            if args != []:
                for _line in (self.function[self.tokens[0].value])["code"]:
                    for arg in args:
                        if arg.startswith('*'):
                            sArgs = ""
                            for tokenArg in self.tokens[args.index(arg)+2:]:
                                if tokenArg.type == NULL:
                                    pass
                                else:
                                    if tokenArg.type == STRING:
                                        sArgs = f'{sArgs},"{tokenArg.value}"'
                                    else:
                                        sArgs = f"{sArgs},{tokenArg.value}"
                            sArgs = sArgs[1:]
                            _line = _line.replace("${"+arg[1:]+"}$", sArgs)
                        elif arg.startswith('...'):
                            mArgs = ""
                            for tokenArg in self.tokens[args.index(arg)+2:]:
                                if tokenArg.type == NULL:
                                    pass
                                else:
                                    mArgs = f"{mArgs},{tokenArg.value}"
                            
                            mArgs = mArgs[1:]+"}"
                            mArgs = "{"+mArgs
                            print(mArgs)
                            _line = _line.replace("${"+arg[3:]+"}$", mArgs)
                        else:
                            _line = _line.replace("${"+arg+"}$", self.tokens[args.index(arg)+1].value)
                    
                    self.ccode.append(_line)
            else:
                for _line in (self.function[self.tokens[0].value])["code"]:
                    self.ccode.append(_line)
        elif self.tokens[0].value == "var":
            # self.tokens[1].value == var name
            # self.tokens[3] == var value/type
            self.vars[self.tokens[1].value] = self.tokens[2]

            if self.tokens[2].type == STRING:
                self.ccode.append(f'char {self.tokens[1].value}[] = "{self.tokens[2].value}";')
            elif self.tokens[2].type == INT:
                self.ccode.append(f'int {self.tokens[1].value} = {self.tokens[2].value};')
            
        elif self.tokens[0].value == "import":
            libscript = open(f"{self.tokens[1].value}.rgc", "r").readlines()

            # Libs
            for lib in libscript[0].split():
                    self.includes.append(f"#include {lib}")
            
            in_label = False
            actual_func = ""
            for libline in libscript[1:]:
                line_split = libline.split()
                if in_label:
                    if libline.isspace():
                        pass
                    elif line_split[0] == "end":
                        in_label = False
                        actual_func = ""
                    else:
                        (self.function[actual_func])["code"].append(libline)
                else:
                    try:
                        if line_split[0] == "label":
                            in_label = True
                            actual_func = line_split[1]
                            self.function[actual_func] = {"args":[], "code":[]}
                            for arg in line_split[2:-1]:
                                (self.function[actual_func])["args"].append(arg)
                    except IndexError:
                        pass
        else:
            print(f"Error in line: {self.line}\n")
            pass

def main():
    from os import system, remove

    Compiler = compiler()
    code = open('script.rgs', 'r')
    for _line in code:
        Compiler.main(_line)
    code.close()
    
    # Write Code
    script = open("tmp.c", "w")

    # Write Libs
    for _line in Compiler.includes:
        script.write(f"{_line}\n")
    
    script.write('int main(){')
    for line in Compiler.ccode:
        script.write(line+"\n") # Write Next Line

    script.write('return 0;')
    script.write('}')
    script.close()
    
    system("gcc tmp.c -o main")
    #remove("tmp.c")

main()