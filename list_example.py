""" Short example script for profiling list creation. 

Run from the command line with:

pyinstrument list_example.py

"""

import time


def make_list_comp(x):
    ll = [x**2 for x in range(x)]
    return ll

def make_list_for(x):
    lf = []
    for i in range(x):
        lf.append(i**2)
    return lf


def make_two_lists(x):
    clist = make_list_comp(x)
    flist = make_list_for(x)

if __name__ == "__main__":
    make_two_lists(2**21)

