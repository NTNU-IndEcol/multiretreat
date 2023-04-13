""" Example regarding multiprocessing in numpy

Simulated task: multiply a matrix with 5 other matrices of the same size

"""

import os
from pyinstrument import Profiler
import multiprocessing as mp


import numpy as np
from threadpoolctl import threadpool_limits, threadpool_info

# Instead of threadpool_limits, you can also use the following environment variables:
# os.environ["OPENBLAS_NUM_THREADS"] = "1"
# os.environ["MKL_NUM_THREADS"] = "1"
# os.environ["OMP_NUM_THREADS"] = "1"
# os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
# os.environ["NUMEXPR_NUM_THREADS"] = "1"


# 5k x 5k about 2 sec on 2.6GHz Intel Core i7 12Gen 12 core
MATRIX_SIZE = (3000, 3000)
# MATRIX_SIZE = (500, 500)


def build_matrix(original, n):
    """Build a new matrix from the original matrix"""
    return original * n


@threadpool_limits.wrap(limits=1, user_api="blas")
def multiply_matrices(a, b):
    """Multiply two matrices (numpy array)"""
    return a @ b


if __name__ == "__main__":
    nr_processes = mp.cpu_count() - 1

    print(f"Multiplying {nr_processes} matrixes of shape {MATRIX_SIZE}.")

    # print("\nSome information about the system as seen by numpy:")
    # print(np.show_config())
    # print(np.show_runtime())
    # print(threadpool_info())

    mat = np.random.rand(*MATRIX_SIZE)
    matrix_factors = [np.random.randint(1, 100) for _ in range(nr_processes)]

    print("\n\nSequential run start")

    with Profiler() as seq_prof:
        res_seq = [multiply_matrices(mat, build_matrix(mat, n)) for n in matrix_factors]

    print(seq_prof.output_text(unicode=True, color=True, timeline=True, show_all=True))

    print("Sequential run finished")

    # ------------------------------

    print("Multiprocessing run start")

    with Profiler() as multi_prof:
        with mp.Pool(processes=nr_processes) as pool:
            res_multi = pool.starmap(
                multiply_matrices, [(mat, build_matrix(mat, n)) for n in matrix_factors]
            )

    print(
        multi_prof.output_text(unicode=True, color=True, timeline=True, show_all=True)
    )

    print("Multiprocessing run finished")
