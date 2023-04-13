""" Pure python examples of multiprocessing. 

We take a list of random integers and check which are multiple of primes for a selection of primes.

"""

import multiprocessing as mp
from multiprocessing import shared_memory
import resource

from typing import List
import numpy as np
import sys
import ray

# 2**23 about 1 sec on 2.6GHz Intel Core i7 12Gen per prime
LIST_INT_SIZE = 2**23
MAX_INT = sys.maxsize

# keeping one core free in case get bored
NR_PROC = mp.cpu_count() - 1

FIRST_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

PRIMES = FIRST_PRIMES[:NR_PROC]

# list of random integers with length of MAX_INT
np.random.seed(42)
LIST_INT = np.random.randint(low=1, high=MAX_INT, size=LIST_INT_SIZE)


# @ray.remote
def find_nr_multiple_of(number: int, int_list: List[int]):
    """Find how many entries in int_list are multiple of number."""
    return len([i for i in int_list if i % number == 0])


def run_with_one_proc(numbers: List[int], int_list: List[int]):
    """Check how many entries in int_list are multiple for each number in numbers."""

    print(
        f"Running with single processor for {len(int_list)} random integers for {len(numbers)} primes."
    )
    return {nr: find_nr_multiple_of(nr, int_list) for nr in numbers}


def run_with_all_processors(numbers: List[int], int_list: List[int], nr_proc: int):
    """Run with all processors."""

    print(
        f"Running with {nr_proc} processor for {len(int_list)} random integers for {len(numbers)} primes (memory_copy)."
    )
    with mp.Pool(processes=nr_proc) as pool:
        # We use .copy() here to simulate the case where the list is not shared between processes.
        # This is (was?) the case when using multiprocessing in Windows.
        # In Unix like system, a fork is using copy-on-write, so the list is not copied by default.
        # Thus, removing the copy() here and the shared memory example are equivalent.
        nr_multiples = pool.starmap(
            find_nr_multiple_of, [(nr, int_list.copy()) for nr in numbers]
            # find_nr_multiple_of, [(nr, int_list) for nr in numbers]
        )
    return {nr: nr_multiples[i] for i, nr in enumerate(numbers)}

#
def find_nr_multiple_of_in_shared_memory(
    number: int, shared_name: str, int_list_shape: tuple, int_list_dtype: str
):
    """Find how many entries in int_list are multiple of number."""
    shared_block = shared_memory.SharedMemory(create=False, name=shared_name)
    int_list = np.ndarray(int_list_shape, dtype=int_list_dtype, buffer=shared_block.buf)
    res = len([i for i in int_list if i % number == 0])
    shared_block.close()
    return res


def run_with_all_processors_shared_memory(
    numbers: List[int], int_list: List[int], nr_proc: int
):
    """Run with all processors and shared memory"""
    print(
        f"Running with {nr_proc} processor for {len(int_list)} random integers for {len(numbers)} primes (shared_memory)."
    )
    shared_block = shared_memory.SharedMemory(
        create=True, size=int_list.nbytes, name="mp_list_share"
    )

    shared_int_list = np.ndarray(
        int_list.shape, dtype=int_list.dtype, buffer=shared_block.buf
    )
    shared_int_list[:] = int_list[:]
    with mp.Pool(processes=nr_proc) as pool:
        res_handler = dict()
        for nr in numbers:
            res_handler[nr] = pool.apply_async(
                find_nr_multiple_of_in_shared_memory,
                kwds={
                    "number": nr,
                    "shared_name": shared_block.name,
                    "int_list_shape": shared_int_list.shape,
                    "int_list_dtype": shared_int_list.dtype,
                },
            )

        res_dict = {nr: res_handler[nr].get() for nr in numbers}
    shared_block.close()
    shared_block.unlink()

    return res_dict

#
# def run_with_ray(numbers: List[int], int_list: List[int]):
#     """Run with ray."""
#     ray.init(ignore_reinit_error=True)
#     int_list_obj_ref = ray.put(int_list)
#     nr_multiples = ray.get(
#         [find_nr_multiple_of.remote(nr, int_list_obj_ref) for nr in numbers]
#     )
#     ray.shutdown()
#     return {nr: nr_multiples[i] for i, nr in enumerate(numbers)}
#




result = run_with_one_proc(PRIMES, LIST_INT)
# result = run_with_all_processors(PRIMES, LIST_INT, NR_PROC)
# result = run_with_all_processors_shared_memory(PRIMES, LIST_INT, NR_PROC)

# result = run_with_ray(PRIMES, LIST_INT)

print(f"Result: {result}")

print(
    f"Maximum used memory: Main {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 } MB\n"
    f"Maximum used memory: Children {resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024 } MB"
)
print(f"User time: {resource.getrusage(resource.RUSAGE_SELF).ru_utime} s")
print(f"System time: {resource.getrusage(resource.RUSAGE_SELF).ru_stime} s")
