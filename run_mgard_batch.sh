#! /bin/bash

file="mgard.log"
rm $file
touch $file
for e in 1e16 5e15 1e15 5e14 1e14 5e13 1e13 5e12 1e12
do
	echo "absolute error = $e" >> $file
	/Users/x0o/github/MGARDx/build/test/test_compress xgc_f64.dat 1 $e 3 0 3 131160 39 39 >> $file
	/Users/x0o/github/MGARDx/build/test/test_decompress xgc_f64.dat xgc_f64.dat.mgard 1 3 131160 39 39 >> $file
	python3 xgc_evaluate.py xgc_f64.dat.mgard.out >> $file
done

scaling_factor=`grep "scaling factor" $file | head -n 1 | grep -o [0-9][0-9]*\.[0-9][0-9]*`
mv $file "mgard_"$scaling_factor".log"

