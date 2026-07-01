# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 00:12:23 2026

@author: ma6
"""

import os
os.chdir('..')

import numpy as np
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.delta_hedge import DeltaHedgingSimulator

call = EuropeanOption(
    spot = 100,
    strike = 110,
    tau = 1,
    option_type = 'Call'
    )

put = EuropeanOption(
    spot = 100,
    strike = 110,
    tau = 1,
    option_type = 'Put'
    )

market = MarketData(
    rate = 0.04,
    dividend= 0.02,
    volatility = 0.25
    )

hedge_engine = DeltaHedgingSimulator()
realized_volatility = 0.2
pnl = hedge_engine.simulate_one_path(call, market, realized_volatility)
print(f"PnL after delta hedge:{pnl:.10f}")
print()



realized_vol = [0.1, 0.25, 0.4]
print("Call option")
print()
for vol in realized_vol:
    n_pnl = hedge_engine.simulate(call, market, vol)
    print(f"Realized vol:  {vol:.10f}")
    print(f"Mean PnL:      {np.mean(n_pnl):.10f}")
    print(f"Std:           {np.std(n_pnl):.10f}")
    print(f"Quantile 0.05: {np.quantile(n_pnl, 0.05):.10f}")
    print(f"Quantile 0.95: {np.quantile(n_pnl, 0.95):.10f}")
    print()
    
print()
print('Put option')
print()
for vol in realized_vol:
    n_pnl = hedge_engine.simulate(put, market, vol)
    print(f"Realized vol:  {vol:.10f}")
    print(f"Mean PnL:      {np.mean(n_pnl):.10f}")
    print(f"Std:           {np.std(n_pnl):.10f}")
    print(f"Quantile 0.05: {np.quantile(n_pnl, 0.05):.10f}")
    print(f"Quantile 0.95: {np.quantile(n_pnl, 0.95):.10f}")
    print()












