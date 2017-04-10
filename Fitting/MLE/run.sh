#!bin/bash

virtualenv -p python3 Fitting

. Fitting/bin/activate

pip3 install numpy
pip3 install scipy
pip3 install matplotlib

python3 run_dmc.py