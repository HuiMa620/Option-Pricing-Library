# Option Pricing Library

A modular Python library for pricing equity options using analytical formulas, binomial trees, Monte Carlo simulation, finite-difference PDE methods, implied volatility solvers, and delta-hedging simulations.

This project was developed as a quantitative finance portfolio project, with a focus on core methods used in derivatives pricing and numerical finance.

## Features

### Black-Scholes Analytical Engine

- European call and put pricing
- Analytical Greeks:
  - Delta
  - Gamma
  - Vega
  - Theta
- Put-call parity validation

### Numerical Greeks

- Bump-and-revalue numerical Greeks
- Engine-agnostic design using a common `.price(option, market)` interface
- Validation against Black-Scholes analytical Greeks

### Binomial Tree Pricing

- Cox-Ross-Rubinstein style binomial tree
- European call and put pricing
- American call and put pricing
- Early exercise comparison against European option values
- Convergence validation against Black-Scholes benchmarks

### Monte Carlo Pricing

- Geometric Brownian motion simulation under the risk-neutral measure
- European call and put pricing
- Standard error estimation
- Antithetic variates for variance reduction
- Control variate variance reduction using discounted terminal stock value:

```text
X = exp(-rT) * S_T
E[X] = S0 * exp(-qT)
```

- Monte Carlo validation against Black-Scholes analytical prices

### Finite-Difference PDE Pricing

- Explicit finite-difference solver
- Implicit finite-difference solver
- Crank-Nicolson finite-difference solver
- Stability check for the explicit finite-difference method
- Grid convergence validation against Black-Scholes analytical benchmarks

### American Option Pricing

- American put pricing using implicit finite differences
- Early exercise constraint:

```python
V = max(continuation_value, exercise_value)
```

- Early exercise premium comparison against European put benchmarks
- American option pricing using binomial trees

### Implied Volatility Solver

- Bisection implied volatility solver
- Newton-Raphson implied volatility solver using Vega
- Hybrid Newton solver with bisection fallback
- Validation by recovering known volatility from Black-Scholes prices

### Delta Hedging Simulator

- Dynamic delta-hedging simulation for European call and put options
- Multi-path hedging P&L simulation
- Analysis of hedging P&L under implied vs realized volatility mismatch
- Demonstrates expected behavior:
  - Realized volatility below implied volatility: positive average P&L for short option hedge
  - Realized volatility equal to implied volatility: near-zero average P&L
  - Realized volatility above implied volatility: negative average P&L

## Project Structure

```text
OptionPricingLibrary/
├── pricing/
│   ├── __init__.py
│   ├── binomial_tree.py
│   ├── products.py
│   ├── market.py
│   ├── black_scholes.py
│   ├── delta_hedge.py
│   ├── implied_volatility.py
│   ├── numerical_greeks.py
│   ├── monte_carlo.py
│   ├── finite_difference.py
│   └── validation.py
│
├── examples/
│   ├── example_american_put_implicit_finite_difference.py
│   ├── example_binomial_tree.py
│   ├── example_black_scholes.py
│   ├── example_crank_nicolson_convergence.py
│   ├── example_crank_nicolson_finite_difference.py
│   ├── example_delta_hedge.py
│   ├── example_fast_finite_difference_convergence.py
│   ├── example_finite_difference.py
│   ├── example_finite_difference_convergence.py
│   ├── example_implicit_finite_difference.py
│   ├── example_implicit_finite_difference_convergence.py
│   ├── example_implied_volatility.py
│   ├── example_monte_carlo.py
│   ├── example_monte_carlo_control_variate.py
│   ├── example_monte_carlo_convergence.py
│   └── example_monte_carlo_greeks.py
│
├── tests/
│   ├── test_american_put_implicit_finite_difference.py
│   ├── test_black_scholes.py
│   ├── test_binomial_tree.py
│   ├── test_crank_nicolson_finite_difference.py
│   ├── test_delta_hedge.py
│   ├── test_finite_difference.py
│   ├── test_implied_volatility.py
│   ├── test_implicit_finite_difference.py
│   ├── test_monte_carlo.py
│   ├── test_monte_carlo_control_variate.py
│   ├── test_numerical_greeks.py
│   └── test_put_call_parity.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

```text
numpy
scipy
matplotlib
pytest
```

## Basic Usage

```python
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine

option = EuropeanOption(
    spot=100,
    strike=110,
    tau=0.5,
    option_type="Call"
)

market = MarketData(
    rate=0.04,
    dividend=0.02,
    volatility=0.25
)

engine = BlackScholesEngine()
price = engine.price(option, market)

print(price)
```

## Implied Volatility Example

```python
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.implied_volatility import ImpliedVolatilitySolver

option = EuropeanOption(
    spot=100,
    strike=110,
    tau=0.5,
    option_type="Call"
)

market = MarketData(
    rate=0.04,
    dividend=0.02,
    volatility=0.25
)

bs_engine = BlackScholesEngine()
market_price = bs_engine.price(option, market)

solver = ImpliedVolatilitySolver()
implied_vol = solver.solve(option, market, market_price)

print(f"Implied volatility: {implied_vol:.6f}")
```

## Monte Carlo Control Variate Example

```python
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.monte_carlo import MonteCarloEngine

option = EuropeanOption(
    spot=100,
    strike=110,
    tau=0.5,
    option_type="Call"
)

market = MarketData(
    rate=0.04,
    dividend=0.02,
    volatility=0.25
)

