# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 18:29:34 2026

@author: ma6
"""

from dataclasses import dataclass

@dataclass
class HestonParams:
    v0: float
    kappa: float
    theta: float
    xi: float
    rho: float
    
    def __post_init__(self):
        self._validate_inputs()
    
    def _validate_inputs(self):
        if self.v0 < 0:
            raise ValueError("v0 must be non-negative.")
        
        if self.kappa <= 0:
            raise ValueError("kappa must be positive.")
        
        if self.theta <= 0:
            raise ValueError("theta must be positive.")
        
        if self.xi < 0:
            raise ValueError("xi must be non-negative.")
        
        if self.rho < -1 or self.rho > 1:
            raise ValueError("rho must be between -1 and 1.")
    
    def satisfies_feller_condition(self):
        return 2.0*self.kappa * self.theta >= self.xi**2
    
    
    
    
    