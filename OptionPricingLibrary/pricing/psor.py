# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:36:25 2026

@author: ma6
"""
'''
Projected Successive Over-Relaxation

The thomas algorithm and SciPy solve linear equation set for every step,
and then take max(V_inner, payoff)

However, after the V_inner is replaced by payoff values, the adjacent values should also
be affected, because each equation in the set is composed of three adjacent grid points.

PSOR takes max(V_inner, payoff) in every step and iterate until convergence,
by which considering the affect of max(V_inner, payoff) to adjacent grid points.

PSOR
x >= payoff
A x > rhs
(x - payoff) * (A x - rhs) = 0
'''
import numpy as np

def psor_solve_tridiagonal(
        lower,
        diag,
        upper,
        rhs,
        payoff,
        initial_guess = None,
        omega = 1.2,
        tol = 1e-8,
        max_iter = 10000
        ):
    
    lower = np.asarray(lower, dtype = float)
    diag = np.asarray(diag, dtype = float)
    upper = np.asarray(upper, dtype = float)
    rhs = np.asarray(rhs, dtype = float)
    payoff = np.asarray(payoff, dtype = float)
    
    n = len(rhs)
    
    if lower.shape != (n,):
        raise ValueError('lower must be the same length as rhs.')
    
    if diag.shape != (n,):
        raise ValueError('diag must have the same length as rhs.')
        
    if upper.shape != (n,):
        raise ValueError('upper must have the same length as rhs.')
    
    if payoff.shape != (n,):
        raise ValueError('payoff must have the same length as rhs.')
        
    if np.any(diag == 0):
        raise ValueError('diag must not contain zero entries.')
        
    if not (0.0 < omega < 2.0):
        raise ValueError('omega should satisfy 0 < omega < 2.')
    
    if tol <= 0:
        raise ValueError('tol must be positive.')
    
    if max_iter <= 0:
        raise ValueError('max_iter must be positive.')
    
    if initial_guess is None:
        x = np.maximum(rhs.copy(), payoff)
    else:
        x = np.asarray(initial_guess, dtype=float).copy()
        
        if x.shape != (n,):
            raise ValueError('initial_guess must have the same length as rhs.')
            
        x = np.maximum(x, payoff)
        
    for iteration in range(max_iter):
        
        x_old = x.copy()
        
        for i in range(n):
            if i == 0:
                lower_term = 0.0
            else:
                lower_term = lower[i] * x[i-1]
            
            if i == n-1:
                upper_term = 0.0
            else:
                upper_term = upper[i]*x_old[i+1]
            
            x_gs = (rhs[i] - lower_term - upper_term) / diag[i]
            
            x_sor = x[i] + omega * (x_gs - x[i])
            
            x[i] = max(payoff[i], x_sor)
            
        error = np.max(np.abs(x - x_old))
        
        if error < tol:
            return x, iteration +1, True
    
    return x, max_iter, False
        
    
    
    




