# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 23:36:34 2026

@author: ma6
"""


from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine


class SurfaceBlackScholesEngine:
    '''
    Use volatility surface to get implied volatility
    Solve the price by bs_engine
    '''
    def __init__(self, volatility_surface):
        self.volatility_surface = volatility_surface
        self.bs_engine = BlackScholesEngine()
        
        
    def _market_with_surface_vol(self, option, market):
        sigma = self.volatility_surface.get_vol(
            tau = option.tau,
            strike = option.strike
            )
        
        surface_market = MarketData(
            rate = market.rate,
            dividend = market.dividend,
            volatility = sigma
            )
        
        return surface_market
    
    
    def price(self, option, market):
        
        surface_market = self._market_with_surface_vol(
            option = option,
            market = market
            )
        
        return self.bs_engine.price(
            option = option,
            market = surface_market
            )
    
    
    
    def Delta(self, option, market):
        surface_market = self._market_with_surface_vol(
            option = option,
            market = market
            )
        
        return self.bs_engine.Delta(
            option = option,
            market = surface_market
            )


    def Gamma(self, option, market):
        surface_market = self._market_with_surface_vol(
            option = option,
            market = market
            )
        
        return self.bs_engine.Gamma(
            option = option,
            market = surface_market
            )



    def Vega(self, option, market):
        surface_market = self._market_with_surface_vol(
            option = option,
            market = market
            )
        
        return self.bs_engine.Vega(
            option = option,
            market = surface_market
            )


    def Theta(self, option, market):
        surface_market = self._market_with_surface_vol(
            option = option,
            market = market
            )
        
        return self.bs_engine.Theta(
            option = option,
            market = surface_market
            )







    
    
    
    
    
    