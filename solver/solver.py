import numpy as np

class RichardsonSolver:
    """
    Richardson iteration for SPD matrices:
        x_{k+1} = x_k + tau * (b - A x_k),   0 < tau < 2 / lmax(A)

    Args:
        tau: optional fixed step. If None and (lmin, lmax) are given, uses 2/(lmin+lmax).
        lmin, lmax: optional spectral bounds for SPD A.
        tol: relative residual tolerance ||b - A x|| / ||b||
        max_iter: maximum iterations
        store_history: keep residual norms if True
    """
    def __init__(self, tau=None, lmin=None, lmax=None, *, tol=1e-8, max_iter=10_000, store_history=False):
        self.tau = tau
        self.lmin = lmin
        self.lmax = lmax
        self.tol = tol
        self.max_iter = max_iter
        self.store_history = store_history

    def _choose_tau(self, A, r):
        if self.tau is not None:
            return float(self.tau)
        if self.lmin and self.lmax and self.lmin > 0 and self.lmax > 0:
            return 2.0 / (self.lmin + self.lmax)
        if self.lmax and self.lmax > 0:
            return 1.0 / self.lmax
        raise ValueError("Cannot choose tau: provide tau or spectral bounds")

    def solve(self, A, b, x0=None):
        """
        Returns:
            (x, res, converged, iters, history_or_None)
        """
        A = np.asarray(A, float)
        b = np.asarray(b, float).reshape(-1)
        n = b.size
        if A.shape != (n, n):
            raise ValueError("A must be square and match b dimension")
        x = np.zeros_like(b) if x0 is None else np.asarray(x0, float).reshape(-1)

        b_norm = y if (y := np.linalg.norm(b)) > 0 else 1.0
        hist = [] if self.store_history else None

        for k in range(1, self.max_iter + 1):
            r = b - A @ x
            tau = self._choose_tau(A, r)
            x = x + tau * r
            res = np.linalg.norm(b - A @ x) / b_norm
            if hist is not None:
                hist.append(float(res))
            if res <= self.tol:
                return x, res, True, k, (hist if hist is not None else None)
        res = np.linalg.norm(b - A @ x) / b_norm
        # not converged
        return x, res, False, self.max_iter, (hist if hist is not None else None)
