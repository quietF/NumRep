#!/bin/bash

javac Function.java
javac Methods.java

plot="
reset;\n
p[-5:5] 10.2-7.4*x-2.1*x*x+x*x*x t \"f(x)\", 0 lc rgb 'black' t \"\";
"
echo -e $plot > gnp/plot.gnp

gnuplot --persist gnp/plot.gnp

g="
reset;\n
p[0:5] exp(x)-2 t \"g(x)\", 0 lc rgb 'black' t \"\";
"

echo -e $g > gnp/plot.gnp
gnuplot --persist gnp/plot.gnp



h="
reset;\n
p[-1:4] cos(x)*sin(3*x) t \"h(x)\", 0 lc rgb 'black' t \"\";
"

echo -e $h > gnp/plot.gnp
gnuplot --persist gnp/plot.gnp

java Methods
