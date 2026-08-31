# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 21:56:35 2026

@author: ma6
"""

import os
os.chdir('..')

import numpy as np
from pricing.psor import psor_solve_tridiagonal

def test_psor_no_exercise_matches_linear_solve():
    # this test assumes no early exercise
    lower = np.array([0.0, -1.0, -1.0])
    diag = np.array([4.0, 4.0, 4.0])
    upper = np.array([-1.0, -1.0, 0.0])
    rhs = np.array([1.0, 2.0, 3.0])
    
    payoff = np.array([-100.0, -100.0, -100.0])
    
    x_psor, num_iter, converged = psor_solve_tridiagonal(
        lower = lower,
        diag = diag,
        upper = upper,
        rhs = rhs,
        payoff = payoff,
        omega = 1.2,
        tol = 1e-10,
        max_iter = 10000
        )
    
    A = np.array([
        [4.0, -1.0, 0.0],
        [-1.0, 4.0, -1.0],
        [0.0, -1.0, 4.0]
        ])
    
    x_exact = np.linalg.solve(A, rhs)
    
    assert converged
    assert np.max(np.abs(x_psor - x_exact)) < 1e-8
    

def test_psor_solution_respects_payoff():
    lower = np.array([0.0, -1.0, -1.0])
    diag = np.array([4.0, 4.0, 4.0])
    upper = np.array([-1.0, -1.0, 0.0])
    rhs = np.array([1.0, 2.0, 3.0])
    
    payoff = np.array([0.0, 1.0, 2.0])
    
    x, num_iter, converged = psor_solve_tridiagonal(
        lower = lower,
        diag = diag,
        upper = upper,
        rhs = rhs,
        payoff = payoff,
        omega = 1.2,
        tol = 1e-10,
        max_iter = 10000
        )
    
    assert converged
    assert np.all(x >= payoff)
    

def test_psor_complementarity_residual():
    
    lower = np.array([0.0, -1.0, -1.0])
    diag = np.array([4.0, 4.0, 4.0])
    upper = np.array([-1.0, -1.0, 0.0])
    rhs = np.array([1.0, 2.0, 3.0])
    
    payoff = np.array([0.0, 1.0, 2.0])
    
    x, num_iter, converged = psor_solve_tridiagonal(
    lower = lower,
    diag = diag,
    upper = upper,
    rhs = rhs,
    payoff = payoff,
    omega = 1.2,
    tol = 1e-10,
    max_iter = 10000
    )
    
    
    A = np.array([
        [4.0, -1.0, 0.0],
        [-1.0, 4.0, -1.0],
        [0.0, -1.0, 4.0]
        ])
    
    residual = A @ x - rhs
    complementarity = (x - payoff) * residual
    
    assert converged
    assert np.all(x >= payoff - 1e-10)
    assert np.all(residual >= -1e-8)
    assert np.max(np.abs(complementarity)) < 1e-7
    

if __name__ == "__main__":
    test_psor_no_exercise_matches_linear_solve()
    test_psor_solution_respects_payoff()
    test_psor_complementarity_residual()
    
    
    

