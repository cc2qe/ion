#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>

double log_choose(double n, double k)
{
  int d;
  double r = 0;

  // swap for efficiency if k is more than half of n
  if (k*2 > n) {
    k = n - k;
  }

  for (d = 1; d <= k; ++d) {
    r += log10(n--);
    r -= log10(d);
  }

  return r;
}

double fisher(int a,
              int b,
              int c,
              int d)
{
  double log_p_val;
  double p_val;
  log_p_val = log_choose(a + b, a) + log_choose(c + d, c) - log_choose(a + b + c + d, a + c);
  p_val = pow(10, log_p_val);

  // printf("00: %d\t01: %d\t10: %d\t11: %d\n", obs1, obs2, obs3, obs4);

  return p_val;
}

int usage()
{
  fprintf(stderr,
          "usage: fisher [options] <a> <b> <c> <d>\n\n"
          "author: Colby Chiang (cc2qe@virginia.edu)\n"
          "description: Calculates fisher exact p-value\n"
          "  for a 2x2 contingency table. Able to handle\n"
	  "  large numbers\n"
          "\n"
          "positional arguments:\n"
	  "   _______\n"
	  "  | a | b |\n"
	  "  |___|___|\n"
	  "  | c | d |\n"
	  "  |___|___|\n\n"
          "  a, b, c, d             observed values in the 2x2 contingency table\n"
          "\n"
          "optional arguments:\n"
          "  -h                     show this help and exit\n"
          "\n"
          );
  return 1;
}


int main (int argc, char **argv)
{
  // parse the optional arguments
  int i;
  while ((i = getopt(argc, argv, "h")) != -1) {
    switch (i) {
    case 'h':
      return usage();
    }
  }

  // parse the positional arguments
  int a = atoi(argv[1]);
  int b = atoi(argv[2]);
  int c = atoi(argv[3]);
  int d = atoi(argv[4]);
  
  if (argc < 5) {
    return usage();
  }

  // the hypergeometric probability (the probability of observing your table,
  // given the row and column sums.
  printf("%e\n", fisher(a, b, c, d));

  return 0;
}
