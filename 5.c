#include "stdio.h"
int palindrome(char *, int);

int main() {
  printf("%d\n", palindrome("nolemonnomelon", 14));
  printf("%d\n", palindrome("civic", 5));
  return 0;
}

int palindrome(char *a , int b) {
  int ans = 0;
  b = b-1;
  for (int i = 0; i < b/2 -1; i++) {
    if (*(a+i) == *(a+(b--)))
      ans = 1;
    else{
      ans = 0;
    }
    if (ans == 0) break;
  }
  printf("ans = %d\n", ans);
  return ans;
}
// a[i] == *(a+i)
