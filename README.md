# Usage
Run `python spin-decomp.py` to generate animations for the time evolution of the Cahn-Hilliard equation using the forward Euler method.

Pass the model parameters into the `main()` function.  

$D = 100$, $\gamma = 0.5$, and 50/50 mixture ($p = 0$).  
<p>
  <img src='/gifs/spin-decomp-D_100-gamma_0.5-p_0.gif' width='400' />
</p>

$D = 100$, $\gamma = 0.5$, and 70/30 mixture ($p = 0.4$) with Ostwald ripening evident.  
<p>
  <img src='gifs/spin-decomp-D_100-gamma_0.5-p_0.4.gif' width='400' />
</p>

# Dependencies
NumPy  
SciPy  
Matplotlib  
Pillow  
