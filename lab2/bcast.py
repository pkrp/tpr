#!/usr/bin/env python

from mpi4py import MPI
from threading import Thread
import numpy as np
import sys

def bcast_simple(data, root, comm):

        rank = comm.Get_rank()
        size = comm.Get_size()

        if(rank == root):
			for i in range(size):
					if(i != rank):
							comm.Send([data, MPI.BYTE], dest=i)
        else: comm.Recv([data, MPI.BYTE], source=root)

def bcast_tree(data, root, comm):

        rank = comm.Get_rank()
        size = comm.Get_size()

        dest1 = 2 * rank + 1
        dest2 = 2 * rank + 2

        sender = (rank - 1)/2

        if(rank != root):
                comm.Recv([data, MPI.BYTE], source=sender)
        if (dest1 < size):
                comm.Send([data, MPI.BYTE], dest=dest1)
        if (dest2 < size):
                comm.Send([data, MPI.BYTE], dest=dest2)

def mpi_bcast(data, root, comm):
        comm.Bcast([data, MPI.BYTE], root)

get_arg = lambda n, default: int(sys.argv[n]) if n < len(sys.argv) else default

type = get_arg(1, 0)            # 0: bcast, 1: simple, 2:  tree
size = get_arg(2, 10)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
world = comm.Get_size()
root = 0
data = np.zeros(size, dtype=np.dtype('i1'))

if type == 1:
        my_bcast = bcast_simple
elif type == 2:
        my_bcast = bcast_tree
else:
        my_bcast = mpi_bcast

my_bcast_time = 0.0

for i in range(10000):
        t_start = MPI.Wtime()
        my_bcast(data, root, comm)
        my_bcast_time += MPI.Wtime() - t_start
        comm.Barrier()

if rank == 0:
        print("%f" % (10e6 * my_bcast_time/(10000.0)))

MPI.Finalize()