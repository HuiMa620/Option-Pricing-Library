# Option Pricing Library

A modular Python library for pricing equity options using analytical formulas, Monte Carlo simulation, finite-difference PDE methods, binomial trees, implied volatility tools, and volatility-surface-based pricing.

This project was developed as a quantitative finance portfolio project. The main goal is to demonstrate core derivatives pricing methods used in equity option modeling, including model validation, numerical convergence checks, and a realistic option-chain-to-volatility-surface workflow.

## Current Status

The library currently supports:

- Black-Scholes analytical pricing and Greeks
- Numerical Greeks using bump-and-revalue
- Monte Carlo pricing with variance reduction
- Explicit, implicit, and Crank-Nicolson finite-difference PDE pricing
- American put pricing with implicit and Crank-Nicolson finite-difference methods
- Binomial tree pricing for European and American options
- Delta hedging simulation
- Implied volatility inversion using bisection and Newton methods
- Implied volatility surface construction from option quotes
- Surface-based Black-Scholes pricing and Greeks
- Option chain CSV loading with bid/ask mid-price conversion
- Synthetic option chain data for examples and integration tests

## Project Structure

```text
OptionPricingLibrary/
    pricing/
        products.py
        market.py
        black_scholes.py
        numerical_greeks.py
        monte_carlo.py
        finite_difference.py
        linear_solvers.py
        binomial_tree.py
        delta_hedge.py
        implied_volatility.py
        volatility_surface.py
        surface_black_scholes.py
        option_chain.py
        validation.py

    examples/
        example_black_scholes.py
        example_monte_carlo.py
        example_monte_carlo_control_variate.py
        example_monte_carlo_convergence.py
        example_monte_carlo_greeks.py
        example_numerical_greeks.py
        example_finite_difference.py
        example_implicit_finite_difference.py
        example_crank_nicolson_finite_difference.py
        example_binomial_tree.py
        example_delta_hedge.py
        example_implied_volatility.py
        example_volatility_surface_get_vol.py
        example_volatility_smile.py
        example_volatility_skew.py
        example_surface_black_scholes.py
        example_build_surface_from_option_chain.py
        example_american_put_implicit_finite_difference.py
        example_american_put_crank_nicolson_finite_difference.py

    tests/
        test_black_scholes.py
        test_put_call_parity.py
        test_monte_carlo.py
        test_monte_carlo_control_variate.py
        test_numerical_greeks.py
        test_finite_difference.py
        test_implicit_finite_difference.py
        test_crank_nicolson_finite_difference.py
        test_binomial_tree.py
        test_delta_hedge.py
        test_implied_volatility.py
        test_volatility_surface.py
        test_option_chain.py
        test_american_put_implicit_finite_difference.py
        test_american_put_crank_nicolson_finite_difference.py
        test_american_put_binomial_tree_vs_finite_difference.py
        test_american_put_crank_nicolson_binomial_tree_implicit.py

    data/
        synthetic_option_chain.csv

    requirements.txt
    README.md
```

## Installation

Clone the repository and install the required Python packages:

```bash
git clone <repository-url>
cd OptionPricingLibrary
pip install -r requirements.txt
```

Core dependencies:

```text
numpy
scipy
matplotlib
pytest
```

## Core Data Structures

The library uses a common object-oriented interface for option products and market inputs.

```python
from pricing.products import EuropeanOption
from pricing.market import MarketData

option = EuropeanOption(
    spot=100.0,
    strike=110.0,
    tau=0.5,
    option_type="Call"
)

market = MarketData(
    rate=0.04,
    dividend=0.02,
    volatility=0.25
)
```

Most engines follow the same interface:

```python
price = engine.price(option, market)
```

## Black-Scholes Analytical Engine

The Black-Scholes engine supports European call and put pricing with analytical Greeks.

```python
from pricing.black_scholes import BlackScholesEngine

engine = BlackScholesEngine()
price = engine.price(option, market)
delta = engine.Delta(option, market)
gamma = engine.Gamma(option, market)
vega = engine.Vega(option, market)
theta = engine.Theta(option, market)
```

Supported analytical Greeks:

- Delta
- Gamma
- Vega
- Theta

The library also includes put-call parity validation.

## Numerical Greeks

The numerical Greeks module provides engine-agnostic bump-and-revalue calculations:

```python
from pricing.numerical_greeks import (
    numerical_delta,
    numerical_gamma,
    numerical_vega,
    numerical_theta,
)
```

These functions can be used to validate analytical Greeks or compute Greeks for engines where closed-form formulas are not available.

## Monte Carlo Pricing

The Monte Carlo engine simulates geometric Brownian motion under the risk-neutral measure.

Features:

- European call and put pricing
- Antithetic variates
- Standard error estimation
- Control variate pricing using Black-Scholes as the control
- Convergence examples against Black-Scholes prices

```python
from pricing.monte_carlo import MonteCarloEngine

mc_engine = MonteCarloEngine(
    n_paths=100000,
    seed=42,
    antithetic=True
)

price = mc_engine.price(option, market)
price, error = mc_engine.price_error(option, market)
```

