# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 16:30:24 2026

@author: ma6
"""
import os
os.chdir('..')

import numpy as np
import matplotlib.pyplot as plt
from pricing.volatility_surface import VolatilitySurface
from pricing.black_scholes import BlackScholesEngine
from pricing.products import EuropeanOption
from pricing.market import MarketData

'''
#quotes data structure
quotes = [
    {"tau": 0.5, "strike": 90,  "option_type": "Put",  "market_price": 2.50},
    {"tau": 0.5, "strike": 100, "option_type": "Call", "market_price": 7.00},
    {"tau": 0.5, "strike": 110, "option_type": "Call", "market_price": 3.80},

    {"tau": 1.0, "strike": 90,  "option_type": "Put",  "market_price": 4.20},
    {"tau": 1.0, "strike": 100, "option_type": "Call", "market_price": 10.00},
    {"tau": 1.0, "strike": 110, "option_type": "Call", "market_price": 6.30},
    ]
'''

spot = 100
rate = 0.04
dividend = 0.02
maturities = np.linspace(0.2, 2.1, 20)
strikes = np.linspace(91, 110, 20)
true_vol = 0.25

bs_engine = BlackScholesEngine()

#synthetic option quotes with constant volatility
quotes= []
for tau in maturities:
    for strike in strikes:
        if strike < spot:
            option_type = 'Put'
        else:
            option_type = 'Call'
        
        option = EuropeanOption(
            spot = spot,
            strike = strike,
            tau = tau,
            option_type = option_type
            )
        
        market = MarketData(
            rate = rate,
            dividend = dividend,
            volatility = true_vol
            )
        
        market_price = bs_engine.price(option, market)
        quotes.append({
            'tau': float(tau),
            'strike': float(strike),
            'option_type': option_type,
            'market_price': float(market_price)
            })


#generate the volatility surface
surface = VolatilitySurface.from_option_quotes(
    quotes = quotes,
    spot = spot,
    rate = rate,
    dividend = dividend,
    initial_vol_guess = 0.2
    )

print(surface.maturities)
print(surface.strikes)
print(surface.vol_matrix)

sigma = surface.get_vol(
    tau = 0.75,
    strike = 110
    )
print(sigma)

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

ax.set_zlim(0.0, 1.0)
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
    vmin = 0.0,
    vmax = 1.0
)

plt.colorbar(label="Implied Volatility")
plt.xlabel("Strike")
plt.ylabel("Maturity")
plt.title("Implied Volatility Heatmap")

plt.show()









