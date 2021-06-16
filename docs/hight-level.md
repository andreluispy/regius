[Return to README](../README.md)

# Comand Table

| COMAND | use | args | examples |
|---|---|---|---|
| // | comment line | none | // a comment! |
| exit | exit | return value | exit; |
| print | write in console | Text or Var | print 'Hello World'; |
| input | get a input from user | var, var_bytes | input name 60; |
| var | create new var in asm section .data | var type, var name, var value | var dd name = 'Andre'; |
| if | compare values | value1, compare type, value2, function to call | if n1 > n2 greater; |
| label | start a label block | label name | label hello_world |
| end | end a label block  | label name | end hello_world |
| import | import regius libs | script lib | import regiuslib.rgs |
| include | import asm libs | script lib | include asmlib.inc |

# Learn Comands

## comments
 Use `//` to make comments in languagem, example:

 ```
print "hello world", /n // show hello world and use /n to break a line
 ```

## exit
 Use to exit from program:
 
 ```
exit
 ```
 
 Using return code:
 ```
exit 0
 ```

## print
 Use to print a value in console

 args:
 - value to print

 example:

 ```
print 'Hello World'
exit
 ```

 Use special args:
 - /n - Use to make a new line

## input
 Use to get a value from user
 
 args:
 - var to get input
 - input max bytes

 example:
 ```
 input name 100

 print name
 exit
 ```
 
## var
 Use to create vars

 args:
 - var size
 - var name
 - var value

 Var sizes:
 - DB = Define Byte -> 1 byte
 - DW = Define Word -> 2 bytes
 - DD = Define Doubleword -> 4 bytes
 - DQ = Define Quadword -> 8 bytes
 - DT = Define Ten -> 10 bytes

 If your var bytes value is greater var size assembly add more bytes to your variable

 example:
 ```
var db name = 'Hello World', /n

print name
exit
 ```

## Labels(functions)
 Assembly labels are the same as functions in other languages

 Define label block using the syntax:
 ```
label hello

// label code

end hello
 ```

 Use `call` to call a function

 example:
 ```
label hello
print 'hello world', /n
end hello

call hello
exit
 ```

## if
 Use to compare values

 args:
 - value1
 - compare type
 - value2
 - function to call if compare is true

 examples:
 ```
label greater
print 'n1 is greater!', /n
end greater

var dd n1 = 55
var dd n2 = 20

if n1 > n2 greater
 ```

## import
 Make and use regius lib!

 in `main.rgs`:
 ```
import regiuslib.rgs

call hello
exit
 ```

 in `regiuslib.rgs`:
 ```
label hello

print "hello world", /n

end hello
 ```

## include
 Make and use libs writed in assembly!

 in `main.rgs`:
 ```
include asmlib.inc

call hello
exit
 ```

 in `asmlib.inc`:
 ```
section .text
hello:
    mov eax, 4
    mov ebx, 1
    mov ecx, msg
    mov edx, len
    int 0x80

    ret

section .data
    msg db 'Hello World', 0xA
    len equ $ - msg
 ```

# Learn with Examples
 Not Avaible
