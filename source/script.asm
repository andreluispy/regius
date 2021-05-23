section .text
global _start
_start:
    call hello
    mov eax, 1
    mov ebx, 0
    int 0x80

hello:
    mov eax, 4
    mov ebx, 1
    mov ecx, data0
    mov edx, len0
    int 0x80

    ret

section .data
    data0 db 'hello world', 0xA
    len0 equ $ - data0

section .bss

