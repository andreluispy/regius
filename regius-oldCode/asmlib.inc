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
