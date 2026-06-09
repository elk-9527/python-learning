import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 1. 定义迭代格式
def phi_newton(x): return 0.5 * (x + 2/x)
def phi_linear(x): return x - 0.2 * (x**2 - 2)
def phi_oscillate(x): return 2/x
def phi_diverge(x): return x**2 + x - 2

formats = {
    "Newton (Quadratic)": phi_newton,
    "Relaxation (Linear)": phi_linear,
    "Oscillating": phi_oscillate,
    "Divergent": phi_diverge
}

def run_experiment(phi, x0, true_val=np.sqrt(2), max_iter=50, tol=1e-12):
    history = [x0]
    status = "Converged"
    for i in range(max_iter):
        try:
            x_next = phi(history[-1])
            if np.isinf(x_next) or np.isnan(x_next) or abs(x_next) > 1e10:
                status = "Diverged/Overflow"
                break
            history.append(x_next)
            if abs(x_next - history[-2]) < tol:
                break
        except:
            status = "Error"
            break
    else:
        status = "Max Iteration Reached"
    
    iters = len(history) - 1
    errors = [abs(x - true_val) for x in history]
    rel_errors = [abs(x - true_val)/true_val for x in history]
    return history, errors, rel_errors, status

# 2. 执行实验
initial_values = [2.0, 1.0, -2.0]
results_all = []

plt.figure(figsize=(12, 8))

for name, phi in formats.items():
    for x0 in initial_values:
        seq, errs, rel_errs, status = run_experiment(phi, x0)
        results_all.append({
            "Method": name, "x0": x0, "Iters": len(seq)-1, 
            "Final_x": seq[-1], "Status": status
        })
        
        if status == "Converged" or name == "Relaxation (Linear)":
            plt.semilogy(errs, label=f"{name} (x0={x0})")

plt.title("Error Decay (Semi-log Plot)")
plt.xlabel("Iteration Step")
plt.ylabel("Absolute Error")
plt.legend()
plt.grid(True)
plt.show()

# 3. 打印结果表
df = pd.DataFrame(results_all)
print(df.to_string(index=False))