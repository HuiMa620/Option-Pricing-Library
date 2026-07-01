# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 22:30:26 2026

@author: ma6
"""


from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.delta_hedge import DeltaHedgingSimulator
import numpy as np

def test_euro_call_delta_hedge():
    call = EuropeanOption(
        spot = 100,
        strike = 110,
        tau = 1,
        option_type = 'Call'
        )

    market = MarketData(
        rate = 0.04,
        dividend = 0.02,
        volatility = 0.25
        )


    hedge_engine = DeltaHedgingSimulator()
    
    #different volatility
    match_volatility = 0.25
    high_volatility = 0.3
    low_volatility = 0.2
    pnl = hedge_engine.simulate(call, market, match_volatility)
    high_vol_pnl = hedge_engine.simulate(call, market, high_volatility)
    low_vol_pnl = hedge_engine.simulate(call, market, low_volatility)
    assert abs(np.mean(pnl)) < 0.2
    assert np.mean(high_vol_pnl) < 0
    assert np.mean(low_vol_pnl) > 0
    

def test_euro_put_delta_hedge():
    put = EuropeanOption(
        spot = 100,
        strike = 110,
        tau = 1,
        option_type = 'Put'
        )
    
    market = MarketData(
        rate = 0.04,
        dividend = 0.02,
        volatility = 0.25
        )
    
    hedge_engine = DeltaHedgingSimulator()
    
    #difference realized volatility
    match_volatility = 0.25
    high_volatility = 0.3
    low_volatility = 0.2
    pnl = hedge_engine.simulate(put, market, match_volatility)
    high_vol_pnl = hedge_engine.simulate(put, market, high_volatility)
    low_vol_pnl = hedge_engine.simulate(put, market, low_volatility)
    assert abs(np.mean(pnl)) < 0.2
    assert np.mean(high_vol_pnl) < 0
    assert np.mean(low_vol_pnl) > 0
    






















