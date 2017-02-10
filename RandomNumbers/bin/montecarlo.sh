#!/bin/bash

javac MyFileReader.java
javac MyFileWriter.java
javac MyGaussianPdf.java
javac MCsim.java

var=$(java MCsim)

python3 MyPlotNormalised.py mc_trial.txt &
python3 MyPlot.py tau_data.txt $var &

rm *.class
