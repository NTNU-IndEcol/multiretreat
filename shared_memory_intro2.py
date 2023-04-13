""" Small intro to introduce shared memory in Python. 

Script to run on interpreter 2

"""

from multiprocessing import shared_memory
import numpy as np

# attach to the shared memory block
shared_block2 = shared_memory.SharedMemory(create=False, name="shared_memory")

# make a numpy array from the shared memory block
intp2 = np.ndarray(shape=(10,), dtype="int64", buffer=shared_block2.buf)

# print the array
print(f"Array: {intp2}")

# shared_block2.close()
