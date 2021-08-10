#include <stdio.h>
int main(){char hello[] = "Hello, ";
printf("Insert your name: ");

char name[200];

scanf("%s", name);

printf("%s%s\n", hello,name);

return 0;}