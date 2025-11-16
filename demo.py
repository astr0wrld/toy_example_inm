import numpy as np
from solver import RichardsonSolver
import matplotlib.pyplot as plt

np.random.seed(7)
Q, _ = np.linalg.qr(np.random.randn(5, 5))
lambdas = np.linspace(1.0, 12.0, 5)
A = Q @ np.diag(lambdas) @ Q.T
x_true = np.random.randn(5)
print("\nTrue solution x*:", x_true)
b = A @ x_true

# Save A and b to CSV files
np.savetxt("A.csv", A, delimiter=",")
np.savetxt("b.csv", b, delimiter=",")

# Load A and b from CSV files
A_csv = np.loadtxt("A.csv", delimiter=",")
b_csv = np.loadtxt("b.csv", delimiter=",").reshape(-1)

solver = RichardsonSolver(
    lmin=float(lambdas.min()),
    lmax=float(lambdas.max()),
    tol=1e-10,
    max_iter=200_000,
    store_history=True,
)

x, rel_res, ok, iters, hist = solver.solve(A_csv, b_csv)

print("Converged:", ok, "iters:", iters, "rel_res:", f"{rel_res:.3e}",
      "||x - x*||:", f"{np.linalg.norm(x - x_true):.3e}", "solution x:", x, sep="\n")

plt.figure()
plt.semilogy(hist)
plt.xlabel("Iteration")
plt.ylabel("Relative Residual")
plt.title("Convergence History")
plt.grid(True)
plt.savefig("convergence.png")
print("\nWrote convergence plot to convergence.png")

np.savetxt("x.csv", x, delimiter=",")
print("\nWrote solution to x.csv\n")