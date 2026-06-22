# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 21:13:04 2026

@author: ma6
"""

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.monte_carlo import MonteCarloEngine
import matplotlib.pyplot as plt
import numpy as np



if __name__ == '__main__':
    call = EuropeanOption(
        spot = 100,
        strike = 110,
        tau = 0.5,
        option_type = 'Call'    
        )


    market = MarketData(
        rate = 0.04,
        dividend = 0.02,
        volatility = 0.25
        )


    bs_engine = BlackScholesEngine()

    n_path_list = [10**3, 5*10**3, 10**4, 5*10**4, 10**5, 5*10**5, 10**6, 5*10**6, 10**7]
    n_price = []
    n_std = []
    n_abs = []
    n_z = []

    bs_price = bs_engine.price(call, market)

    print('Monte Carlo Convergence test')
    print()

    print(f"Bench mark price for option:{bs_price:.10f}")
    print()

    print(
          f"{'n_paths':>15}"
          f"{'MC price':>15}"
          f"{'Std error':>15}"
          f"{'Abs error':>15}"
          f"{'z-score':>15}"
          )

    print('-' * 80)

    for paths in n_path_list:
        mc_engine = MonteCarloEngine(
            n_paths = paths,
            seed = 42,
            antithetic = True        
            )
        mc_price, mc_error = mc_engine.price_error(call, market)
        abs_error = abs(bs_price - mc_price)
        z_score = abs_error/mc_error
        n_price.append(mc_price)
        n_std.append(mc_error)
        n_abs.append(abs_error)
        n_z.append(z_score)
        print(
            f"{paths:15d}"
            f"{mc_price:15.10f}"
            f"{mc_error:15.10f}"
            f"{abs_error:15.10f}"
            f"{z_score:15.10f}"
            )
    
    plt.close('all')
    plt.figure()
    plt.xlabel('n paths', fontsize = 18)
    plt.ylabel('MC price', fontsize = 18)
    plt.plot(n_path_list, n_price, 'k-',linewidth = 1.5)
    plt.tick_params(axis='both', labelsize=14)
    plt.xscale("log")
    plt.tight_layout()
    
    plt.figure()
    plt.xlabel('n paths', fontsize = 18)
    plt.ylabel('std/abs/z', fontsize = 18)
    plt.plot(n_path_list, n_std, 'r-', linewidth = 1.5, label = 'std')
    plt.plot(n_path_list, n_abs, 'g-.', linewidth = 1.5, label = 'abs')
    plt.plot(n_path_list, n_z, 'b:', linewidth = 1.5, label = 'z')
    plt.xscale("log")
    plt.yscale("log")
    plt.legend(fontsize = 15)
    plt.tick_params(axis='both', labelsize=14)
    plt.tight_layout()
 







