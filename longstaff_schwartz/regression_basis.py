# -*- coding: utf-8 -*-

import numpy as np
from numpy.linalg import lstsq


class RegressionBasis:
    def __init__(self, basis_functions):
        self.basis_functions = basis_functions

    def __str__(self):
        return ' + '.join(str(f) for f in self.basis_functions)

    def apply(self, x):
        for f in self.basis_functions:
            yield f(x)

    def __call__(self, x):
        assert x.ndim == 1
        x = x.reshape((x.shape[0], 1))
        return np.concatenate(tuple(self.apply(x)), axis=1)

    def fit(self, x, y):
        beta, *_ = lstsq(self(x), y, rcond=None)
        return FittedFunction(self, beta)


class FittedFunction:
    def __init__(self, basis, beta):
        self.basis = basis
        self.beta = beta

    def __call__(self, x):
        return self.basis(x) @ self.beta


class PolynomialRegressionFunction:
    def __init__(self, exponent):
        self.exponent = exponent

    def __str__(self):
        return f'x**{self.exponent}'

    def __call__(self, x):
        return x ** self.exponent


class PolynomialRegressionBasis(RegressionBasis):
    def __init__(self, degree):
        super().__init__([PolynomialRegressionFunction(i)
                          for i in range(degree + 1)])
        self.degree = degree
