%include 'asmlib.inc'

section .text
global _start
_start:
    call hello

    mov eax, 1
    mov ebx, 0
    int 0x80

section .data

section .bss
