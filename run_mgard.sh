#! /bin/bash

/Users/x0o/github/MGARDx/build/test/test_compress xgc_f64.dat 1 $1 3 0 3 131160 39 39
/Users/x0o/github/MGARDx/build/test/test_decompress xgc_f64.dat xgc_f64.dat.mgard 1 3 131160 39 39
python3 xgc_evaluate.py xgc_f64.dat.mgard.out 