bs_price = BlackScholesEngine().price(option, market)

mc_engine = MonteCarloEngine(
    n_paths=100000,
    seed=1,
    antithetic=False
)

mc_price, mc_error = mc_engine.price_error(option, market)
cv_price, cv_error = mc_engine.price_control_variate_error(option, market)

print(f"Black-Scholes price:       {bs_price:.6f}")
print(f"Plain MC price:            {mc_price:.6f}")
print(f"Plain MC standard error:   {mc_error:.6f}")
print(f"Control variate price:     {cv_price:.6f}")
print(f"Control variate error:     {cv_error:.6f}")
```

## Finite-Difference Example

```python
from pricing.finite_difference import (
    ExplicitFiniteDifferenceEngine,
    ImplicitFiniteDifferenceEngine,
    CrankNicolsonFiniteDifferenceEngine,
)

explicit_engine = ExplicitFiniteDifferenceEngine(
    s_max=300,
    n_s=200,
    n_t=20000
)

implicit_engine = ImplicitFiniteDifferenceEngine(
    s_max=300,
    n_s=200,
    n_t=500
)

cn_engine = CrankNicolsonFiniteDifferenceEngine(
    s_max=300,
    n_s=200,
    n_t=500
)
```

Note: the explicit finite-difference method is conditionally stable and usually requires a much smaller time step than implicit or Crank-Nicolson methods.

## Delta Hedging Example

```python
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.delta_hedge import DeltaHedgingSimulator

option = EuropeanOption(
    spot=100,
    strike=110,
    tau=1.0,
    option_type="Call"
)

market = MarketData(
    rate=0.04,
    dividend=0.02,
    volatility=0.25
)

simulator = DeltaHedgingSimulator(
    n_steps=252,
    n_paths=10000,
    seed=10
)

pnl = simulator.simulate(
    option,
    market,
    realized_volatility=0.30
)

print(pnl.mean())
```

## American Put Example

```python
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.finite_difference import (
    ImplicitFiniteDifferenceEngine,
    AmericanPutImplicitFiniteDifferenceEngine,
)

put = EuropeanOption(
    spot=100,
    strike=110,
    tau=0.5,
    option_type="Put"
)

market = MarketData(
    rate=0.04,
    dividend=0.02,
    volatility=0.25
)

european_engine = ImplicitFiniteDifferenceEngine(
    s_max=300,
    n_s=200,
    n_t=500
)

american_engine = AmericanPutImplicitFiniteDifferenceEngine(
    s_max=300,
    n_s=200,
    n_t=500
)

european_price = european_engine.price(put, market)
american_price = american_engine.price(put, market)

print(f"European put price: {european_price:.6f}")
print(f"American put price: {american_price:.6f}")
print(f"Early exercise premium: {american_price - european_price:.6f}")
```

## Binomial Tree Example

```python
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.binomial_tree import BinomialTreeEngine

put = EuropeanOption(
    spot=100,
    strike=110,
    tau=0.5,
    option_type="Put"
)

market = MarketData(
    rate=0.04,
    dividend=0.02,
    volatility=0.25
)

bs_engine = BlackScholesEngine()

european_tree_engine = BinomialTreeEngine(
    n_steps=1000,
    exercise="European"
)

american_tree_engine = BinomialTreeEngine(
    n_steps=1000,
    exercise="American"
)

bs_price = bs_engine.price(put, market)
european_tree_price = european_tree_engine.price(put, market)
american_tree_price = american_tree_engine.price(put, market)

print(f"Black-Scholes European put: {bs_price:.6f}")
print(f"European tree put:         {european_tree_price:.6f}")
print(f"American tree put:         {american_tree_price:.6f}")
print(f"Early exercise premium:    {american_tree_price - european_tree_price:.6f}")
```

## Running Examples

Run examples from the project root directory:

```bash
python examples/example_black_scholes.py
python examples/example_binomial_tree.py
python examples/example_implied_volatility.py
python examples/example_delta_hedge.py
python examples/example_monte_carlo_control_variate.py
python examples/example_crank_nicolson_finite_difference.py
python examples/example_american_put_implicit_finite_difference.py
```

## Running Tests

```bash
pytest
```

The tests validate:

- Black-Scholes benchmark prices
- Put-call parity
- Analytical Greeks against numerical Greeks
- Binomial tree prices against Black-Scholes benchmarks
- Monte Carlo prices against Black-Scholes benchmarks
- Control variate standard error reduction
- Finite-difference prices against Black-Scholes benchmarks
- Implied volatility recovery from Black-Scholes prices
- Delta hedging P&L behavior under realized vs implied volatility mismatch
- American put no-arbitrage properties and early exercise premium

## Roadmap

Planned extensions:

- American put pricing with Crank-Nicolson finite differences
- Asian option pricing using Monte Carlo simulation
- Barrier option pricing using Monte Carlo simulation
- Monte Carlo path-dependent payoff framework
- Optimized tridiagonal matrix solver using Thomas algorithm or `scipy.linalg.solve_banded`
- Basic fixed-income pricing: zero-coupon bonds, coupon bonds, duration, convexity
- Optional C++ implementation of core pricing engines

## Purpose

This project demonstrates practical implementation of derivatives pricing methods, including analytical pricing, numerical Greeks, lattice methods, Monte Carlo simulation, variance reduction, finite-difference PDE solvers, American option early exercise, implied volatility inversion, delta hedging, validation examples, and unit testing.
