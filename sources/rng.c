#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <inttypes.h>
#include <errno.h>
#include <string.h>

int main(int argc, char const *argv[]) {
  int maxRng = 6;
  argv++;
  if (argc > 1) {
    // convert stdin to int
    maxRng = strtoimax(*argv, NULL,0);
  }
  if (!maxRng) {
    puts("perhaps you used this function wrong? Exiting.");
    return 404;
  }
  // return_value
  int num;
  // random seed is based on time
  srand (time(NULL));
  // generate a random number
  num = rand() % maxRng;
  // make the number definetely greater than 0
  num++;
  printf("%i\n", num);
  return 0;
}
