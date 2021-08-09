
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

section .data
    data0 db "hello", 0xA
    len0 equ $ - data0

section .bss
