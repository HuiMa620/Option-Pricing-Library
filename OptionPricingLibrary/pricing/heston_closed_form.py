# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:02:32 2026

@author: ma6
"""

import numpy as np
from scipy.integrate import  quad

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.heston_params import HestonParams


class HestonClosedFormEngine:
    def __init__(
            self,
            integration_limit = 100.0,
            integration_epsabs = 1e-8,
            integration_epsrel = 1e-8
            ):
        
        self.integration_limit = integration_limit
        self.integration_epsabs = integration_epsabs
        self.integration_epsrel = integration_epsrel
        
        self._validate_inputs()
        
    def _validate_inputs(self):
        if self.integration_limit <= 0:
            raise ValueError("integration_limit must be positive.")
            
        if self.integration_epsabs <= 0:
            raise ValueError("integration_epsabs must be positive.")
            
        if self.integration_epsrel <= 0:
            raise ValueError("integration_epsrel must be positive.")
    
    
    def _characteristic_function(self, u, option, market, params):
        """
        Heston characteristic function of log(S_T)
        
        phi(u) = E[exp(i u log(S_T))]
        """
        
        S0 = option.spot
        T = option.tau
        r = market.rate
        y = market.dividend
        
        v0 = params.v0
        kappa = params.kappa
        theta = params.theta
        xi = params.xi
        rho = params.rho
        
        x0 = np.log(S0)
        i = 1j
        
        #if xi = 0, Heston reduces to deterministic variance
        # To avoid division by xi**2, handle separately
        
        if xi == 0.0:
            if kappa == 0.0:
                integrated_variance = v0 * T
            else:
                integrated_variance = (
                    theta * T + (v0 - theta) * (1.0 - np.exp(-kappa * T))/kappa
                    )
            mean = x0 + (r - y) * T - 0.5*integrated_variance
            return np.exp(
                i*u*mean - 0.5*u**2 * integrated_variance
                )
        
        d = np.sqrt(
            (rho * xi * i * u - kappa) ** 2 + xi ** 2 * (u**2 + i*u) 
            )
        
        g = (
            (kappa - rho*xi*i*u - d) / (kappa - rho*xi*i*u + d)
            )
        
        exp_minus_dT = np.exp(-d*T)
        
        C = (
            i*u*(x0 + (r - y)*T) + (kappa*theta/xi**2)*(
                (kappa - rho*xi*i*u - d)*T - 2.0*np.log(
                    (1.0 - g*exp_minus_dT) / (1.0 - g)
                    )
                )
            )
        
        D = (
            (v0 / xi**2)*(kappa - rho*xi*i*u - d)*(
                (1.0 - exp_minus_dT) / (1.0 - g*exp_minus_dT)
                )
            )
        
        return np.exp(C + D)
    
    
    def _integrand_p1(self, u, option, market, params):
        K = option.strike
        logK = np.log(K)
        i = 1j
        
        phi_u_minus_i = self._characteristic_function(u-i, option, market, params)
        
        phi_minus_i = self._characteristic_function(-i, option, market, params)
        
        value = np.exp(-i * u * logK) * phi_u_minus_i / (i*u*phi_minus_i)
        
        return np.real(value)
    
    def _integrand_p2(self, u, option, market, params):
        K = option.strike
        logK = np.log(K)
        i = 1j
        
        phi_u = self._characteristic_function(u, option, market, params)
        
        value = np.exp(-i*u*logK) * phi_u / (i*u)
        
        return np.real(value)
    
    def _probability(self, option, market, params, probability_type):
        if probability_type == 1:
            integrand = lambda u: self._integrand_p1(
                u, option, market, params
                )
            
        elif probability_type == 2:
            integrand = lambda u: self._integrand_p2(
                u, option, market, params
                )
            
        else:
            raise ValueError("probability_type must be 1 or 2.")
            
        integral_value, _ = quad(
            integrand,
            1e-8,
            self.integration_limit,
            epsabs = self.integration_epsabs,
            epsrel = self.integration_epsrel,
            limit = 200
            )
        
        probability = 0.5 + integral_value / np.pi
        
        return probability
    
    def _call_price(self, option, market, params):
        S0 = option.spot
        K = option.strike
        T = option.tau
        r = market.rate
        y = market.dividend
        
        P1 = self._probability(
            option = option,
            market = market,
            params = params,
            probability_type = 1
            )
        
        P2 = self._probability(
            option = option,
            market = market, 
            params = params, 
            probability_type = 2
            )
        
        call_price = S0*np.exp(-y*T)*P1 - K*np.exp(-r*T)*P2
        
        return call_price
    
    def price(self, option, market, params):
        if not isinstance(option, EuropeanOption):
            raise TypeError("option must be a EuropeanOption.")
        
        if not isinstance(market, MarketData):
            raise TypeError("market must be a MarketData.")
        
        if not isinstance(params, HestonParams):
            raise TypeError("params must be a HestonParams.")
        
        #Black_scholes limiting case
        
        if params.xi == 0.0 and np.isclose(params.v0, params.theta):
            bs_market = MarketData(
                rate = market.rate,
                dividend = market.dividend,
                volatility = np.sqrt(params.theta)
                )
            
            return BlackScholesEngine().price(
                option = option,
                market = bs_market
                )
        
        call_price = self._call_price(
            option = option,
            market = market,
            params = params
            )
        
        if option.option_type == 'Call':
            return call_price
        
        elif option.option_type == 'Put':
            S0 = option.spot
            K = option.strike
            T = option.tau
            r = market.rate
            y = market.dividend
            
            put_price = (
                call_price - S0*np.exp(-y*T) + K*np.exp(-r*T)
                )
            
            return put_price
        
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
            
    
        
        
        
        
   