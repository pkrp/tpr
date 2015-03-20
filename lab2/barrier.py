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

t_start = MPI.Wtime()

do_some_operation()
print "M1 %d %f" %(comm.rank, (MPI.Wtime() - t_start));
comm.Barrier()
print "B1 %d %f" %(comm.rank, (MPI.Wtime() - t_start));

do_some_operation()
print "M2 %d %f" %(comm.rank, (MPI.Wtime() - t_start));
comm.Barrier()
print "B2 %d %f" %(comm.rank, MPI.Wtime() - t_start);

do_some_operation()
print "M3 %d %f" %(comm.rank, (MPI.Wtime() - t_start));
comm.Barrier()
print "B3 %d %f" %(comm.rank, (MPI.Wtime() - t_start));

MPI.Finalize()