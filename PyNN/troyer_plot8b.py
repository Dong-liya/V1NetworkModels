import numpy as np
import matplotlib.pyplot as plt
from kernel_functions import gabor_kernel
from connector_functions import gabor_probability
from scipy.stats.stats import pearsonr
from misc_functions import circular_dist, normal_function


# Gabor parameters
w = 0.8
phi = 0
gamma = 1  # Aspect ratio
sigma = 1
theta = 0



# Space parameters
dx = 0.1
lx = 6.0
dy = 0.1
ly = 6.0

xc = 0
yc = 0

size_x = 0.75
size_y = 0.75

x_values = np.arange(-size_x/2, size_x/2, dx)
y_values = np.arange(-size_y/2, size_y/2, dy)

points = 50
orientation_sigma = 15
phase_sigma = 30
n_pick = 15

phis = np.linspace(-90, 270, points)
thetas = np.linspace(-90, 90, points)

correlation_phi = np.zeros(phis.size)
correlation_phi_inh = np.zeros(phis.size)
correlation_theta = np.zeros(thetas.size)
correlation_phi_normal = np.zeros(phis.size)
correlation_phi_normal_inh = np.zeros(phis.size)
correlation_theta_normal = np.zeros(thetas.size)

Z1 = gabor_kernel(lx, dx, ly, dy, sigma, gamma, phi, w, theta, xc, yc)

# Phase

for index, phi2 in enumerate(phis):
    Z2 = gabor_kernel(lx, dx, ly, dy, sigma, gamma, phi2, w, theta, xc, yc)

    correlation = pearsonr(Z1.flat, Z2.flat)[0]
    correlation_phi[index] = np.sum(np.random.rand(n_pick) < correlation)
    correlation_phi_inh[index] = np.sum(np.random.rand(n_pick) < -correlation)

# Orientations

for index, theta2 in enumerate(thetas):
    Z2 = gabor_kernel(lx, dx, ly, dy, sigma, gamma, phi, w, theta2, xc, yc)

    correlation = pearsonr(Z1.flat, Z2.flat)[0]
    correlation_theta[index] = np.sum(np.random.rand(n_pick) < correlation)


for index, phi2 in enumerate(phis):
    or_distance = circular_dist(theta, theta, 180)
    phase_distance = circular_dist(phi, phi2, 360)
    phase_distance_inh = 180 - circular_dist(phi, phi2, 360)

    or_gauss = normal_function(or_distance, mean=0, sigma=orientation_sigma)
    phase_gauss = normal_function(phase_distance, mean=0, sigma=phase_sigma)
    phase_gauss_inh = normal_function(phase_distance_inh, mean=0, sigma=phase_sigma)

    # Now normalize by guassian in zero
    or_gauss = or_gauss / normal_function(0, mean=0, sigma=orientation_sigma)
    phase_gauss = phase_gauss / normal_function(0, mean=0, sigma=phase_sigma)
    phase_gauss_inh = phase_gauss_inh / normal_function(0, mean=0, sigma=phase_sigma)

    # Probability is the product
    probability = or_gauss * phase_gauss
    probability_inh = or_gauss * phase_gauss_inh
    correlation_phi_normal[index] = np.sum(np.random.rand(n_pick) < probability)
    correlation_phi_normal_inh[index] = np.sum(np.random.rand(n_pick) < probability_inh)


for index, theta2 in enumerate(thetas):
    or_distance = circular_dist(theta, theta2, 180)
    phase_distance = circular_dist(phi, phi, 360)

    or_gauss = normal_function(or_distance, mean=0, sigma=orientation_sigma)
    phase_gauss = normal_function(phase_distance, mean=0, sigma=phase_sigma)

    # Now normalize by guassian in zero
    or_gauss = or_gauss / normal_function(0, mean=0, sigma=orientation_sigma)
    phase_gauss = phase_gauss / normal_function(0, mean=0, sigma=phase_sigma)

    # Probability is the product
    probability = or_gauss * phase_gauss
    correlation_theta_normal[index] = np.sum(np.random.rand(n_pick) < probability)

y_min = 1.3
y_max = -1.3

# Phis correlation mechanism

plt.subplot(2, 2, 1)
plt.title('Correlation with varying phi')
plt.plot(phis, correlation_phi/np.max(correlation_phi), 'b')
plt.plot(phis, -correlation_phi_inh/np.max(correlation_phi_inh), 'r')
plt.ylim([y_min, y_max])
plt.xlabel('Phase differences (degrees)')
#plt.grid()

# Thetas correlation mechanism

plt.subplot(2, 2, 2)
plt.title('Correlation with varying theta')
plt.plot(thetas, correlation_theta/np.max(correlation_theta), 'b')
plt.plot(thetas, -correlation_theta/np.max(correlation_theta), 'r')
plt.ylim([y_min, y_max])
plt.xlabel('Orientation differences (degrees)')
#plt.grid()

# Phis correlation polar scheme

plt.subplot(2, 2, 3)
plt.title('Correlation with varying phi polar scheme')
plt.plot(phis, correlation_phi_normal/ np.max(correlation_phi_normal), 'b')
plt.plot(phis, -correlation_phi_normal_inh / np.max(correlation_phi_normal_inh), 'r')
plt.ylim([y_min, y_max])
plt.xlabel('Phase differences (degrees)')
#plt.grid()

plt.subplot(2, 2, 4)
plt.title('Correlation with varying theta polar scheme')
plt.plot(thetas, correlation_theta_normal/np.max(correlation_theta_normal), 'b')
plt.plot(thetas, -correlation_theta_normal / np.max(correlation_theta_normal), 'r')
plt.ylim([y_min, y_max])
plt.xlabel('Orientation differences (degrees)')
plt.plot
#plt.grid()


plt.show()