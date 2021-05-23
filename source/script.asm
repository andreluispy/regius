section .text
global _start
_start:
    mov eax, DWORD[n1]
    mov ebx, DWORD[n2]
    cmp eax, ebx
    jl skip0
    je skip0
    call maior

skip0:
    mov eax, DWORD[n1]
    mov ebx, DWORD[n2]
    cmp eax, ebx
    jg skip1
    je skip1
    call menor

skip1:
    mov eax, 1
    mov ebx, 0
    int 0x80

maior:
    mov eax, 4
    mov ebx, 1
    mov ecx, data0
    mov edx, len0
    int 0x80

    ret
menor:
    mov eax, 4
    mov ebx, 1
    mov ecx, data1
    mov edx, len1
    int 0x80

    ret

section .data
    n1 dd 50
    n2 dd 25
    data0 db 'é maior', 0xA
    len0 equ $ - data0
    data1 db 'é menor', 0xA
    len1 equ $ - data1

section .bss

