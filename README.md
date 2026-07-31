# Option Pricing Library

A modular Python library for equity option pricing, numerical methods, volatility-surface construction, local volatility simulation, and Heston stochastic-volatility modeling.

This project was developed as a quantitative finance portfolio project. It demonstrates the core workflow used in derivatives analytics: analytical pricing, numerical pricing, model validation, implied-volatility inversion, volatility-surface construction, and stochastic-volatility calibration.

## Highlights

- Black-Scholes analytical pricing and Greeks
- Engine-agnostic numerical Greeks
- Monte Carlo pricing with antithetic variates and control variates
- Explicit, implicit, and Crank-Nicolson finite-difference PDE solvers
- European and American option pricing with binomial trees
- American put pricing with PSOR early-exercise handling
- Barrier option Monte Carlo pricing for knock-out options
- Delta-hedging simulation
- Implied-volatility inversion with Newton and bisection methods
- Volatility-surface construction from option chains
- Surface-based Black-Scholes pricing and Greeks
- Local-volatility Monte Carlo simulation
- Heston Monte Carlo simulation
- Heston semi-closed-form pricing using characteristic functions
- Heston price-based calibration to option prices

## Project Structure

```text
OptionPricingLibrary/
    pricing/
        products.py                  # EuropeanOption and BarrierOption definitions
        market.py                    # MarketData container
        black_scholes.py             # Analytical Black-Scholes pricing and Greeks
        numerical_greeks.py          # Bump-and-revalue Greeks
        monte_carlo.py               # GBM Monte Carlo engine
        finite_difference.py         # Explicit, implicit, and Crank-Nicolson PDE engines
        linear_solvers.py            # Linear solvers for finite-difference methods
        binomial_tree.py             # European and American binomial tree pricing
        psor.py                      # PSOR solver for American early-exercise problems
        delta_hedge.py               # Delta-hedging simulation
        implied_volatility.py        # Implied-volatility solvers
        volatility_surface.py        # Volatility surface construction and interpolation
        surface_black_scholes.py     # Black-Scholes pricing under a volatility surface
        option_chain.py              # CSV option-chain loader
        barrier_options.py           # Barrier option Monte Carlo engine
        local_volatility.py          # Local volatility surface and Monte Carlo engine
        heston_params.py             # Heston parameter container
        heston_monte_carlo.py        # Heston Monte Carlo engine
        heston_closed_form.py        # Heston semi-closed-form pricing engine
        heston_calibration.py        # Heston calibration engine
        validation.py                # Validation helpers

    examples/
        example_black_scholes.py
        example_monte_carlo.py
        example_finite_difference.py
        example_binomial_tree.py
        example_delta_hedge.py
        example_implied_volatility.py
        example_surface_black_scholes.py
        example_build_surface_from_option_chain.py
        example_barrier_options.py
        example_local_volatility.py
        example_heston_monte_carlo.py
        example_heston_closed_form.py
        example_heston_calibration.py
        ...

    tests/
        test_black_scholes.py
        test_monte_carlo.py
        test_finite_difference.py
        test_binomial_tree.py
        test_delta_hedge.py
        test_implied_volatility.py
        test_volatility_surface.py
        test_option_chain.py
        test_barrier_options.py
        test_local_volatility.py
        test_heston_monte_carlo.py
        test_heston_closed_form.py
        test_heston_calibration.py
        ...

    data/
        synthetic_option_chain.csv

    requirements.txt
    README.md
```

## Installation

Clone the repository and install the dependencies:

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

## Core Usage

Most engines use the same object-oriented interface:

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

price = engine.price(option, market)
```

The common product inputs are:

- `spot`: current underlying price
- `strike`: option strike
- `tau`: time to maturity in years
- `option_type`: `"Call"` or `"Put"`

The common market inputs are:

- `rate`: continuously compounded risk-free rate
- `dividend`: continuously compounded dividend yield
- `volatility`: Black-Scholes volatility, used by Black-Scholes-style engines and as a benchmark input

## Black-Scholes Analytical Engine

The Black-Scholes engine prices European calls and puts and computes analytical Greeks.

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

The project includes validation tests for Black-Scholes prices and put-call parity.

## Numerical Greeks

The numerical Greeks module provides bump-and-revalue calculations that can be applied to different pricing engines.

```python
from pricing.numerical_greeks import (
    numerical_delta,
    numerical_gamma,
    numerical_vega,
    numerical_theta,
)

