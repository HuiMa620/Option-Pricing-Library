# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 18:31:47 2026

@author: ma6
"""

#pricing/black_scholes.py

import numpy as np
from scipy.stats import norm



class BlackScholesEngine:
    def _calc_d1(self, option, market):
        S = option.spot
        K = option.strike
        tau = option.tau
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        d1 = (np.log(S/K) + (r - y + sigma**2/2)*tau)/(sigma * np.sqrt(tau))
        return d1
    
    
    
    def _calc_d2(self, option, market):
        tau = option.tau
        sigma = market.volatility
        
        d1 = self._calc_d1(option, market)
        d2 = d1 - sigma* np.sqrt(tau)
        return d2
    
    
    
    def price(self, option, market):
        S = option.spot
        K = option.strike
        tau = option.tau
        r = market.rate
        y = market.dividend
        
        d1 = self._calc_d1(option, market)
        d2 = self._calc_d2(option, market)
        
        if option.option_type == 'Call':
            price = S * np.exp(- y* tau) * norm.cdf(d1) - K*np.exp(-r * tau)*norm.cdf(d2)
        elif option.option_type == 'Put':
            price = K * np.exp(-r * tau) * norm.cdf(-d2) - S * np.exp(-y *tau) * norm.cdf(-d1)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'")
        return price
    
    
    def Delta(self, option, market):
        tau = option.tau
        y = market.dividend
        
        d1 = self._calc_d1(option, market)
        if option.option_type == 'Call':
            delta = np.exp(-y*tau) * norm.cdf(d1)
        elif option.option_type == 'Put':
            delta = -np.exp(-y*tau) * (1 - norm.cdf(d1))
        else:
            raise ValueError("option_type must be 'Call' or 'Put'")
        
        return delta
    
    
    
    def Gamma(self, option, market):
        S = option.spot
        tau = option.tau
        y = market.dividend
        sigma = market.volatility
        
        d1 = self._calc_d1(option, market)
        gamma = norm.pdf(d1) * np.exp(-y * tau)/(S * sigma * np.sqrt(tau))
        return gamma
    
    
    
    def Theta(self, option, market):
        S = option.spot
        K = option.strike
        tau = option.tau
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        d1 = self._calc_d1(option, market)
        d2 = self._calc_d2(option, market)
        
        if option.option_type == 'Call':
            theta = - S*norm.pdf(d1)*sigma*np.exp(-y*tau)/(2*np.sqrt(tau)) + y * S * np.exp(-y*tau)*norm.cdf(d1) - r*K*np.exp(-r*tau) * norm.cdf(d2)
        elif option.option_type == 'Put':
            theta = -S *norm.pdf(d1)*sigma*np.exp(-y*tau)/(2*np.sqrt(tau)) - y*S*np.exp(-y*tau) * norm.cdf(-d1) + r*K *np.exp(-r*tau)*norm.cdf(-d2)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'")
        
        return theta
    
    
    
        
    def Vega(self, option, market):
        S = option.spot
        tau = option.tau
        y = market.dividend
        
        d1 = self._calc_d1(option, market)
        vega = S * np.exp(-y * tau) * np.sqrt(tau) * norm.pdf(d1)
        return vega





