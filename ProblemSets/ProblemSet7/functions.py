'''
Define functions to be used for solving my Dynamic Programming Problem
'''

# Import packages
import numpy as np
import pandas as pd
from scipy import interpolate
from scipy.optimize import fminbound
import scipy.optimize as opt
import numba


# Define utility function
def utility(m, m_prime, P, sigma):
    '''
    Utility function
    '''
    c = (m / P) - (m_prime / P)
    if sigma == 1:
        U = np.log(c)
    else:
        U = (c ** (1 - sigma)) / (1 - sigma)

    return U



# Define the endogenous grid operator
# @numba.jit()
def bellman_operator(V, m_grid, P_grid, params):
    beta, sigma = params

    Val_func = interpolate.interp1d(m_grid, V, kind='cubic', fill_value='extrapolate')

    # Initialize array for operator and policy function
    TV = np.empty_like(V)
    optM = np.empty_like(TV)
    # loops for populating grids with max Value and optimal Ms
    for i, p in enumerate(P_grid):
        for j, m in enumerate(m_grid):
            def objective(m_prime):
                return - utility(m, m_prime, p, sigma) - beta * Val_func(m_prime)
            m_prime_star = fminbound(objective, 1e-6, m - 1e-6)
            optM[j] = m_prime_star
            TV[j] = - objective(m_prime_star)


    return TV, optM
