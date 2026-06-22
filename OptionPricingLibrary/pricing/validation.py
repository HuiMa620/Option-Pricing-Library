# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 18:33:29 2026

@author: ma6
"""

#pricing/validation.py

import numpy as np

def check_put_call_parity(call_price, put_price, option, market):
    S = option.spot
    K = option.strike
    tau = option.tau
    r = market.rate
    y = market.dividend
    
    left = call_price - put_price
    right = S * np.exp(-y*tau) - K * np.exp(-r*tau)
    error = left - right
    return left, right, error






