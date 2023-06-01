import glob

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from scipy.ndimage import laplace
from tqdm import trange


def initialize_lattice(N, p):
    rng = np.random.default_rng(seed=42)
    return rng.choice([-1, 1], (N, N), p=[0.5 + (p / 2), 0.5 - (p / 2)])


def plot_lattice(c, ax, t, i):
    im = ax.imshow(c)
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    # ax.set_title(f'$t = {t:.3f}$')
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
    path_out = 'figs/spinodal-decomposition.gif'

    imgs = []
    for f in sorted(glob.glob(path_in)):
        img = Image.open(f)
        imgs.append(img.copy())
        img.close()
    imgs[0].save(
        fp=path_out, format='GIF', append_images=imgs[1:],
        save_all=True, duration=1, loop=0,
    )


if __name__ == "__main__":
    main(N=200, p=0.2, D=10, gamma=0.5, num_iter=25000, dt=0.0001, frame_iter=100)
