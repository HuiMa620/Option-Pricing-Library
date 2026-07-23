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
    
    def __post_init__(self):
        self._validate_inputs()
        
    def _validate_inputs(self):
        if self.spot <= 0:
            raise ValueError('spot must be positive.')
        
        if self.strike <= 0:
            raise ValueError('strike must be positive.')
            
        if self.tau <= 0:
            raise ValueError('tau must be positive.')
            
        if self.option_type not in ['Call','Put']:
            raise ValueError("option_type must be 'Call' or 'Put'.")
            

@dataclass
class BarrierOption:
    spot: float
    strike: float
    barrier: float        # barrier level
    tau: float
    option_type: str      # Call or Put
    barrier_type: str     # Down or Up
    knock_type: str       # Out first version only support Out
    
    def __post_init__(self):
        self._validate_inputs()
    
    def _validate_inputs(self):
        if self.spot <= 0:
            raise ValueError('spot must be positive.')
        
        if self.strike <= 0:
            raise ValueError('strike must be positive.')
        
        if self.barrier <= 0:
            raise ValueError('barrier must be positive.')
        
        if self.tau <= 0:
            raise ValueError('tau must be positive.')
            
        if self.option_type not in ['Call','Put']:
            raise ValueError("option_type must be 'Call' or 'Put'.")
            
        if self.barrier_type not in ['Down', 'Up']:
            raise ValueError("barrier_type must be 'Down' or 'Up'.")
        
        if self.knock_type != 'Out':
            raise ValueError("Only knock_type = 'Out' is currently supported.")










