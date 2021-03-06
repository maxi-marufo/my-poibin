# Poisson Binomial Distribution for Python

### This Version
This is a fork from the [original project](https://github.com/tsakim/poibin)
by [@tsakim](https://github.com/tsakim)
This version adds these Features:
* Adds `mean`, `var`, `std`, `skew`, `amax` and `argmax` methods
* Solves FFT instability issues, as [proposed here](https://github.com/tsakim/poibin/pull/7)
by [@zeeshansayyed](https://github.com/zeeshansayyed)

## About
The module contains a Python implementation of functions related to the Poisson
Binomial probability distribution \[1\], which describes the probability
distribution of the sum of independent Bernoulli random variables with
non-uniform success probabilities. For further information, see reference \[1\].

The implemented methods are:
* `pmf`: probability mass function
* `cdf`: cumulative distribution function
* `pval`: p-value for right tailed tests
* `mean`: mean of the distribution
* `var`: variance of the distribution
* `std`: standard deviation of the distribution
* `skew`: skewness of the distribution
* `amax`: max value of the probability mass function
* `argmax`: index of the max value of the probability mass function

## Authors
Mika Straka, Maxi Marufo, Zeeshan Sayyed

## Dependencies
* [NumPy](http://www.numpy.org/)
* [pytest](https://docs.pytest.org/en/latest/contents.html) For testing

## Usage
Consider `n` independent and non-identically distributed random variables and
be `p` a list/NumPy array of the corresponding Bernoulli success probabilities.
In order to create the Poisson Binomial distributions, use
```python
from poibin import PoiBin
pb = PoiBin(p)
```
* Mean
```python
pb.mean()
```
* Variance
```python
pb.var()
```
* Standard Deviation
```python
pb.std()
```
* Skewness
```python
pb.skew()
```
* Max value
```python
pb.amax()
```
* Index of the max value
```python
pb.argmax()
```

Be `x` a list/NumPy array of different numbers of success. Use the following
methods to obtain the corresponding quantities:

* Probability mass function
```python
pb.pmf(x)
```
* Cumulative distribution function
```python
pb.cdf(x)
```
* P-values for right tailed tests
```python
pb.pval(x)
```

All three methods accept single integers as well as lists/NumPy arrays of
integers. Note that `x[i]` must be smaller than `len(p)`.

## Testing
The methods have been implemented using the `pytest` module. To run the tests, execute

```
$ pytest test_poibin.py
```
in the command line. For verbose mode, use

```
$ pytest -v test_poibin.py
```

## Reference
[Yili Hong, On computing the distribution function for the Poisson binomial
distribution,
Computational Statistics & Data Analysis, Volume 59, March 2013, pages 41-51,
ISSN 0167-9473](http://dx.doi.org/10.1016/j.csda.2012.10.006)

---
Copyright (c) 2016-2020 Mika J. Straka, Maxi Marufo, Zeeshan Sayyed
