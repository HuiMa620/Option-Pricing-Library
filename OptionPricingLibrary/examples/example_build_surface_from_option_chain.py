# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 15:32:25 2026

@author: ma6
"""

import os
os.chdir('..')

import numpy as np
import matplotlib.pyplot as plt
from pricing.option_chain import load_option_chain_csv
from pricing.volatility_surface import VolatilitySurface
from pricing.surface_black_scholes import SurfaceBlackScholesEngine
from pricing.products import EuropeanOption
from pricing.market import MarketData

quotes = load_option_chain_csv(
    'data/synthetic_option_chain.csv'
    )

surface = VolatilitySurface.from_option_quotes(
    quotes = quotes,
    spot = 100.0,
    rate = 0.04,
    dividend = 0.02,
    initial_vol_guess = 0.2
    )

K_grid, T_grid = np.meshgrid(
    surface.strikes,
    surface.maturities
    )

Z = surface.vol_matrix
print('Volatility Surface from option chain')
print(Z)
print()

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

surface_engine = SurfaceBlackScholesEngine(surface)

option = EuropeanOption(
    spot = 100.0,
    strike = 110.0,
    tau = 1.0,
    option_type = 'Call',
    )

market = MarketData(
    rate = 0.04,
    dividend = 0.02,
    volatility = 100.0 #This volatility will be replaced
    )

surface_price = surface_engine.price(option, market)

surface_vol = surface.get_vol(
    tau = option.tau,
    strike = option.strike
    )

label_width = 60
value_width = 15
label_vol = f"Surface implied vol at T={option.tau}, K={option.strike}"
label_price = "Option price by volatility surface from option chain"

surface_delta = surface_engine.Delta(option, market)
surface_gamma = surface_engine.Gamma(option, market)
surface_vega = surface_engine.Vega(option, market)
surface_theta = surface_engine.Theta(option, market)

print(f"{label_vol:<{label_width}}: {surface_vol:>{value_width}.10f}")
print(f"{label_price:<{label_width}}: {surface_price:>{value_width}.10f}")
print(f"{'Surface Delta':<{label_width}}: {surface_delta:>{value_width}.10f}")
print(f"{'Surface Gamma':<{label_width}}: {surface_gamma:>{value_width}.10f}")
print(f"{'Surface Vega':<{label_width}}: {surface_vega:>{value_width}.10f}")
print(f"{'Surface Theta':<{label_width}}: {surface_theta:>{value_width}.10f}")








