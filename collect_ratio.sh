#/bin/bash

grep ratio $1 | grep -o [0-9][0-9]*\.[0-9][0-9]*

