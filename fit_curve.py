"""
Assignment for Research and Development / AI
--------------------------------------------
Estimate unknown parameters (θ, M, X) from the given parametric curve:
    x = (t*cos(θ) - e^(M*t)*sin(0.3*t)*sin(θ)) + X
    y = (42 + t*sin(θ) + e^(M*t)*sin(0.3*t)*cos(θ))

Dataset: xy_data.csv
Parameter range: 6 < t < 60
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import math

# --- Load data ---
data = pd.read_csv("xy_data.csv")
x_data, y_data = data["x"].values, data["y"].values
t = np.linspace(6, 60, len(data))  # parameter t range

# --- Define parametric model ---
def curve_model(t, theta_deg, M, X):
    theta = np.radians(theta_deg)
    x = (t * np.cos(theta) - np.exp(M * t) * np.sin(0.3 * t) * np.sin(theta)) + X
    y = (42 + t * np.sin(theta) + np.exp(M * t) * np.sin(0.3 * t) * np.cos(theta))
    return np.concatenate([x, y])  # concatenated x,y for joint fitting

# --- Prepare data for fitting ---
xy_concat = np.concatenate([x_data, y_data])

# --- Initial guess & bounds ---
initial_guess = [20, 0.0, 50]  # θ (deg), M, X
bounds = ([0, -0.05, 0], [50, 0.05, 100])

# --- Fit model ---
params, covariance = curve_fit(curve_model, t, xy_concat, p0=initial_guess, bounds=bounds)
theta_fit, M_fit, X_fit = params
std_devs = np.sqrt(np.diag(covariance))

# --- Print results ---
print("Estimated Parameters:")
print(f"Theta (°): {theta_fit:.4f} ± {std_devs[0]:.4f}")
print(f"M: {M_fit:.4f} ± {std_devs[1]:.4f}")
print(f"X: {X_fit:.4f} ± {std_devs[2]:.4f}")

# --- Compute predicted curve ---
theta_rad = math.radians(theta_fit)
x_pred = (t * np.cos(theta_rad) - np.exp(M_fit * t) * np.sin(0.3 * t) * np.sin(theta_rad)) + X_fit
y_pred = (42 + t * np.sin(theta_rad) + np.exp(M_fit * t) * np.sin(0.3 * t) * np.cos(theta_rad))

# --- Visualization ---
plt.figure(figsize=(8, 6))
plt.scatter(x_data, y_data, color='blue', label='Actual Data', alpha=0.7)
plt.plot(x_pred, y_pred, color='red', linewidth=2, label='Fitted Curve')
plt.title("Parametric Curve Fit: Comparison of Actual vs Predicted", fontsize=13)
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Desmos/LaTeX-ready output ---
print("\nDesmos format:")
print(f"( (t*cos({theta_rad:.6f})-e^({M_fit:.4f}*t)*sin(0.3*t)*sin({theta_rad:.6f}))+{X_fit:.4f} , "
      f"42+t*sin({theta_rad:.6f})+e^({M_fit:.4f}*t)*sin(0.3*t)*cos({theta_rad:.6f}) ), 6<t<60 )")

