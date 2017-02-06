#!/bin/bash

javac MyFileReader.java
javac MyFileWriter.java
javac MyGaussianPdf.java
javac MCsim.java

java MCsim

python3 MyPlot.py mc_trial.txt &
python3 MyPlot.py tau_data.txt &

rm *.class
