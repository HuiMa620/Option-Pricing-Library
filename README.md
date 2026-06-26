Option Pricing Library
A modular Python library for pricing and validating equity options using analytical formulas, Monte Carlo simulation, and finite-difference PDE methods.
This project is designed as a quantitative finance learning and portfolio project. It focuses on core derivatives pricing techniques commonly used in options markets, including Black-Scholes analytics, Greeks, Monte Carlo simulation, finite-difference solvers, and American option early exercise constraints.


Features

Products and Market Data
•	European call and put option representation
•	Market data container for:
  1.	risk-free rate
  2.	dividend yield
  3.	volatility
     
Black-Scholes Analytical Engine
•	European call and put pricing
•	Analytical Greeks:
  1.	Delta
  2.  Gamma
  3.	Vega
  4.	Theta
•	Put-call parity validation

Numerical Greeks
•	Bump-and-revalue numerical Greeks
•	Engine-agnostic design: numerical Greeks can be applied to any pricing engine with a .price(option, market) interface
•	Validation against Black-Scholes analytical Greeks

Monte Carlo Pricing
•	Geometric Brownian motion simulation under the risk-neutral measure
•	European call and put pricing
•	Antithetic variates for variance reduction
•	Standard error estimation
•	Monte Carlo convergence examples
•	Monte Carlo validation against Black-Scholes prices

Finite-Difference PDE Pricing
Finite-difference solvers for the Black-Scholes PDE in time-to-maturity form:
•	Explicit finite-difference solver
•	Implicit finite-difference solver
•	Crank-Nicolson finite-difference solver
•	Grid convergence validation against Black-Scholes analytical benchmarks
•	Stability check for the explicit finite-difference method
American Option Pricing
•	American put pricing using an implicit finite-difference method
•	Early exercise constraint:
•	V = max(continuation_value, exercise_value)
•	Early exercise premium comparison against European put benchmarks


Project Structure
OptionPricingLibrary/
│
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
│   ├── example_numerical_greeks.py
│   ├── example_monte_carlo.py
│   ├── example_monte_carlo_convergence.py
│   ├── example_monte_carlo_greeks.py
│   ├── example_finite_difference.py
│   ├── example_finite_difference_convergence.py
│   ├── example_implicit_finite_difference.py
│   ├── example_implicit_finite_difference_convergence.py
│   ├── example_crank_nicolson_finite_difference.py
│   ├── example_crank_nicolson_convergence.py
│   └── example_american_put_implicit_finite_difference.py
│
├── tests/
│   ├── test_black_scholes.py
│   ├── test_put_call_parity.py
│   ├── test_numerical_greeks.py
│   ├── test_monte_carlo.py
│   ├── test_finite_difference.py
│   ├── test_implicit_finite_difference.py
│   ├── test_crank_nicolson_finite_difference.py
│   └── test_american_put_implicit_finite_difference.py
│
├── requirements.txt
├── README.md
└── .gitignore


Installation
Required packages include:
numpy
scipy
matplotlib
pytest
Basic Usage
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
Black-Scholes Greeks
engine = BlackScholesEngine()

delta = engine.delta(option, market)
gamma = engine.gamma(option, market)
vega = engine.vega(option, market)
theta = engine.theta(option, market)

print(delta, gamma, vega, theta)
Monte Carlo Example
from pricing.monte_carlo import MonteCarloEngine

mc_engine = MonteCarloEngine(
    n_paths=100000,
    seed=1,
    antithetic=True
)

price, standard_error = mc_engine.price_error(option, market)

print(f"Monte Carlo price: {price:.6f}")
print(f"Standard error:    {standard_error:.6f}")
Finite-Difference Example
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

explicit_price = explicit_engine.price(option, market)
implicit_price = implicit_engine.price(option, market)
cn_price = cn_engine.price(option, market)

print(explicit_price)
print(implicit_price)
print(cn_price)
Note: the explicit finite-difference method is conditionally stable and generally requires a much smaller time step than implicit or Crank-Nicolson methods.
American Put Example
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

european_put_price = european_engine.price(put, market)
american_put_price = american_engine.price(put, market)

print(f"European put price:  {european_put_price:.6f}")
print(f"American put price:  {american_put_price:.6f}")
print(f"Early exercise premium: {american_put_price - european_put_price:.6f}")


Running Examples
Run example scripts from the project root directory:
python examples/example_crank_nicolson_finite_difference.py
python examples/example_american_put_implicit_finite_difference.py
Running Tests
Run all unit tests from the project root directory:
pytest
The tests validate:
•	Black-Scholes prices against known benchmark values
•	Put-call parity
•	Analytical Greeks against numerical Greeks
•	Monte Carlo prices against Black-Scholes benchmarks
•	Finite-difference prices against Black-Scholes benchmarks
•	Crank-Nicolson finite-difference prices
•	American put no-arbitrage properties:
  1.	American put price is greater than or equal to European put price
  2.	American put price is greater than or equal to intrinsic value


Numerical Methods Implemented
Analytical Pricing
The Black-Scholes engine provides closed-form European option prices and Greeks under the standard lognormal diffusion assumption.
Monte Carlo Simulation
The Monte Carlo engine simulates terminal stock prices under geometric Brownian motion:
dS = (r - q) S dt + sigma S dW
The simulated discounted payoff is used to estimate the option value. Antithetic variates are included to reduce variance.
Finite-Difference PDE Methods
The finite-difference engines solve the Black-Scholes PDE in time-to-maturity form:
∂V/∂τ = 0.5 σ² S² ∂²V/∂S² + (r - q) S ∂V/∂S - rV
Implemented schemes:
Explicit:
V_new = V_old + dt * L(V_old)

Implicit:
V_new - dt * L(V_new) = V_old

Crank-Nicolson:
V_new - V_old = 0.5 * dt * (L(V_old) + L(V_new))
American Put Early Exercise
The American put engine applies an early exercise constraint after each implicit time step:
V(S, t) = max(continuation value, K - S)
This converts the European PDE problem into a discrete approximation of the American option free-boundary problem.
Roadmap
Planned extensions:
•	American put pricing with Crank-Nicolson finite differences
•	Binomial tree pricing for European and American options
•	Asian option pricing using Monte Carlo simulation
•	Barrier option pricing using Monte Carlo simulation
•	Delta-hedging simulation and hedging error analysis
•	Optimized tridiagonal matrix solvers using Thomas algorithm or scipy.linalg.solve_banded
•	Optional C++ implementation of core pricing engines
Project Purpose
This project is intended to demonstrate practical knowledge of derivatives pricing, numerical methods, and modular Python software design. It combines analytical finance theory with computational methods including Monte Carlo simulation, PDE solvers, convergence validation, and unit testing.

