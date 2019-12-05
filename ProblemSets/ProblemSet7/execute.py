# import packages
import numpy as np
import matplotlib.pyplot as plt
import ar1_approx as ar1
import functions


# Set parameters
beta = 0.95
sigma = 1.0
alpha = 1
rho = 0.75
sigma_eps = 0.2
N = 6
num_sigma = 4

# Create grid for m
lb_m = 0.4
ub_m = 2.0
size_m = 100
m_grid = np.linspace(lb_m, ub_m, size_m)

# Theoretical sigma of epsilon
sigma_P = sigma_eps / ((1 - rho ** 2) ** (1 / 2))
step = (num_sigma * sigma_P) / (N / 2)

# Create grid for P'
pi, P_grid = ar1.rouwen(rho, alpha, step, N)
# P_discrete = sim_markov(P_grid, pi, num_draws)

VFtol = 1e-5  # tolerance for distance between V's
VFdist = 7.0  # initial distance for V
VFmaxiter = 2000  # maximum iterations allowed
V = np.zeros(size_m)
Vstore = np.zeros((size_m, VFmaxiter))  # initialize array for storing V's
VFiter = 1  # initialize iterations
V_params = (beta, sigma)


while (VFdist > VFtol) and (VFiter < VFmaxiter):
    Vstore[:, VFiter] = V
    TV, optM = functions.bellman_operator(V, m_grid, P_grid, V_params)
    VFdist = (np.absolute(V - TV)).max()
    print('Iteration: ', VFiter, ', distance: ', VFdist)
    V = TV
    VFiter += 1

if VFiter < VFmaxiter:
    print('Value function converged after ', VFiter, ' iterations.')

else:
    print('Value function did not converge :(')

VF = V

optC = (m_grid - optM) / p

plt.figure()
plt.plot(m_grid[1:], VF[1:])
