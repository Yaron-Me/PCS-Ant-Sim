# This script fits a reciprocal function to the data and plots the fitted curve and the original data points

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

plt.rc('font', size=17)

# Given data
antamounts = ["10", "25", "50", "100", "500", "1000"]

data_10x10 = np.array([70.51687503, 33.49537697, 21.56392872, 15.22595244, 8.68999014, 7.51073394])
data_15x15 = np.array([186.97949411, 101.32731153, 65.77109136, 46.54486119, 28.06822419, 24.86951389])
data_20x20 = np.array([202.64502983, 100.80075394, 73.25084322, 54.09197419, 31.99877975, 28.57584328])

maze_sizes = ["10x10", "15x15", "20x20"]

# Concatenate all data into a single array
all_data = np.concatenate([data_10x10, data_15x15, data_20x20])

# Convert antamounts to integers
antamounts_int = list(map(int, antamounts))


# Define a reciprocal function to fit the data
def reciprocal_function(x, a, b):
    return a / x + b


# Fit the curve to the data
params_10x10, covariance_10x10 = curve_fit(reciprocal_function, antamounts_int, data_10x10, p0=[1, 1])
params_15x15, covariance_15x15 = curve_fit(reciprocal_function, antamounts_int, data_15x15, p0=[1, 1])
params_20x20, covariance_20x20 = curve_fit(reciprocal_function, antamounts_int, data_20x20, p0=[1, 1])

# Generate x values for plotting
x_values = np.linspace(min(antamounts_int), max(antamounts_int), 100)

# Plot the original data points
plt.scatter(antamounts_int, data_10x10, label="10x10", color='red')
plt.scatter(antamounts_int, data_15x15, label="15x15", color='green')
plt.scatter(antamounts_int, data_20x20, label="20x20", color='blue')

tenbyten = f"f(x) = {params_10x10[0]:.2f} / (x + {params_10x10[1]:.2f})"
fifteenbyfifteen = f"f(x) = {params_15x15[0]:.2f} / (x + {params_15x15[1]:.2f})"
twentybytwenty = f"f(x) = {params_20x20[0]:.2f} / (x + {params_20x20[1]:.2f})"

# Plot the fitted curves
plt.plot(x_values, reciprocal_function(x_values, *params_10x10), '--', label=tenbyten, color='red')
plt.plot(x_values, reciprocal_function(x_values, *params_15x15), '--', label=fifteenbyfifteen, color='green')
plt.plot(x_values, reciprocal_function(x_values, *params_20x20), '--', label=twentybytwenty, color='blue')

print("Fitted Function for 10x10: f(x) =", f"{params_10x10[0]:.2f} / (x + {params_10x10[1]:.2f})")
print("Fitted Function for 15x15: f(x) =", f"{params_15x15[0]:.2f} / (x + {params_15x15[1]:.2f})")
print("Fitted Function for 20x20: f(x) =", f"{params_20x20[0]:.2f} / (x + {params_20x20[1]:.2f})")

# Generate more ant amounts for prediction
additional_antamounts = np.array([200, 300, 400, 600, 800, 1200])

# Predict values using the fitted function
predictions_10x10 = reciprocal_function(additional_antamounts, *params_10x10)
predictions_15x15 = reciprocal_function(additional_antamounts, *params_15x15)
predictions_20x20 = reciprocal_function(additional_antamounts, *params_20x20)

# Plot the predicted points
plt.scatter(additional_antamounts, predictions_10x10, marker='x', color='red', label="Predicted 10x10")
plt.scatter(additional_antamounts, predictions_15x15, marker='x', color='green', label="Predicted 15x15")
plt.scatter(additional_antamounts, predictions_20x20, marker='x', color='blue', label="Predicted 20x20")

plt.xlabel("Ant Colony Size")
plt.ylabel("Time in hours")
plt.legend()
plt.show()
