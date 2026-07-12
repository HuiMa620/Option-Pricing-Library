# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 12:20:12 2026

@author: ma6
"""

import os
os.chdir('..')

import numpy as np
import matplotlib.pyplot as plt
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.volatility_surface import VolatilitySurface

def local_true_vol_skew(tau, strike, spot):
    moneyness = strike / spot
    skew = 0.25 - 0.3 * (moneyness - 1.0)
    term_structure = 0.1 * np.exp(-tau)
    return skew + term_structure


def synthetic_skew_vol_quotes(
        spot = 100.0,
        rate = 0.04,
        dividend = 0.02
        ):
    
    maturities = np.linspace(0.2, 2.1, 20)
    strikes = np.linspace(71, 130, 20)
    
    bs_engine = BlackScholesEngine()
    quotes = []
    true_vol_matrix = np.zeros(shape = (len(maturities), len(strikes)))
    
    for i, tau in enumerate(maturities):
        for j, strike in enumerate(strikes):
            
            if strike < spot:
                option_type = 'Put'
            else:
                option_type = 'Call'
            
            local_true_vol = local_true_vol_skew(
                tau = float(tau),
                strike = float(strike),
                spot = spot
                )
            
            true_vol_matrix[i, j] = local_true_vol
            
            option = EuropeanOption(
                spot = spot,
                strike = strike,
                tau = tau,
                option_type = option_type
                )
            
            market = MarketData(
                rate = rate,
                dividend = dividend,
                volatility = local_true_vol
                )
            
            market_price = bs_engine.price(option, market)
            
            quotes.append({
                'tau': float(tau),
                'strike': float(strike),
                'option_type': option_type,
                'market_price': float(market_price)
                })
            
    return quotes, maturities, strikes, true_vol_matrix



spot = 100
rate = 0.04
dividend = 0.02
quotes, maturities, strikes, true_vol_matrix = synthetic_skew_vol_quotes(
    spot = spot,
    rate = rate,
    dividend = dividend
    )

surface = VolatilitySurface.from_option_quotes(
    quotes = quotes,
    spot = spot,
    rate = rate,
    dividend = dividend,
    initial_vol_guess = 0.2
    )

print(f'Recovered vol min:  {np.min(surface.vol_matrix):.10f}')
print(f'Recovered vol max:  {np.max(surface.vol_matrix):.10f}')
print(f'True vol min:       {np.min(true_vol_matrix):.10f}')
print(f'True vol max:       {np.max(true_vol_matrix):.10f}')
print(f'Max error:          {np.max(np.abs(surface.vol_matrix - true_vol_matrix)):.10f}')


K_grid, T_grid = np.meshgrid(
    surface.strikes,
    surface.maturities
    )

Z = surface.vol_matrix

plt.close('all')

#3D volatility surface plot
fig = plt.figure(figsize = (8,6))
ax = fig.add_subplot(111, projection = '3d')

ax.plot_surface(
    K_grid,
    T_grid,
    Z,
    edgecolor = 'k',
    linewidth = 0.5,
    alpha =0.8
    )

ax.set_zlim(Z.min() * 0.9, Z.max() * 1.1)
ax.set_xlabel("Strike")
ax.set_ylabel("Maturity")
ax.set_zlabel("Implied Volatility")
ax.set_title("Implied Volatility Surface")

plt.show()

#plot heatmap
plt.figure(figsize=(7, 5))

plt.imshow(
    Z,
    origin="lower",
    aspect="auto",
    extent=[
        surface.strikes[0],
        surface.strikes[-1],
        surface.maturities[0],
        surface.maturities[-1]
    ],
    vmin = Z.min() * 0.9,
    vmax = Z.max() * 1.1
)

plt.colorbar(label="Implied Volatility")
plt.xlabel("Strike")
plt.ylabel("Maturity")
plt.title("Implied Volatility Heatmap")

plt.show()































