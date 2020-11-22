#/bin/bash

grep $2 $1 | grep -o "error = .*," | grep -o [0-9].*[^,]


