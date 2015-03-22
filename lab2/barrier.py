#!/usr/bin/env python

from mpi4py import MPI
import numpy as np

def do_some_operation():
        X = np.zeros((10,10))
        Y = np.zeros((10,10))
        result = np.zeros((10,10))
        for i in range(len(X)):
                for j in range(len(Y[0])):
                        for k in range(len(Y)):
                                result[i][j] += X[i][k] * Y[k][j]
        return

comm = MPI.COMM_WORLD

result = 0.0
for i in range(200):
        t_start = MPI.Wtime()
        do_some_operation()
        t_end = (MPI.Wtime() - t_start);
        comm.Barrier()
        result += (MPI.Wtime() - t_start) - t_end
print "R1 %d %f" %(comm.rank, result/200.0);

result = 0.0
for i in range(200):
        t_start = MPI.Wtime()
        do_some_operation()
        t_end = (MPI.Wtime() - t_start);
        comm.Barrier()
        result += (MPI.Wtime() - t_start) - t_end
print "R2 %d %f" %(comm.rank, result/200.0);

result = 0.0
for i in range(200):
        t_start = MPI.Wtime()
        do_some_operation()
        t_end = (MPI.Wtime() - t_start);
        comm.Barrier()
        result += (MPI.Wtime() - t_start) - t_end
print "R3 %d %f" %(comm.rank, result/200.0);

MPI.Finalize()