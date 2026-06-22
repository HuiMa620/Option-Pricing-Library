# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:23:39 2026

@author: ma6
"""

#pricing/numerical_greeks.py
#bump-and-revalue


from dataclasses import replace

def numerical_delta(engine, option, market, bump = 1e-4):
    option_up = replace(option, spot = option.spot + bump)
    option_down = replace(option, spot = option.spot - bump)
    
    price_up = engine.price(option_up, market)
    price_down = engine.price(option_down, market)
    
    return (price_up - price_down)/(2*bump)




def numerical_gamma(engine, option, market, bump = 1e-3):
    option_up = replace(option, spot = option.spot + bump)
    option_down = replace(option, spot = option.spot - bump)
    
    price_up = engine.price(option_up, market)
    price_mid = engine.price(option, market)
    price_down = engine.price(option_down, market)
    
    return (price_up - 2*price_mid + price_down)/(bump**2)




def numerical_theta(engine, option, market, bump = 1e-4):
    bump = max(option.tau/100, 1e-6)
    option_up = replace(option, tau = option.tau + bump)
    option_down = replace(option, tau = option.tau - bump)
    
    price_up = engine.price(option_up, market)
    price_down = engine.price(option_down, market)
    
    return -(price_up - price_down)/(2*bump)

    


def numerical_vega(engine, option, market, bump = 1e-4):
    market_up = replace(market, volatility = market.volatility + bump)
    market_down = replace(market, volatility = market.volatility - bump)
    
    price_up = engine.price(option, market_up)
    price_down = engine.price(option, market_down)
    
    return (price_up - price_down)/(2*bump)

    
    
    
    








