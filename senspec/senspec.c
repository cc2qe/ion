#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>

int usage()
{
  fprintf(stderr,
	  "usage: senspec [options] <TP> <TN> <FP> <FN>\n\n"
          "author: Colby Chiang (cc2qe@virginia.edu)\n"
          "description: Calculates classification performance\n"
          "  for a 2x2 contingency table.\n"
          "   _________\n"
          "  | TP | FP |\n"
          "  |____|____|\n"
          "  | FN | TN |\n"
          "  |____|____|\n\n"
          "positional arguments:\n"
          "  TP, FP, FN, TN         observed values in the\n"
	  "                           2x2 contingency table\n"
	  "                           (true pos, false pos,\n"
	  "                           false neg, true neg)\n"
          "\n"
          "optional arguments:\n"
          "  -h                     show this help and exit\n"
	  "  -d                     show detailed definitions\n"
          "\n"
          );
  return 1;
}

int definitions()
{
  fprintf(stderr,
	  "\n"
          "   __________\n"
          "  | TP | FP |\n"
          "  |____|____|\n"
          "  | FN | TN |\n"
          "  |____|____|\n"
	  "\n"
	  "true positive               TP\n"
	  "  syn: hit\n"
	  "true negative               TN\n"
	  "false positive              FP\n"
	  "  syn: type I error\n"
	  "false negative              FN\n"
	  "  syn: type II error\n"
	  "sensitivity                 TP / (TP + FN)\n"
	  "  syn: true positive\n"
	  "    rate (TPR), power, recall\n"
	  "specificity                 TN / N = TN / (FP + TN)\n"
	  "type I error rate           FP / (FP + TN) = 1 - specificity\n"
	  "  syn: alpha, FPR\n"
	  "type II error rate          FN / (TP + FN) = 1 - sensitivity\n"
	  "  syn: beta, FNR\n"
	  "positive predictive value   TP / (TP + FP)\n"
	  "  syn: precision\n"
	  "negative predictive value   TN / (TN + FN)\n"
	  "false discovery rate (FDR)  FP / (FP + TP)\n"
	  "accuracy                    (TP + TN) / (TP + TN + FP + FN)\n"
	  "\n"
	  "\n"
	  );
  return 0;
}

int main (int argc, char **argv)
{
  // parse the optional arguments
  int i;
  while ((i = getopt(argc, argv, "hd")) != -1) {
    switch (i) {
    case 'h':
      return usage();
    case 'd':
      return definitions();
    }
  }


  // input control
  if (argc != 5) {
    return usage();
  }

  // parse the positional arguments
  double TP = atof(argv[1]);
  double FP = atof(argv[2]);
  double FN = atof(argv[3]);
  double TN = atof(argv[4]);

  // initialize the outputs
  double true_pos_rate; // (sensitivity)
  double true_neg_rate;// (specificity)
  double false_pos_rate; // (type I error, alpha)
  double false_neg_rate; // (type II error, beta)

  // calculate the outputs
  true_pos_rate = TP / (TP + FN);
  true_neg_rate= TN / (FP + TN);
  false_pos_rate = 1 - true_neg_rate;
  false_neg_rate = 1 - true_pos_rate;

  printf("a: %f, b: %f, c %f, d %f\n", TP, FP, FN, TN);


  // print output
  printf("sensitivity (true pos rate): %f\n", true_pos_rate);
  printf("specificity (true neg rate): %f\n", true_neg_rate);
  printf("type I error (false pos rate): %f\n", false_pos_rate);
  printf("type II error (false neg rage): %f\n", false_neg_rate);
  

  //printf("%e\n", fisher(a, b, c, d));

  return 0;
}
