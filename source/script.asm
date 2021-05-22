section .data
    data0 db 'Insert your name: '
    len0 equ $ - data0
    data1 db 'Ola '
    len1 equ $ - data1

section .bss
    name resb 1

section .text
global _start
_start:
    mov eax, 4
    mov ebx, 1
    mov ecx, data0
    mov edx, len0
    int 0x80

    mov eax, 3
    mov ebx, 0
    mov ecx, name
    mov edx, 60
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, data1
    mov edx, len1
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, name
    mov edx, 60
    int 0x80

    mov eax, 1
    mov ebx, 0
    int 0x80

