// ---------------------------------------------
// Programa, em linguagem C, que le um numero n
// e imprime os n primeiros numeros da sequencia
// de Fibonacci. Alem disso, aproxima a razao 
// aurea dividindo um termo pelo anterior.
// ---------------------------------------------

#include <stdio.h>

int main() {
  long int a,b,c;
  int n,cont;
  double r;

  printf("Digite quantos termos da sequencia de Fibonacci voce quer:\n");
  scanf("%d", &n);

  if (n <= 1) {
    printf("Numero de termos invalido\n");
  }
  else {
    
    a = 1;
    b = 1;
    cont = 2;
    printf("\n\n1\n1\n");

    while(cont < n) {
      c = a + b;
      r = c;
      r = r/b;
      printf("%ld %.15lf\n", c, r);
      a = b;
      b = c;
      cont = cont + 1;
      //eh a mesma coisa: cont++;
    }
  }

  return(0);
}
