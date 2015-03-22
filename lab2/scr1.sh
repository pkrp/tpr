#!/bin/bash
module load libs/boost/1.52.0
module load libs/openblas/0.2.6
module load ruby/2.0.0-p247

pip install --user mpi4py

NOW=$(date "+%F_%T")

mkdir $NOW
cp barrier.py ./$NOW
cd $NOW

chmod +x ./barrier.py

mpiexec -n 3 ./barrier.py $BYTES >> BARRIER.txt
mpiexec -n 6 ./barrier.py $BYTES >> BARRIER.txt
mpiexec -n 9 ./barrier.py $BYTES >> BARRIER.txt