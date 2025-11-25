import numpy as np
import matplotlib.pyplot as plt
import math

# 1. Metode Bisection
def bisection_method(func, x_low, x_high, tolerance=1e-6, max_iterations=100):
    f_low = func(x_low)
    f_high = func(x_high)

    if f_low * f_high > 0:
        return None  # Tidak ada akar dalam interval

    for _ in range(max_iterations):
        x_mid = 0.5 * (x_low + x_high)
        f_mid = func(x_mid)

        if abs(f_mid) < tolerance or (x_high - x_low) < tolerance:
            return x_mid

        if f_low * f_mid < 0:
            x_high = x_mid
            f_high = f_mid
        else:
            x_low = x_mid
            f_low = f_mid

    return x_mid

# 2. Parameter Input
TISSERAND_PARAM = 3        # Nilai T_p
INCLINATION_DEG = 0        # Inklinasi orbit (derajat)
COS_I           = math.cos(math.radians(INCLINATION_DEG))

# Sumbu semi-mayor planet (AU)
PLANET_A = {
    0.387: "Merkurius",
    0.723: "Venus",
    1.000: "Bumi",
    1.524: "Mars",
    5.203: "Jupiter",
    9.537: "Saturnus"
}

# Rentang eksentrisitas
E_VALUES = np.linspace(0, 0.6, 6000)

# 3. Equation Solver untuk x menggunakan Bisection
def compute_x_values(T_p, cos_i, e):
    def equation(x):
        return 2 * cos_i * x**3 - T_p * x**2 + (1 - e**2)

    # Dua akar dengan interval berbeda
    root1 = bisection_method(equation, 0.05, 1.0)
    root2 = bisection_method(equation, 1.001, 3.0)

    return root1, root2

# 4. Plotting Per Planet
def plot_per_planet(a_planet, planet_name, color):
    a1_results = []
    a2_results = []

    for e in E_VALUES:
        x1, x2 = compute_x_values(TISSERAND_PARAM, COS_I, e)
        a1_results.append((x1**2 * a_planet) / (1 - e**2) if x1 is not None else None)
        a2_results.append((x2**2 * a_planet) / (1 - e**2) if x2 is not None else None)

    plt.figure(figsize=(8, 5))
    plt.plot(a1_results, E_VALUES, linestyle='-', color=color, label=f"{planet_name} (x1)")
    plt.plot(a2_results, E_VALUES, linestyle='-', color=color, label=f"{planet_name} (x2)")
    plt.xlabel("Sumbu Semi-Mayor (a)")
    plt.ylabel("Eksentrisitas (e)")
    plt.title(f"Grafik Tisserand untuk {planet_name} (T_p={TISSERAND_PARAM}, i={INCLINATION_DEG}°) (Metode Bisection)")
    plt.grid(True)
    plt.legend()
    plt.xlim(0, 30 if a_planet > 1.524 else 10)
    plt.ylim(0, 0.6)
    plt.show()

    return a1_results, a2_results

# 5. Plot Gabungan Semua Planet
def plot_combined(all_a1, all_a2, labels, colors):
    plt.figure(figsize=(10, 6))

    for idx in range(len(all_a1)):
        plt.plot(all_a1[idx], E_VALUES, linestyle='-', color=colors[idx], label=labels[idx])
        plt.plot(all_a2[idx], E_VALUES, linestyle='-', color=colors[idx])

    plt.xlabel("Sumbu Semi-Mayor (a)")
    plt.ylabel("Eksentrisitas (e)")
    plt.title(f"Grafik Parameter Tisserand untuk Semua Planet {TISSERAND_PARAM}, i={INCLINATION_DEG}°) (Metode Bisection)")
    plt.grid(True)
    plt.legend()
    plt.xlim(0, 30)
    plt.ylim(0, 0.6)
    plt.show()

# 6. Main Program
def main():
    colors = ['b', 'g', 'r', 'c', 'm', 'y']

    all_a1_values = []
    all_a2_values = []
    labels = []

    for idx, (a_planet, planet_name) in enumerate(PLANET_A.items()):
        color = colors[idx % len(colors)]
        a1, a2 = plot_per_planet(a_planet, planet_name, color)

        all_a1_values.append(a1)
        all_a2_values.append(a2)
        labels.append(planet_name)

    plot_combined(all_a1_values, all_a2_values, labels, colors)

# Program Start
if __name__ == "__main__":
    main()
