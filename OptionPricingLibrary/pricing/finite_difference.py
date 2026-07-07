# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 12:32:35 2026

@author: ma6
"""

#pricing/finite_difference.py

import numpy as np

class ExplicitFiniteDifferenceEngine():
    
    def __init__(self, s_max = 300, n_s = 200, n_t = 2*10**4):
        self.s_max = s_max
        self.n_s= n_s
        self.n_t = n_t
        
    def price_loop(self, option, market):# slow version based on for loop
        S0 = option.spot
        K = option.strike
        T = option.tau
        option_type = option.option_type
        
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        dS = self.s_max / self.n_s
        dt = T / self.n_t
        
        S_grid = np.linspace(0.0, self.s_max, self.n_s + 1)
        
        #boundary condition at tau = 0
        if option_type == 'Call':
            V = np.maximum(S_grid - K, 0.0)
        elif option_type == 'Put':
            V = np.maximum(K - S_grid, 0.0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
            
        
        #reverse time stepping
        for step in range(self.n_t):
            tau = dt * (step + 1)
            
            V_old = V.copy()
            
            #boundary condition at two sides of S
            if option_type == 'Call':
                V[0] = 0.0
                V[-1] = self.s_max * np.exp(-y*tau) - K*np.exp(-r*tau)
            else:
                V[0] = K*np.exp(-r*tau)
                V[-1] = 0.0
                
            for i in range(1, self.n_s):
                delta = (V_old[i+1] - V_old[i-1])/ (2*dS)
                gamma = (V_old[i+1] - 2*V_old[i] + V_old[i-1]) / (dS**2)
                
                theta_forward = (
                    0.5*sigma**2 * S_grid[i]**2 * gamma
                    + (r - y) * S_grid[i] * delta
                    - r*V_old[i]
                    )
                
                V[i] = V_old[i] + dt * theta_forward
                
            
        price = np.interp(S0, S_grid, V)
            
        return price
    
    
    
    def price(self, option, market):
        S0 = option.spot
        K = option.strike
        T = option.tau
        option_type = option.option_type
        
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        dS = self.s_max / self.n_s
        dt = T / self.n_t
        
        max_i = self.n_s
        stability_ratio = dt*sigma**2 * max_i**2
        
        if stability_ratio > 0.5:
            raise ValueError(
                "Explicit finite difference scheme may be unstable."
                "Increase n_t or decrease n_s."
                f"Current dt*sigma**2 * n_s**2 = {stability_ratio:.10f}"
                )
        
        S_grid = np.linspace(0.0, self.s_max, self.n_s + 1)
        
        #boundary condition at tau = 0
        if option_type == 'Call':
            V = np.maximum(S_grid - K, 0.0)
        elif option_type == 'Put':
            V = np.maximum(K - S_grid, 0.0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
            
        #reverse time stepping
        i = np.arange(1, self.n_s)
        S_inner = S_grid[i]
        
        for step in range(self.n_t):
            tau = dt * (step + 1)
            V_old = V.copy()
            
            if option_type == 'Call':
                V[0] = 0.0
                V[-1] = self.s_max * np.exp(-y*tau) - K*np.exp(-r*tau)
            else:
                V[0] = K*np.exp(-r*tau)
                V[-1] = 0.0
                
            delta = (V_old[i+1] - V_old[i-1])/ (2*dS)
            gamma = (V_old[i+1] - 2*V_old[i] + V_old[i-1]) / (dS**2)
            theta_forward = (
                0.5*sigma**2 * S_inner**2 * gamma
                + (r - y) * S_grid[i] * delta
                - r*V_old[i]
                )
            V[i] = V_old[i] + dt * theta_forward
        
        
        price = np.interp(S0, S_grid, V)
        return price
        
        
        
        
class ImplicitFiniteDifferenceEngine:
    def __init__(self, s_max = 300.0, n_s= 200, n_t = 500):
        self.s_max = s_max
        self.n_s = n_s
        self.n_t = n_t
        
        
    def price(self, option, market):
        S0 = option.spot
        K = option.strike
        T = option.tau
        option_type = option.option_type
        
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        dS = self.s_max / self.n_s
        dt = T / self.n_t
        
        S_grid = np.linspace(0.0, self.s_max, self.n_s + 1)
        
        #boundary condition at tau = 0
        if option_type == 'Call':
            V = np.maximum(S_grid - K, 0)
        elif option_type == 'Put':
            V = np.maximum(K - S_grid, 0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
            
        #vectorize
        i = np.arange(1, self.n_s)
        S_inner = S_grid[i]
        
        A = 0.5*sigma**2 * S_inner**2
        B = (r - y)*S_inner
        
        lower = - dt*(A/dS **2 - B /(2*dS))
        diag = 1.0 + dt*(2*A/dS**2 + r)
        upper = -dt*(A/dS**2 + B/(2*dS))
        
        #tridiagonal matrix
        M = np.zeros((self.n_s - 1, self.n_s - 1))
        np.fill_diagonal(M, diag)
        np.fill_diagonal(M[1:], lower[1:])
        np.fill_diagonal(M[:,1:], upper[:-1])
        
        for step in range(self.n_t):
            tau = (step + 1) * dt
            
            #boundary condition at the to sides of S
            if option_type == 'Call':
                leftB = 0.0
                rightB = self.s_max * np.exp(-y*tau) - K*np.exp(-r*tau)
            else:
                leftB = K*np.exp(-r*tau)
                rightB = 0.0
                
            rhs = V[1:-1].copy()             #The matrix did not include V0 and V_n_s. The boudanry here need to be corrected
            rhs[0] -= lower[0] * leftB       #Otherwise, the first row is b_1 * V_1 + c_1 * V_2 = V_1_old
            rhs[-1] -= upper[-1] * rightB    #But it supposed to be a_1 * V_0 + b_1 * V_1 + c_1 * V_2 = V_1_old
                                             #The rhs is corrected as V_1_old - a_1*V_0. The same for V_n_1
            V_inner_new = np.linalg.solve(M, rhs)
            
            V[0] = leftB
            V[-1] = rightB
            V[1:-1] = V_inner_new
            
        price = np.interp(S0, S_grid, V)
        return price
                
        
        

class CrankNicolsonFiniteDifferenceEngine():
    
    def __init__(self, s_max = 300, n_s = 200, n_t = 500):
        self.s_max = s_max
        self.n_s = n_s
        self.n_t = n_t
        
    def price(self, option, market):
        S0 = option.spot
        K = option.strike
        T = option.tau
        option_type = option.option_type
        
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        dS = self.s_max / self.n_s
        dt = T / self.n_t
        S_grid = np.linspace(0.0, self.s_max, self.n_s + 1)
        
        #boundary condition at tau = 0
        if option_type == 'Call':
            V = np.maximum(S_grid - K, 0)
        elif option_type == 'Put':
            V = np.maximum(K - S_grid, 0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
            
        #vectorize S
        i = np.arange(1, self.n_s)
        S_inner = S_grid[i]
        
        A = 0.5*sigma**2 * S_inner**2
        B = (r - y)*S_inner
        
        #operator L coefficients
        L_lower = A / dS**2 - B / (2.0 * dS)
        L_diag = -2.0 * A / dS**2 - r
        L_upper = A / dS**2 + B / (2.0 * dS)
        
        #left hand side: I + 0.5*dt*L
        lhs_lower = -0.5*dt*L_lower
        lhs_diag = 1.0 - 0.5*dt*L_diag
        lhs_upper = -0.5 *dt*L_upper
        
        #righr hand side: I + 0.5* dt*L
        rhs_lower = 0.5*dt*L_lower
        rhs_diag = 1.0 + 0.5*dt*L_diag
        rhs_upper = 0.5*dt*L_upper
        
        #left hand side matrix
        M_left = np.zeros((self.n_s-1, self.n_s-1))
        np.fill_diagonal(M_left, lhs_diag)
        np.fill_diagonal(M_left[1:], lhs_lower[1:])
        np.fill_diagonal(M_left[:,1:], lhs_upper[:-1])
        
        #rigth hand side matrix
        M_right = np.zeros((self.n_s - 1, self.n_s - 1))
        np.fill_diagonal(M_right, rhs_diag)
        np.fill_diagonal(M_right[1:], rhs_lower[1:])
        np.fill_diagonal(M_right[:,1:], rhs_upper[:-1])
        
        for step in range(self.n_t):
            tau_old = step*dt
            tau_new = (step + 1)*dt
            
            #old boundary condition
            if option_type == 'Call':
                left_old = 0.0
                right_old = self.s_max * np.exp(-y*tau_old) - K*np.exp(-r*tau_old)
                
                left_new = 0.0
                right_new = self.s_max*np.exp(-y*tau_new) - K*np.exp(-r*tau_new)
                
            else:
                left_old = K*np.exp(-r*tau_old)
                right_old = 0.0
                
                left_new = K*np.exp(-r*tau_new)
                right_new = 0.0
                
            #rhs from old interior values
            rhs = M_right @ V[1:-1]
            
            rhs[0] += rhs_lower[0] * left_old
            rhs[-1] += rhs_upper[-1] * right_old
            
            rhs[0] -= lhs_lower[0]*left_new
            rhs[-1] -= lhs_upper[-1]*right_new
            
            V_inner_new = np.linalg.solve(M_left, rhs)
            
            V[0] = left_new
            V[-1] = right_new
            V[1:-1] = V_inner_new
            
        price = np.interp(S0, S_grid, V)
        return price
                
                
            
        
        
class AmericanPutImplicitFiniteDifferenceEngine():
    def __init__(self, s_max = 300, n_s = 200, n_t = 500):
        self.s_max = s_max
        self.n_s = n_s
        self.n_t = n_t
        
    def price(self, option, market):
        S0 = option.spot
        K = option.strike
        T = option.tau
        option_type = option.option_type
        if option_type != 'Put':
            raise ValueError("option_type must be 'Put' in AmericanPutImplicitFiniteDifferenceEngine.")
        
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        dS = self.s_max / self.n_s
        dt = T / self.n_t
        
        S_grid = np.linspace(0.0, self.s_max, self.n_s + 1)
        
        #boundary condition at tau = 0
        V = np.maximum(K - S_grid, 0)
        
        #grid points in S space
        i = np.arange(1, self.n_s)
        S_inner = S_grid[i]
        
        A = 0.5*sigma**2 * S_inner**2
        B = (r - y)*S_inner
        
        lower = -dt*(A/dS**2 - B/(2*dS))
        diag = 1 + dt*(2 * A/dS**2 + r)
        upper = -dt*(A/dS**2 + B/(2*dS))
        
        #tridiagonal matrix
        M = np.zeros((self.n_s - 1, self.n_s - 1))
        np.fill_diagonal(M, diag)
        np.fill_diagonal(M[1:], lower[1:])
        np.fill_diagonal(M[:,1:], upper[:-1])
        
        #immediate exercise value for S grid points
        exercise_inner = np.maximum(K - S_inner, 0.0)
        
        for step in range(self.n_t):
            #tau = (step + 1)*dt
            
            #boundary condition at two sides of S
            leftB = K
            rightB = 0.0
            
            rhs = V[1:-1].copy()
            
            #boundary condition
            rhs[0] -= lower[0] * leftB
            rhs[-1] -= upper[-1] * rightB
            
            #continuation value from implicit computation
            continuation_inner = np.linalg.solve(M, rhs)
            
            #correct V value by exercise value vs continuation value
            V_inner_new = np.maximum(continuation_inner, exercise_inner)
            
            V[0] = leftB
            V[-1] = rightB
            V[1:-1] = V_inner_new
            
        price = np.interp(S0, S_grid, V)
        return price
            
            
        
        
        
class AmericanPutCrankNicolsonFiniteDifferenceEngine():
    
    def __init__(self, s_max = 300, n_s = 200, n_t = 500):
        self.s_max = s_max
        self.n_s = n_s
        self.n_t = n_t
        
    def price(self, option, market):
        S0 = option.spot
        K = option.strike
        T = option.tau
        option_type = option.option_type
        
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        dS = self.s_max / self.n_s
        dt = T / self.n_t
        S_grid = np.linspace(0.0, self.s_max, self.n_s + 1)
        
        #boundary condition at tau = 0
        if option_type == 'Put':
            V = np.maximum(K - S_grid, 0)
        else:
            raise ValueError("option_type must be 'Put'.")
            
        #vectorize S
        i = np.arange(1, self.n_s)
        S_inner = S_grid[i]
        
        A = 0.5*sigma**2 * S_inner**2
        B = (r - y)*S_inner
        
        #operator L coefficients
        L_lower = A / dS**2 - B / (2.0 * dS)
        L_diag = -2.0 * A / dS**2 - r
        L_upper = A / dS**2 + B / (2.0 * dS)
        
        #left hand side: I + 0.5*dt*L
        lhs_lower = -0.5*dt*L_lower
        lhs_diag = 1.0 - 0.5*dt*L_diag
        lhs_upper = -0.5 *dt*L_upper
        
        #righr hand side: I + 0.5* dt*L
        rhs_lower = 0.5*dt*L_lower
        rhs_diag = 1.0 + 0.5*dt*L_diag
        rhs_upper = 0.5*dt*L_upper
        
        #left hand side matrix
        M_left = np.zeros((self.n_s-1, self.n_s-1))
        np.fill_diagonal(M_left, lhs_diag)
        np.fill_diagonal(M_left[1:], lhs_lower[1:])
        np.fill_diagonal(M_left[:,1:], lhs_upper[:-1])
        
        #rigth hand side matrix
        M_right = np.zeros((self.n_s - 1, self.n_s - 1))
        np.fill_diagonal(M_right, rhs_diag)
        np.fill_diagonal(M_right[1:], rhs_lower[1:])
        np.fill_diagonal(M_right[:,1:], rhs_upper[:-1])
        
        exercise_inner = np.maximum(K - S_inner, 0.0)
        for step in range(self.n_t):
            #tau_old = step*dt
            #tau_new = (step + 1)*dt
            
            #old boundary condition
            left_old = K
            right_old = 0.0
            
            left_new = K
            right_new = 0.0
                
            #rhs from old interior values
            rhs = M_right @ V[1:-1]
            
            rhs[0] += rhs_lower[0] * left_old
            rhs[-1] += rhs_upper[-1] * right_old
            
            rhs[0] -= lhs_lower[0]*left_new
            rhs[-1] -= lhs_upper[-1]*right_new
            
            V_continuation_inner = np.linalg.solve(M_left, rhs)
            V_inner_new = np.maximum(exercise_inner, V_continuation_inner)
            
            V[0] = left_new
            V[-1] = right_new
            V[1:-1] = V_inner_new
            
        price = np.interp(S0, S_grid, V)
        return price
        
        
        
        
        
        
        