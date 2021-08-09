#include <stdio.h>
int main(){char hello[] = "Hello, ";
char name[] = "0000000000000";
printf("Insert your name: ");

scanf("%s", name);

printf("%s%s\n", hello,name);

return 0;}