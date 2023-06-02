# Usage
Run `python spin-decomp.py` to generate animations for the time evolution of the Cahn-Hilliard equation using the forward Euler method.

Set the model parameters in the `CahnHilliard` call in the `main()` function.

$D = 100$, $\gamma = 0.5$, and 50/50 mixture ($p = 0$). <br>
<img src='figs/spinodal-decomposition_D-100_gamma-0.5_p-0.gif' width='400' />

$D = 100$, $\gamma = 0.5$, and 70/30 mixture ($p = 0.4$) with Ostwald ripening evident.<br>
<img src='figs/spinodal-decomposition_D-100_gamma-0.5_p-0.4.gif' width='400' />

# Dependencies
NumPy v1.24.3 <br>
SciPy v1.7.3 <br>
Matplotlib v3.7.1 <br>
Pillow v9.4.0 <br>
tqdm v4.65.0
