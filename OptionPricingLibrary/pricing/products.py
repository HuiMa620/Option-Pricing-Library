# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 18:28:52 2026

@author: ma6
"""

#pricing/products.py


from dataclasses import dataclass

@dataclass
class EuropeanOption:
    spot: float
    strike: float
    tau: float
    option_type: str # 'Call' or 'Put'










