import glob
import os

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from scipy.ndimage import laplace
from tqdm import trange


class CahnHilliard:
    def __init__(self, N=100, p=0, num_iter=5000, D=1, gamma=0.5, dt=0.001, frame_iter=10):
        self.N = N
        self.p = p
        self.num_iter = num_iter
        self.D = D
        self.gamma = gamma
        self.dt = dt
        self.frame_iter = frame_iter

    # Cahn-Hilliard equation
    def CH_eqn(self,c, D, gamma):
        return D * laplace((c ** 3) - c - (gamma * laplace(c, mode='wrap')), mode='wrap')

    # Initialize random data on a 2d square lattice
    def initialize_lattice(self):
        rng = np.random.default_rng(seed=42)
        return rng.choice([-1, 1], (self.N, self.N), 
                          p=[0.5 + (self.p / 2), 0.5 - (self.p / 2)])

    # forward Euler method for solving ODEs
    def forward_euler(self, x, func, dt, *fargs):
        return x + func(*fargs) * dt

    # solver function
    def solve(self):
        c = self.initialize_lattice()
        t = 0

        fig, ax = plt.subplots() 
        self.plot_lattice(c, ax, t, 0)
        for i in trange(1, self.num_iter + 1):
            fargs = (c, self.D, self.gamma)
            ax.clear()
            c = self.forward_euler(c, self.CH_eqn, self.dt, *fargs)
            t = np.round(t + self.dt, 6)
            if i % self.frame_iter == 0:
                self.plot_lattice(c, ax, t, i)
        return c

    # create snapshot at time t
    def plot_lattice(self, c, ax, t, i):
        im = ax.imshow(c)
        ax.set_xticks([], [])
        ax.set_yticks([], [])
        ax.annotate(
            f'$t = {t:.3f}$', xy=(0.05, 0.95), xycoords='axes fraction',
            bbox={'color': 'white', 'alpha': 0.8, 
                  'boxstyle': 'Round', 'edgecolor': None}, 
            ha='left', va='top', fontsize=14
        )
        plt.tight_layout() 
        plt.savefig(f'figs/{i:06d}.png')

    # create animation from snapshots
    def animate(self):
        # generate gif from snapshots
        path_in = 'figs/*.png'
        path_out = f'figs/spinodal-decomposition_D-{self.D}_gamma-{self.gamma}_p-{self.p}.gif'
        imgs = []
        for f in sorted(glob.glob(path_in)):
            img = Image.open(f)
            imgs.append(img.copy())
            img.close()
        imgs[0].save(
            fp=path_out, format='GIF', append_images=imgs[1:],
            save_all=True, duration=1, loop=0,
        )

        # delete snapshots, keep animation
        for f in os.listdir('figs'):
            if f.endswith('.png'):
                os.remove(os.path.join('figs', f))


<<<<<<< HEAD

def main():
    ch = CahnHilliard(
        N=200, p=0.4, D=100, gamma=0.5, 
        num_iter=50000, dt=0.0001, frame_iter=100
    ) 
    ch.solve()
    ch.animate()
=======
def plot_lattice(c, ax, t, i):
    im = ax.imshow(c)
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    ax.annotate(
        f'$t = {t:.3f}$', xy=(0.05, 0.95), xycoords='axes fraction',
        bbox={'color': 'white', 'alpha': 0.8,
              'boxstyle': 'Round', 'edgecolor': None},
        ha='left', va='top', fontsize=14
    )
    plt.savefig(f'figs/{i:06d}.png')
 

def forward_euler(x, func, dt, *fargs):
    return x + func(*fargs) * dt


def cahn_hilliard(c, D, gamma):
    x = c ** 3
    y = c
    z = gamma * laplace(c, mode='wrap')
    return D * laplace(x - y - z, mode='wrap')


def solve(c, num_iter, D, gamma, dt, frame_iter):
    fig, ax = plt.subplots()
    t = 0

    plot_lattice(c, ax, t, 0)
    for i in trange(1, num_iter + 1):
        fargs = (c, D, gamma)
        ax.clear()
        c = forward_euler(c, cahn_hilliard, dt, *fargs)
        t = np.round(t + dt, 6)
        if i % frame_iter == 0:
            plot_lattice(c, ax, t, i)
    return c


def main(N=100, p=0, num_iter=1000, D=1, gamma=0.5, dt=0.001, frame_iter=10):
    c = initialize_lattice(N, p)
    solve(c, num_iter, D, gamma, dt, frame_iter)
    
    # generate gif from snapshots
    path_in = 'figs/*.png'
    path_out = f'figs/spinodal-decomposition_D-{D}_gamma-{gamma}_p-{p}.gif'
    imgs = []
    for f in sorted(glob.glob(path_in)):
        img = Image.open(f)
        imgs.append(img.copy())
        img.close()
    imgs[0].save(
        fp=path_out, format='GIF', append_images=imgs[1:],
        save_all=True, duration=1, loop=0,
    )
>>>>>>> master

    # delete snapshots, keep .gif
    for f in os.listdir('figs'):
        if f.endswith('.png'):
            os.remove(os.path.join('figs', f))


if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main(N=200, p=0.4, D=100, gamma=0.5, num_iter=50000, dt=0.0001, frame_iter=100)
>>>>>>> master
