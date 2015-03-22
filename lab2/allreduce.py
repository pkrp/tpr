#!/usr/bin/env python

from mpi4py import MPI
from threading import Thread
import numpy as np
import sys
 
def bcast_tree(data, root, comm):
	rank = comm.Get_rank()
	size = comm.Get_size()
	
	dest1 = 2 * rank + 1
	dest2 = 2 * rank + 2
	
	sends_me = (rank - 1) / 2
	
	if(rank != root):
		comm.Recv([data, MPI.BYTE], source=sends_me)
		
	if (dest1 < size): 
		comm.Send([data, MPI.BYTE], dest=dest1)
	if (dest2 < size): 
		comm.Send([data, MPI.BYTE], dest=dest2)
		
def reduce_data(data1, data2, result, operation):
	data2 = np.add(data1, data2)	
		
def my_reduce(data, result, operation, comm):
	rank = comm.Get_rank()
	size = comm.Get_size()	

	source1 = 2 * rank + 1
	source2 = 2 * rank + 2
	
	destination = (rank - 1) / 2
	
	result1 = [0 for i in range(len(data))]
	result2 = [0 for i in range(len(data))] 

	reduce1 = source1 < size
	reduce2 = source2 < size
	
	if reduce1: 
		comm.Recv([result1, MPI.INT], source=source1)
	if reduce2:
		comm.Recv([result2, MPI.INT], source=source2)
		
	if reduce1 & reduce2:
		reduce_data(result1, result2, operation)
		reduce_data(data, result2, operation)
	elif reduce1:
		reduce_data(data, result1, operation)
		result2 = result1
	elif reduce2:
		reduce_data(data, result2, operation)
	else:
		result2 = data
		
	if rank != root:
		comm.Send([result2, MPI.INT], dest=destination)
	else:
		result = result2
		
def my_allreduce(data, result, operation, root, comm):
	root = 0
	my_reduce(data, result, operation, comm)
	my_bcast_tree(result, root, comm)
	
def mpi_allreduce(data, result, operation, root, comm):
	comm.allreduce(data, result, op=operation)

get_arg = lambda n, default: int(sys.argv[n]) if n < len(sys.argv) else default
 
type = get_arg(1, 0) 		# 0: mpi allreduce, 1: my allreduce
size = get_arg(1, 10) 		

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
world = comm.Get_size()
root = 0
data = [i for i in range(size)]
result = [0 for i in range(size)] 

if type == 1:
	my_allreduce = my_allreduce
else:
	my_allreduce = mpi_allreduce

	my_allreduce_time = 0.0

for i in range(100):
	t_start = MPI.Wtime()
	my_allreduce(data, result, MPI.SUM, root, comm)
	my_allreduce_time += MPI.Wtime() - t_start
	comm.Barrier()

if rank == 0:
	print("%f" % (my_allreduce_time/100.0)	)
	
MPI.Finalize()
