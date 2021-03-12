import matplotlib.pyplot as plt
import numpy as np

# Task 1

# We approximate the derivative in the ODE with the forward difference
# operator, and rearrange to give an expression for P(t + dt) in terms
# of P(t):
#
# (P(t + dt) - P(t)) / dt = k * P(t) * (1 - P(t) / K) - m
# 
# => P(t + dt) = dt * (k * P(t) * (1 - P(t) / K) - m) + P(t)
#
# Starting from the known initial condition P(t=0) = P0,
# we can now compute P(dt); then, we can use P(dt) to compute
# P(2dt); then, use that to compute P(3dt); etc.

# Set model parameters
k = 0.1
K = 1000
m = 10
P0 = range(300, 1501, 300)

# Set simulation parameters
dt = 1/7
n_weeks = 52 * 5
nmax = int(n_weeks / dt)

# We store the solution values for each P0 in a different row
P = np.zeros([len(P0), nmax])

# Initial conditions
P[:, 0] = P0

# Prepare the plot
time = np.linspace(0, n_weeks, nmax)
fig, ax = plt.subplots()

# Run simulation for all values of P0
for i in range(len(P0)): 
    # Forward Euler
    for n in range(1, nmax):
        P[i, n] = (k*P[i, n-1]*(1 - P[i, n-1]/K) - m)*dt + P[i, n-1]

        # Stop if population reaches zero
        if P[i, n] <= 0:
            break

    # Plot the results
    ax.plot(time, P[i, :], label=f'P0 = {P0[i]}')

ax.set(xlabel='Time (weeks)', ylabel='Population')
ax.legend()
plt.show()


# Task 2

fig, ax = plt.subplots()

# Set test values for m
m = np.arange(10, 31)

# Initialise the array -- each row corresponds to a value of m
P0 = 500
P = np.zeros([len(m), nmax])
P[:, 0] = P0

# Run the simulation for all values of m
for i in range(len(m)):
    # Forward Euler
    for n in range(1, nmax):
        P[i, n] = (k*P[i, n-1]*(1 - P[i, n-1]/K) - m[i])*dt + P[i, n-1]

        # Stop if population reaches zero
        if P[i, n] <= 0:
            break

    # Display the results
    ax.plot(time, P[i, :], label=f'm = {m[i]}')

ax.set(xlabel='Time (weeks)', ylabel='Population')
ax.legend()
plt.show()


# Bonus task: backward Euler
#
# Replacing the derivative in the ODE with the backward difference
# operator leads to a quadratic equation in P(t). This time P(t-dt)
# is known but P(t) is the unknown.

# One of the roots is negative, which is irrelevant as we are computing
# a population of fish which is positive. We calculate the positive root
# at every time step.

# Set model parameters
k = 0.1
K = 1000
m = 10
P0 = 500

# Set simulation parameters, increase dt to see difference
dt = 1
n_weeks = 52 * 5
nmax = int(n_weeks / dt)

# Initial conditions
P = np.zeros([2, nmax])
P[:, 0] = P0

# Quadratic coefficients
a = dt * k / K
b = 1 - k * dt

# Forward and backward Euler
for n in range(1, nmax):
    # Forward Euler
    P[0, n] = (k*P[0, n-1]*(1 - P[0, n-1]/K) - m)*dt + P[0, n-1]

    # Backward Euler
    # Calculate the positive root
    c = m * dt - P[1, n-1]
    sqrt_delta = np.sqrt(b**2 - 4*a*c)
    P[1, n] = (-b + sqrt_delta) / (2*a)

    # Stop if population reaches zero
    if P[0, n] <= 0 and P[1, n] <= 0:
        break

# Plot the results
fig, ax = plt.subplots()
time = np.linspace(0, n_weeks, nmax)

ax.plot(time, P[0, :], '-', label='Forward Euler')
ax.plot(time, P[1, :], '--', label='Backward Euler')

ax.set(xlabel='Time (weeks)', ylabel='Population', xlim=[0, n*dt])
ax.legend()
plt.show()