numerical_delta_value = numerical_delta(engine, option, market)
```

This is useful for validating analytical Greeks and for pricing engines where closed-form Greeks are not implemented.

## Monte Carlo Pricing

The Monte Carlo engine simulates geometric Brownian motion under the risk-neutral measure.

```python
from pricing.monte_carlo import MonteCarloEngine

mc_engine = MonteCarloEngine(
    n_paths=100000,
    seed=42,
    antithetic=True
)

price = mc_engine.price(option, market)
price, standard_error = mc_engine.price_error(option, market)
```

Features:

- European call and put pricing
- Antithetic variates
- Standard error estimation
- Control variate pricing using the Black-Scholes price as the control
- Convergence examples against Black-Scholes analytical prices

Control variate example:

```python
cv_price = mc_engine.price_control_variate(option, market)
cv_price, cv_error = mc_engine.price_control_variate_error(option, market)
```

## Finite-Difference PDE Pricing

The finite-difference module implements explicit, implicit, and Crank-Nicolson finite-difference methods for the Black-Scholes PDE.

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

Implemented methods:

- Explicit finite difference
- Implicit finite difference
- Crank-Nicolson finite difference
- Thomas algorithm for tridiagonal systems
- Banded-matrix solver option
- Convergence tests against analytical Black-Scholes prices

## American Options and Early Exercise

The library supports American put pricing through both binomial trees and finite-difference methods.

```python
from pricing.binomial_tree import BinomialTreeEngine

bt_engine = BinomialTreeEngine(n_steps=500)
price = bt_engine.price(option, market, exercise="American")
```

Early exercise is also handled with a projected successive over-relaxation solver for the linear complementarity problem that arises in finite-difference American option pricing.

```python
from pricing.psor import psor
```

Implemented early-exercise tools:

- American put via binomial tree
- American put via implicit finite difference
- American put via Crank-Nicolson finite difference
- PSOR projection for early-exercise constraints
- Cross-validation between binomial tree and finite-difference engines

## Implied Volatility

The implied-volatility module solves for the Black-Scholes volatility that reproduces a target option price.

```python
from pricing.implied_volatility import ImpliedVolatilitySolver

iv_solver = ImpliedVolatilitySolver()
implied_vol = iv_solver.solve(
    option=option,
    market=market,
    target_price=price
)
```

Implemented methods:

- Bisection method
- Newton method
- Fallback logic for robust implied-volatility inversion

## Volatility Surface Workflow

The volatility-surface module builds an implied-volatility surface from option quotes and interpolates volatilities across strike and maturity.

```python
from pricing.volatility_surface import VolatilitySurface

surface = VolatilitySurface(
    maturities=[0.5, 1.0, 2.0],
    strikes=[80.0, 90.0, 100.0, 110.0, 120.0],
    vol_matrix=vol_matrix,
    interpolation_method="total_variance",
    extrapolation_method="flat"
)

vol = surface.get_vol(tau=1.0, strike=105.0)
```

Features:

- Volatility interpolation by strike and maturity
- Flat extrapolation outside the quoted grid
- Total-variance interpolation
- Synthetic volatility smile and skew examples
- Surface construction from option quotes

## Option Chain Loading

The option-chain module loads option quotes from CSV files and converts bid/ask quotes into mid prices.

```python
from pricing.option_chain import load_option_chain_csv

quotes = load_option_chain_csv("data/synthetic_option_chain.csv")
```

The project includes a synthetic option-chain CSV file for examples and tests.

## Surface-Based Black-Scholes Pricing

The surface-based Black-Scholes engine prices options using volatility read from an implied-volatility surface instead of a single constant market volatility.

```python
from pricing.surface_black_scholes import SurfaceBlackScholesEngine

surface_engine = SurfaceBlackScholesEngine(vol_surface=surface)

