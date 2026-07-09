# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 22:26:55 2026

@author: ma6
"""


import numpy as np
from scipy.linalg import solve_banded


def thomas_algorithm(lower, diag, upper, rhs):
    n = len(diag)
    if n != len(lower) or n != len(upper) or n != len(rhs):
        raise ValueError("lower, diag, upper, and rhs must have the same length.")
    
    a = lower.copy()
    b = diag.copy()
    c = upper.copy()
    d = rhs.copy()
    
    for i in range(1, n):
        m = a[i] / b[i-1]
        b[i] -= m * c[i-1]
        d[i] -= m * d[i-1]
        
    x = np.zeros(n)
    x[-1] = d[-1] / b[-1]
    
    for i in range(n-2, -1, -1):
        x[i] = (d[i] - c[i]*x[i+1]) / b[i]
        
    return x

def solve_tridiagonal_banded(lower, diag, upper, rhs):
    n = len(diag)
    if n != len(lower) or n != len(upper) or n != len(rhs):
        raise ValueError("lower, diag, upper, and rhs must have the same length.")
    
    ab = np.zeros([3, n])
    ab[0,1:] = upper[:-1]
    ab[1,:] = diag
    ab[2, :-1] = lower[1:]
    
    return solve_banded((1,1), ab, rhs)



def solve_tridiagonal(lower, diag, upper, rhs, method='thomas'):
    if method == 'thomas':
        return thomas_algorithm(lower, diag, upper, rhs)
    elif method == 'scipy':
        return solve_tridiagonal_banded(lower, diag, upper, rhs)
    else:
        raise ValueError("method must be 'thomas' or 'scipy'.")






        










