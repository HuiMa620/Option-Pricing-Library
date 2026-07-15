# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 12:00:31 2026

@author: ma6
"""

import os 
os.chdir('..')

import numpy as np
import matplotlib.pyplot as plt
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.surface_black_scholes import SurfaceBlackScholesEngine
from pricing.volatility_surface import VolatilitySurface

def local_true_vol_skew(tau, strike, spot):
    moneyness = strike / spot
    skew = 0.25 - 0.3 * (moneyness - 1.0)
    term_structure = 0.1 * np.exp(-tau)
    return skew + term_structure




spot = 100
rate = 0.04
dividend = 0.02
maturities = np.linspace(0.2, 2.1, 20)
strikes = np.linspace(71, 130, 20)

true_vol_matrix = np.zeros(shape = (len(maturities), len(strikes)))

for i, tau in enumerate(maturities):
    for j, strike in enumerate(strikes):
        option_type = 'Call'
        
        local_true_vol = local_true_vol_skew(
            tau = float(tau),
            strike = float(strike),
            spot = spot
            )
        
        true_vol_matrix[i, j] = local_true_vol
        
surface = VolatilitySurface(
    maturities = maturities,
    strikes = strikes,
    vol_matrix = true_vol_matrix
    )

surface_engine = SurfaceBlackScholesEngine(surface)

market = MarketData(
    rate = rate,
    dividend = dividend,
    volatility = 0.3
    )

pricing_tau = 1.0
pricing_strikes = np.linspace(75, 125, 11)

prices = []
surface_vols = []

for strike in pricing_strikes:
    option = EuropeanOption(
        spot = spot,
        strike = strike,
        tau = pricing_tau,
        option_type = 'Call'
        )
    
    sigma = surface.get_vol(
        tau = pricing_tau,
        strike = float(strike)
        )
    
    price = surface_engine.price(
        option = option,
        market = market
        )
    
    surface_vols.append(sigma)
    prices.append(price)
    
    print(
        f"K = {strike:.10f},"
        f"surface vol={sigma:.10f},"
        f"surface BS price={price:.10f}"
        )
    

plt.close('all')

plt.figure()
plt.plot(pricing_strikes, surface_vols, 'k-')
plt.xlabel('Strike', fontsize = 15)
plt.ylabel('Surface Implied Volatility', fontsize = 15)
plt.title('Volatility used by Surface Black-Scholes Engine', fontsize = 15)
plt.show()

plt.figure()
plt.plot(pricing_strikes, prices, 'b-')
plt.xlabel('Strike', fontsize = 15)
plt.ylabel('Option Price', fontsize = 15)
plt.title('Surface Black-Scholes Call Prices', fontsize = 15)
plt.show()

    
































        

