price = surface_engine.price(option, market)
delta = surface_engine.Delta(option, market)
gamma = surface_engine.Gamma(option, market)
vega = surface_engine.Vega(option, market)
theta = surface_engine.Theta(option, market)
```

This provides a practical bridge between market option-chain data and Black-Scholes-style pricing and Greeks.

## Barrier Option Pricing

The barrier option module prices knock-out barrier options with Monte Carlo path simulation.

```python
from pricing.products import BarrierOption
from pricing.barrier_options import BarrierMonteCarloEngine

barrier_option = BarrierOption(
    spot=100.0,
    strike=100.0,
    barrier=80.0,
    tau=1.0,
    option_type="Call",
    barrier_type="Down",
    knock_type="Out"
)

barrier_engine = BarrierMonteCarloEngine(
    n_paths=100000,
    n_steps=252,
    seed=1,
    antithetic=True
)

price, standard_error = barrier_engine.price_error(barrier_option, market)
```

Current barrier option support:

- Down-and-out options
- Up-and-out options
- Call and put payoffs
- Standard error estimation
- Validation against vanilla option bounds and limiting cases

## Local Volatility

The local-volatility module introduces a deterministic volatility function of time and spot, then simulates paths under that local volatility.

```python
from pricing.local_volatility import (
    LocalVolatilitySurface,
    LocalVolatilityMonteCarloEngine,
)

local_vol_surface = LocalVolatilitySurface(
    base_vol=0.20,
    skew_strength=0.30,
    term_strength=0.05,
    reference_spot=100.0
)

lv_engine = LocalVolatilityMonteCarloEngine(
    n_paths=100000,
    n_steps=252,
    seed=1,
    antithetic=True
)

price, standard_error = lv_engine.price_error(
    option=option,
    market=market,
    local_vol_surface=local_vol_surface
)
```

The first version uses a simple local volatility function with downside skew and term structure. It is intended as an introduction to local-volatility simulation rather than a full Dupire calibration engine.

## Heston Stochastic Volatility

The Heston model extends Black-Scholes by making variance stochastic:

```text
dS_t = (r - q) S_t dt + sqrt(v_t) S_t dW_t^S
dv_t = kappa (theta - v_t) dt + xi sqrt(v_t) dW_t^v
corr(dW_t^S, dW_t^v) = rho
```

The parameter container is shared by the Heston Monte Carlo, closed-form, and calibration modules:

```python
from pricing.heston_params import HestonParams

params = HestonParams(
    v0=0.25**2,
    kappa=2.0,
    theta=0.25**2,
    xi=0.4,
    rho=-0.7
)

print(params.satisfies_feller_condition())
```

Important convention: `v0` and `theta` are variances, not volatilities. For example, a 25% volatility corresponds to `0.25**2` variance.

### Heston Monte Carlo

```python
from pricing.heston_monte_carlo import HestonMonteCarloEngine

heston_mc = HestonMonteCarloEngine(
    n_paths=100000,
    n_steps=252,
    seed=1,
    antithetic=True
)

price, standard_error = heston_mc.price_error(
    option=option,
    market=market,
    params=params
)
```

Features:

- Correlated Brownian shocks for spot and variance
- Full-truncation-style handling of non-negative variance
- European call and put pricing
- Standard error estimation
- Black-Scholes limiting-case tests

### Heston Semi-Closed-Form Pricing

The Heston closed-form engine prices European options using the Heston characteristic function and numerical Fourier inversion.

```python
from pricing.heston_closed_form import HestonClosedFormEngine

heston_cf = HestonClosedFormEngine(
    integration_limit=100.0
)

price = heston_cf.price(
    option=option,
    market=market,
    params=params
)
```

Validation includes:

- Black-Scholes limiting case when volatility of variance is zero
- Put-call parity
- Positive and finite price checks
- Sanity check against Heston Monte Carlo

### Heston Calibration

The Heston calibration module fits Heston parameters to option prices by minimizing a price-based loss function.

```python
from pricing.heston_calibration import HestonCalibrator

quotes = [
    {
        "tau": 0.5,
        "strike": 90.0,
        "option_type": "Call",
        "market_price": 12.34,
    },
    {
        "tau": 1.0,
        "strike": 100.0,
        "option_type": "Call",
        "market_price": 9.87,
    },
]

calibrator = HestonCalibrator(pricing_engine=heston_cf)