Control variate pricing:

```python
cv_price = mc_engine.price_control_variate(option, market)
cv_price, cv_error = mc_engine.price_control_variate_error(option, market)
```

## Finite-Difference PDE Pricing

The library includes explicit, implicit, and Crank-Nicolson finite-difference engines.

```python
from pricing.finite_difference import (
    ExplicitFiniteDifferenceEngine,
    ImplicitFiniteDifferenceEngine,
    CrankNicolsonFiniteDifferenceEngine,
)

fd_engine = CrankNicolsonFiniteDifferenceEngine(
    s_max=300.0,
    n_s=300,
    n_t=300,
    solver="thomas"
)

price = fd_engine.price(option, market)
```

Implemented PDE methods:

- Explicit finite difference
- Implicit finite difference
- Crank-Nicolson finite difference
- Tridiagonal linear solvers using Thomas algorithm and banded matrix routines
- Convergence examples against Black-Scholes analytical prices

## American Put Pricing

The library supports American put pricing using finite-difference methods and binomial trees.

```python
from pricing.finite_difference import (
    AmericanPutImplicitFiniteDifferenceEngine,
    AmericanPutCrankNicolsonFiniteDifferenceEngine,
)
from pricing.binomial_tree import BinomialTreeEngine

american_fd = AmericanPutCrankNicolsonFiniteDifferenceEngine(
    s_max=300.0,
    n_s=300,
    n_t=300,
    solver="thomas"
)

price = american_fd.price(option, market)
```

American put results are validated against binomial tree benchmarks.

Current American option implementation focuses on American puts. A future improvement is to add a PSOR solver for a more direct treatment of the early-exercise linear complementarity problem.

## Binomial Tree Pricing

The binomial tree engine supports European and American exercise styles.

```python
from pricing.binomial_tree import BinomialTreeEngine

engine = BinomialTreeEngine(
    n_steps=1000,
    exercise="American"
)

price = engine.price(option, market)
```

The binomial tree module is used both as a standalone pricing method and as a benchmark for American finite-difference methods.

## Implied Volatility Solver

The implied volatility solver supports bisection and Newton methods.

```python
from pricing.implied_volatility import ImpliedVolatilitySolver

solver = ImpliedVolatilitySolver()

iv = solver.solve(
    option=option,
    market=market,
    market_price=market_price,
    initial_guess=0.2
)
```

Features:

- Bisection solver
- Newton solver
- Automatic fallback behavior through the main `solve()` interface
- Validation against known Black-Scholes prices

## Volatility Surface

The volatility surface module builds an implied volatility surface from option quotes.

```python
from pricing.volatility_surface import VolatilitySurface

surface = VolatilitySurface.from_option_quotes(
    quotes=quotes,
    spot=100.0,
    rate=0.04,
    dividend=0.02,
    initial_vol_guess=0.2,
    interpolation_method="vol",
    extrapolation="flat"
)

sigma = surface.get_vol(
    tau=1.0,
    strike=110.0
)
```

Supported features:

- Construction from option quote dictionaries
- Implied volatility inversion quote by quote
- Rectangular maturity-strike surface validation
- Duplicate quote detection
- Missing quote detection
- Volatility interpolation
- Total variance interpolation
- Flat extrapolation outside the grid
- Smile and skew examples using synthetic option data

Each quote should have the form:

```python
{
    "tau": 0.5,
    "strike": 100.0,
    "option_type": "Call",
    "market_price": 5.25,
}
```

## Surface-Based Black-Scholes Engine

The surface Black-Scholes engine prices options by first querying the implied volatility surface at the option maturity and strike, then passing that volatility into the Black-Scholes analytical engine.

```python
from pricing.surface_black_scholes import SurfaceBlackScholesEngine

surface_engine = SurfaceBlackScholesEngine(surface)

surface_price = surface_engine.price(option, market)
surface_delta = surface_engine.Delta(option, market)
surface_gamma = surface_engine.Gamma(option, market)
surface_vega = surface_engine.Vega(option, market)
surface_theta = surface_engine.Theta(option, market)
```

This provides a realistic workflow for surface-implied pricing and Greeks:

```text
option chain -> implied volatility surface -> surface volatility -> Black-Scholes price and Greeks
```

The current Greeks are sticky-strike surface Greeks: the volatility is read from the surface at the option's maturity and strike, then the standard Black-Scholes Greek formulas are applied using that volatility.

## Option Chain CSV Loader

The option chain module loads bid/ask option chain data from CSV and converts each row into the quote format required by `VolatilitySurface.from_option_quotes()`.

```python
from pricing.option_chain import load_option_chain_csv

quotes = load_option_chain_csv("data/synthetic_option_chain.csv")
```

Expected CSV columns:

```text
tau,strike,option_type,bid,ask
```

Example row:

```text
0.5,100,Call,5.0,5.4
```

The loader computes:

```python
market_price = 0.5 * (bid + ask)
```

Validation includes:

- Required column checks
- Positive maturity and strike
- Non-negative bid
- Positive ask
- Ask greater than or equal to bid
- Valid option type: `Call` or `Put`
- Positive mid price

