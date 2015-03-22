#!/bin/bash
module load libs/boost/1.52.0
module load libs/openblas/0.2.6
module load ruby/2.0.0-p247

pip install --user mpi4py

NOW=$(date "+%F_%T")

mkdir $NOW
cp bcast.py ./$NOW
cd $NOW

chmod +x ./bcast.py

BYTESAMOUNT="1000 2000 3000 4000 5000 7500 10000 12500 15000 20000 25000 30000 40000 50000 75000 100000 140000 180000 240000 300000 350000 400000 450000 500000 600000 700000 800000 900000 1000000"

for BYTES in $BYTESAMOUNT
do
        mpiexec -n 3 ./bcast.py 0 $BYTES >> BCAST30.txt
        mpiexec -n 3 ./bcast.py 1 $BYTES >> BCAST31.txt
        mpiexec -n 3 ./bcast.py 2 $BYTES >> BCAST32.txt
        mpiexec -n 6 ./bcast.py 0 $BYTES >> BCAST60.txt
        mpiexec -n 6 ./bcast.py 1 $BYTES >> BCAST61.txt
        mpiexec -n 6 ./bcast.py 2 $BYTES >> BCAST62.txt
        mpiexec -n 9 ./bcast.py 0 $BYTES >> BCAST90.txt
        mpiexec -n 9 ./bcast.py 1 $BYTES >> BCAST91.txt
        mpiexec -n 9 ./bcast.py 2 $BYTES >> BCAST92.txt
done