calibrated_params, result = calibrator.calibrate(
    quotes=quotes,
    spot=100.0,
    rate=0.04,
    dividend=0.02,
    initial_guess=None,
    bounds=None
)

print(calibrated_params)
print(result.success)
```

The current calibration objective is:

```text
mean((Heston model price - market price)^2)
```

The test suite validates calibration on synthetic option prices generated from known Heston parameters. The validation focuses on whether calibrated prices fit the synthetic market prices, rather than requiring exact recovery of each individual Heston parameter.

## Examples

Run examples from the project root:

```bash
python examples/example_black_scholes.py
python examples/example_monte_carlo.py
python examples/example_surface_black_scholes.py
python examples/example_build_surface_from_option_chain.py
python examples/example_barrier_options.py
python examples/example_local_volatility.py
python examples/example_heston_monte_carlo.py
python examples/example_heston_closed_form.py
python examples/example_heston_calibration.py
```

Selected example workflows:

- `example_black_scholes.py`: analytical pricing and Greeks
- `example_monte_carlo.py`: Monte Carlo price and standard error
- `example_build_surface_from_option_chain.py`: CSV option chain to implied-volatility surface
- `example_surface_black_scholes.py`: pricing and Greeks under a volatility surface
- `example_barrier_options.py`: barrier option Monte Carlo pricing
- `example_local_volatility.py`: local-volatility Monte Carlo pricing
- `example_heston_monte_carlo.py`: stochastic-volatility simulation under Heston
- `example_heston_closed_form.py`: characteristic-function-based Heston pricing
- `example_heston_calibration.py`: synthetic Heston calibration workflow

## Running Tests

Run the full test suite from the project root:

```bash
pytest tests
```

Or run individual test files:

```bash
pytest tests/test_black_scholes.py
pytest tests/test_volatility_surface.py
pytest tests/test_heston_closed_form.py
pytest tests/test_heston_calibration.py
```

The test suite covers:

- Analytical Black-Scholes prices and Greeks
- Put-call parity
- Monte Carlo convergence and variance reduction
- Finite-difference convergence against Black-Scholes
- Binomial tree pricing
- American put comparisons across methods
- Implied-volatility inversion
- Volatility-surface interpolation and extrapolation
- Option-chain loading
- Barrier option payoff and knock-out logic
- Local-volatility path simulation
- Heston Monte Carlo simulation
- Heston semi-closed-form pricing
- Heston calibration on synthetic prices

## Design Principles

This project emphasizes:

- A common `.price(option, market, ...)` style interface where possible
- Clear separation between products, market data, models, and numerical engines
- Model validation through limiting cases and cross-method comparisons
- Educational readability over production-level optimization
- Incremental development from Black-Scholes to volatility surfaces and stochastic volatility

## Current Scope and Limitations

The library is intended as a portfolio and educational project, not a production trading system.

Current limitations include:

- Equity-style options only
- European vanilla pricing for Heston closed-form and calibration
- Knock-out barrier options only in the first barrier option version
- Local volatility uses a simple parametric local-volatility function, not a full Dupire calibration
- Heston calibration currently uses price-based least squares, not implied-volatility-based calibration or vega-weighted calibration
- No production market-data cleaning, no exchange calendars, and no transaction cost modeling

## Possible Future Extensions

Possible future improvements include:

- Implied-volatility-based Heston calibration
- Vega-weighted price calibration
- Multi-start Heston calibration
- Dupire local-volatility calibration from an implied-volatility surface
- Additional exotic products such as Asian, lookback, and double-barrier options
- Jump-diffusion or Bates model extensions
- SABR model implementation and calibration
- More robust packaging with `pyproject.toml`
- Continuous integration with automated tests

## Suggested GitHub Release Description

```text
v1.0.0 - Option Pricing Library with Volatility Surface and Heston Calibration

This release completes the first full version of the option pricing library, including analytical Black-Scholes pricing, Monte Carlo simulation, finite-difference PDE methods, binomial trees, American option early-exercise handling, volatility-surface construction, barrier option pricing, local volatility simulation, Heston Monte Carlo, Heston semi-closed-form pricing, and Heston calibration to option prices.
```

## License

No license file is currently included. Add a license before distributing or reusing this project publicly.
