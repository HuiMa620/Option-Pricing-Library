# Option Pricing Library

A modular Python library for pricing equity options using analytical formulas, Monte Carlo simulation, and finite-difference PDE methods.

This project was developed as a quantitative finance portfolio project, with a focus on core methods used in derivatives pricing.

## Features

### Black-Scholes Analytical Engine

* European call and put pricing
* Analytical Greeks:

  * Delta
  * Gamma
  * Vega
  * Theta
* Put-call parity validation

### Numerical Greeks

* Bump-and-revalue numerical Greeks
* Engine-agnostic design using a common `.price(option, market)` interface
* Validation against Black-Scholes analytical Greeks

### Monte Carlo Pricing

* Geometric Brownian motion simulation under the risk-neutral measure
* European call and put pricing
* Antithetic variates for variance reduction
* Standard error estimation
* Monte Carlo convergence validation against Black-Scholes prices

### Finite-Difference PDE Pricing

* Explicit finite-difference solver
* Implicit finite-difference solver
* Crank-Nicolson finite-difference solver
* Grid convergence validation against Black-Scholes analytical benchmarks
* Stability check for the explicit finite-difference method

### American Option Pricing

* American put pricing using implicit finite differences
* Early exercise constraint:

```python
V = max(continuation_value, exercise_value)
```

* Early exercise premium comparison against European put benchmarks

## Project Structure

```text
OptionPricingLibrary/
├── pricing/
│   ├── __init__.py
│   ├── products.py
│   ├── market.py
│   ├── black_scholes.py
│   ├── numerical_greeks.py
│   ├── monte_carlo.py
│   ├── finite_difference.py
│   └── validation.py
│
├── examples/
│   ├── example_black_scholes.py
│   ├── example_monte_carlo.py
│   ├── example_finite_difference.py
│   ├── example_crank_nicolson_finite_difference.py
│   └── example_american_put_implicit_finite_difference.py
│
├── tests/
│   ├── test_black_scholes.py
│   ├── test_put_call_parity.py
│   ├── test_numerical_greeks.py
│   ├── test_monte_carlo.py
│   ├── test_finite_difference.py
│   ├── test_crank_nicolson_finite_difference.py
│   └── test_american_put_implicit_finite_difference.py
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

## Running Examples

Run examples from the project root directory:

```bash
python examples/example_black_scholes.py
python examples/example_crank_nicolson_finite_difference.py
python examples/example_american_put_implicit_finite_difference.py
```

## Running Tests

```bash
pytest
```

The tests validate:

* Black-Scholes benchmark prices
* Put-call parity
* Analytical Greeks against numerical Greeks
* Monte Carlo prices against Black-Scholes benchmarks
* Finite-difference prices against Black-Scholes benchmarks
* American put no-arbitrage properties

## Roadmap

Planned extensions:

* American put pricing with Crank-Nicolson finite differences
* Binomial tree pricing for European and American options
* Asian option pricing using Monte Carlo simulation
* Barrier option pricing using Monte Carlo simulation
* Delta-hedging simulation and hedging error analysis
* Optimized tridiagonal matrix solver using Thomas algorithm or `scipy.linalg.solve_banded`
* Optional C++ implementation of core pricing engines

## Purpose

This project demonstrates practical implementation of derivatives pricing methods, including analytical pricing, Monte Carlo simulation, PDE-based finite-difference methods, American option early exercise constraints, validation examples, and unit testing.