## Synthetic Option Chain Example

The `data/synthetic_option_chain.csv` file provides a small synthetic option chain for examples and integration tests. It contains a rectangular grid of maturities and strikes with bid/ask prices generated from a mild skew volatility surface.

The main workflow example is:

```bash
python examples/example_build_surface_from_option_chain.py
```

This example demonstrates:

- Loading option chain data from CSV
- Computing mid prices
- Building an implied volatility surface
- Plotting the 3D volatility surface
- Plotting a heatmap
- Pricing an option using the surface-based Black-Scholes engine
- Computing surface-based Greeks

## Delta Hedging Simulation

The delta hedging simulator uses Black-Scholes delta to dynamically hedge simulated stock paths.

```python
from pricing.delta_hedge import DeltaHedgingSimulator

simulator = DeltaHedgingSimulator(
    n_steps=252,
    n_paths=1000,
    seed=42
)

results = simulator.simulate(
    option=option,
    market=market,
    realized_volatility=0.25
)
```

This module is intended to illustrate discrete hedging error and the relationship between model volatility, realized volatility, and hedging P&L.

## Tests

The repository includes tests for the main pricing components:

```text
tests/test_black_scholes.py
tests/test_put_call_parity.py
tests/test_monte_carlo.py
tests/test_monte_carlo_control_variate.py
tests/test_numerical_greeks.py
tests/test_finite_difference.py
tests/test_implicit_finite_difference.py
tests/test_crank_nicolson_finite_difference.py
tests/test_binomial_tree.py
tests/test_delta_hedge.py
tests/test_implied_volatility.py
tests/test_volatility_surface.py
tests/test_option_chain.py
tests/test_american_put_implicit_finite_difference.py
tests/test_american_put_crank_nicolson_finite_difference.py
tests/test_american_put_binomial_tree_vs_finite_difference.py
tests/test_american_put_crank_nicolson_binomial_tree_implicit.py
```

The tests cover:

- Black-Scholes prices and Greeks
- Put-call parity
- Monte Carlo convergence
- Monte Carlo control variate variance reduction
- Numerical Greeks versus analytical Greeks
- Explicit, implicit, and Crank-Nicolson finite-difference methods
- American put pricing versus binomial tree benchmarks
- Implied volatility inversion
- Volatility surface construction, interpolation, extrapolation, smile, and skew behavior
- Surface-based Black-Scholes pricing and Greeks
- Option chain CSV parsing and validation
- Full option-chain-to-volatility-surface integration workflow

To run tests with pytest:

```bash
pytest tests/
```

Individual test files can also be run directly during development.

## Example Workflows

### Black-Scholes price and Greeks

```bash
python examples/example_black_scholes.py
```

### Monte Carlo pricing and convergence

```bash
python examples/example_monte_carlo.py
python examples/example_monte_carlo_convergence.py
python examples/example_monte_carlo_control_variate.py
```

### Finite-difference pricing

```bash
python examples/example_finite_difference.py
python examples/example_implicit_finite_difference.py
python examples/example_crank_nicolson_finite_difference.py
```

### American put pricing

```bash
python examples/example_american_put_implicit_finite_difference.py
python examples/example_american_put_crank_nicolson_finite_difference.py
```

### Implied volatility and volatility surface

```bash
python examples/example_implied_volatility.py
python examples/example_volatility_surface_get_vol.py
python examples/example_volatility_smile.py
python examples/example_volatility_skew.py
python examples/example_surface_black_scholes.py
python examples/example_build_surface_from_option_chain.py
```

### Delta hedging

```bash
python examples/example_delta_hedge.py
```

## Development Roadmap

Completed or implemented in first version:

1. Black-Scholes analytical pricing and Greeks
2. Numerical Greeks
3. Monte Carlo pricing with antithetic variates and control variates
4. Explicit, implicit, and Crank-Nicolson finite-difference pricing
5. Binomial tree pricing
6. American put pricing using implicit and Crank-Nicolson finite-difference methods
7. Implied volatility solver
8. Volatility surface construction from option quotes
9. Surface-based Black-Scholes pricing and Greeks
10. Option chain CSV loader and synthetic option chain workflow

Planned next steps:

1. Add PSOR solver for American put early-exercise LCP treatment
2. Add barrier option pricing
3. Introduce local volatility concepts
4. Add Heston Monte Carlo pricing
5. Add Heston semi-closed-form pricing
6. Add Heston calibration to implied volatility surfaces
7. Improve project packaging and command-line test execution
8. Add more robust data handling for real-world option chain formats

## Notes and Limitations

This project is designed for learning, validation, and portfolio demonstration. It is not intended for production trading or risk management use.

Current limitations include:

- Equity option focus
- European options for most engines
- American exercise currently focused on puts
- Volatility surface built on rectangular synthetic or cleaned option quote grids
- Surface Greeks are sticky-strike Black-Scholes Greeks
- No transaction costs, funding costs, or discrete dividends in the current core models
- No stochastic volatility calibration yet
