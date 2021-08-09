# Regius
 A low-level language that is compiled into assembly, with 2 syntax:

 - Main Low Level Syntax
 - Optional Hight Level Syntax
 
 All syntax is possible to use in mix!

# Compare
 Hello World:
 - c: 17kb
 - regius: 9kb

# Hello World
 Try in hight level syntax:

 ```
print 'Hello World', /n
exit
 ```

 Try in low level syntax:
 
 ```
$m = 4;
$n = 1;
$v = 'Hello World', /n;
call kernell;

$m = 1;
$v = 0;
call kernell;
 ```

This in assembly x86 code:

 ```
section .data
    data0 db 'Hello World', 0xA
    len0 equ $ - data0

section .text
global _start
_start:
    mov eax, 4
    mov ebx, 1
    mov ecx, data0
    mov edx, len0
    int 0x80

    mov eax, 1
    mov ebx, 0
    int 0x80
 ```

# Docs

 View Low-Level Syntax Docs:
 
 [unavailable](README.md)

 View Hight-Level Syntax Docs:

 [Click Here](docs/hight-level.md)

# Legal

    MIT License

    Copyright (c) 2021 Andre Luis

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

