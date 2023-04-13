""" Small intro to introduce shared memory in Python. 

Script to run on interpreter 1

"""

from multiprocessing import shared_memory
import numpy as np

# random list of integers
rand_list = np.random.randint(low=1, high=100, size=10)

# create shared memory block with the size of rand_list
shared_block1 = shared_memory.SharedMemory(
    create=True, size=rand_list.nbytes, name="shared_memory"
)

# make a numpy array from the shared memory block
intp1 = np.ndarray(rand_list.shape, dtype=rand_list.dtype, buffer=shared_block1.buf)

# copy the data from rand_list to the shared memory block
intp1[:] = rand_list[:]

# get the parameters of the shared memory block and array
print(
    f"Shared memory block name: {shared_block1.name}, Size: {shared_block1.size}, Shape: {intp1.shape}, Dtype: {intp1.dtype}"
)

print(f"Array: {intp1}")

# shared_block1.close()
# shared_block1.unlink()
