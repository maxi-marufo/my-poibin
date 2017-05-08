# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29, 2016

Module:
    poibin - Poisson Binomial Distribution

Author:
    Mika Straka

Description:
    Implementation of the Poisson Binomial distribution as described in the
    reference [Hong2013]_.

    Implemented method:

        * ``pmf``: probability mass function
        * ``cdf``: cumulative distribution function
        * ``pval``: p-value (1 - cdf)

Usage:
    Be ``p`` a list or  NumPy array of success probabilities for ``n``
    non-identically distributed Bernoulli random variables.

    Import the module and create an instance of the distribution with::

        >>> from poibin import PoiBin
        >>> pb = PoiBin(p)

    Be ``x`` a list or NumPy array of different number of successes.
    To obtain:

    * probability mass function of x, use::

        >>> pb.pmf(x)

    * cumulative distribution function of x, use

        >>> pb.cdf(x)

    * p-values of x, use

        >>> pb.pval(x)

    The functions are applied component-wise and a NumPy array of the same
    length as ``x`` is returned.

References:
.. [Hong2013] Yili Hong, On computing the distribution function for the Poisson
    binomial distribution,
    Computational Statistics & Data Analysis, Volume 59, March 2013,
    Pages 41-51, ISSN 0167-9473,
    http://dx.doi.org/10.1016/j.csda.2012.10.006.
"""

import collections
import numpy as np


class PoiBin:

    def __init__(self, p):
        self.p = np.array(p)
        self.n = self.p.size
        self.check_input_prob()
        self.omega = 2 * np.pi / (self.n + 1)
        self.pmf_list = self.get_pmf_xi()
        self.cdf_list = self.get_cdf(self.pmf_list)

# ------------------------------------------------------------------------------
# Methods for the Poisson Binomial Distribution
# ------------------------------------------------------------------------------

    def pmf(self, kk):
        """Calculate the probability mass function ``pmf`` for the input values.

        The ``pmf`` is defined as

        .. math::

            pmf(k) = Pr(X = k), k = 0, 1, ..., n.

        :param kk: integers for which the pmf is calculated
        :type kk: int or list of ints
        """
        self.check_rv_input(kk)
        return self.pmf_list[kk]

    def cdf(self, kk):
        """Calculate the cumulative distribution function for the input values.

        The cumulative distribution function ``cdf`` is defined as

        .. math::

            cdf(k) = Pr(X \leq k), k = 0, 1, ..., n.

        :param kk: integers for which the cdf is calculated.
        :type kk: int or list of integers
        """
        self.check_rv_input(kk)
        return self.cdf_list[kk]

    def pval(self, kk):
        """Return the p-value corresponding to the input values kk,

        The p-values of right-sided testing are defined as

        .. math::

            pval(k) = Pr(X \geq k ),  k = 0, 1, ..., n.

        .. note::

            Since :math:`cdf(k) = Pr(X <= k)`, the function returns

            .. math::

                1 - cdf(X < k) & = 1 - cdf(X <= k - 1)
                               & = 1 - cdf(X <= k) + pmf(X = k),

                               k = 0, 1, .., n.

        :param kk: integers for which the cdf is calculated.
        :type kk: int, or np.array or list of integers
        """
        self.check_rv_input(kk)
        i = 0
        try:
            isinstance(kk, collections.Iterable)
            fk = np.array(kk, dtype='float')
            # if input is iterable (list, numpy.array):
            for k in kk:
                fk[i] = 1. - self.cdf(k) + self.pmf(k)
                i += 1
            return fk
        except TypeError:
            # if input is an integer:
            if kk == 0:
                return 1
            else:
                return 1 - self.cdf(kk - 1)

# ------------------------------------------------------------------------------
# Methods to obtain pmf and cdf
# ------------------------------------------------------------------------------

    def get_cdf(self, xx):
        """Return the values of the cumulative density function.

        Return a list which contains all the values of the cumulative
        density function for :math:`i = 0, 1, ..., n`j.
        """
        c = np.empty(self.n + 1)
        c[0] = xx[0]
        for i in range(1, self.n + 1):
            c[i] = c[i - 1] + xx[i]
        return c

    def get_pmf_xi(self):
        """Return the values of ``xi``.

        The components ``xi`` make up the probability mass function.
        """
        chi = np.empty(self.n + 1, dtype=complex)
        chi[0] = 1
        half_n = int(self.n / 2 + self.n % 2)
        # set first half of chis:
        chi[1:half_n + 1] = self.get_chi(np.arange(1, half_n + 1))
        # set second half of chis:
        chi[half_n + 1:self.n + 1] = np.conjugate(chi[1:self.n - half_n + 1]
                                                  [::-1])
        chi /= self.n + 1
        xi = np.fft.fft(chi)
        if self.check_xi_are_real(xi):
            xi = xi.real
        else:
            raise TypeError("pmf / xi values have to be real.")
        return xi

    def get_chi(self, idx_array):
        """Return the values of ``chi`` for the specified indices."""
        # get_z:
        e = np.exp(self.omega * idx_array * 1j)
        xy = 1 - self.p + self.p * e[:, np.newaxis]
        # get__argz_sum:
        argz_sum = np.arctan2(xy.imag, xy.real).sum(axis=1)
        # get_d:
        exparg = np.log(np.abs(xy)).sum(axis=1)
        d = np.exp(exparg)
        # get_chi:
        chi = d * np.exp(argz_sum * 1j)
        return chi

# ------------------------------------------------------------------------------
# Auxiliary functions
# ------------------------------------------------------------------------------

    def check_rv_input(self, kk):
        """Assert that the input values ``kk`` are OK.

        Check that the input values ``kk`` for the random variable are >=0,
        integers and <= n.
        """
        try:
            for k in kk:
                assert (type(k) == int or type(k) == np.int64), \
                        "Values in input list must be integers"
                assert k >= 0, 'Values in input list cannot be negative.'
                assert k <= self.n, \
                    'Values in input list must be smaller or equal to the ' \
                    'number of input probabilities "n"'
        except TypeError:
            assert (type(kk) == int or type(kk) == np.int64), \
                'Input value must be an integer.'
            assert kk >= 0, "Input value cannot be negative."
            assert kk <= self.n, \
                'Input value cannot be greater than ' + str(self.n)
        return True

    @staticmethod
    def check_xi_are_real(xx):
        """Check whether all the xis have imaginary part equal to 0.

        The probabilities ``pmf`` have to be positive.
        """
        eps = 1e-15  # account for machine precision
        return np.all(xx.imag <= eps)

    def check_input_prob(self):
        """Check that all the input probabilities are in the interval [0, 1]."""
        if self.p.shape != (self.n,):
            raise ValueError(
                "Input must be an one-dimensional array or a list.")
        if not np.all(self.p >= 0):
            raise ValueError("Input probabilites have to be non negative.")
        if not np.all(self.p <= 1):
            raise ValueError("Input probabilites have to be smaller than 1.")

################################################################################
# Main
################################################################################

if __name__ == "__main__":
    pass

