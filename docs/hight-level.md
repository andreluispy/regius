[Return to README](../README.md)

# Comand Table

| COMAND | use | args | examples |
|---|---|---|---|
| exit | exit | NONE | exit; |
| print | write in console | Text or Var | print 'Hello World'; |
| input | get a input from user | var, var_bytes | input name 60; |
| var | create new var in asm section .data | var type, var name, var value | var dd name = 'Andre'; |
| if | compare values | value1, compare type, value2, function to call | if n1 > n2 greater; |
| label | start a label block | label name | label hello_world |
| end | end a label block  | label name | end hello_world |

# Learn Comands
## exit
 Use to exit from program:
 
 ```
exit;
 ```

## print
 Use to print a value in console

 args:
 - value to print

 example:

 ```
print 'Hello World';
exit;
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
 input name 100;

 print name;
 exit;
 ```
 


## var
 Use to create vars

 args:
 - var type
 - var name
 - var value

 Var types:
 - DB = Define Byte -> 1 byte
 - DW = Define Word -> 2 bytes
 - DD = Define Doubleword -> 4 bytes
 - DQ = Define Quadword -> 8 bytes
 - DT = Define Ten -> 10 bytes

 If your var bytes value is greater var type assembly add more bytes to your variable

 example:
 ```
var db name = 'Hello World', /n;

print name;
exit;
 ```

## Labels(functions)
 Assembly labels are the same as functions in other languages

 Define label block using the syntax:
 ```
label hello
# label_code
end hello
 ```

 Use `call` to call a function

 example:
 ```
label hello
print 'hello world', /n;
end hello

call hello;
exit;
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
print 'n1 is greater!', /n;
end greater

var dd n1 = 55;
var dd n2 = 20;

if n1 > n2 greater;
 ```


# Learn with Examples
 Not Avaible
