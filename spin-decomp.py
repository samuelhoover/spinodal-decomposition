# pyright: basic

import glob
import shutil
import os

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

from PIL import Image
from scipy.ndimage import laplace

SEED: int = 42  # change this for different outcomes


class CahnHilliard:
    def __init__(
        self,
        N: int = 100,
        p: float = 0,
        D: float = 1,
        gamma: float = 0.5,
        num_iter: int = 5000,
        dt: float = 0.001,
        frame_iter: int = 10,
    ) -> None:
        self.N = N
        self.p = p
        self.D = D
        self.gamma = gamma
        self.num_iter = num_iter
        self.dt = dt
        self.frame_iter = frame_iter

    # Cahn-Hilliard equation
    def CH_eqn(
        self, c: npt.NDArray[np.float64], D: float, gamma: float
    ) -> npt.NDArray[np.float64]:
        return D * laplace(
            input=(c**3) - c - (gamma * laplace(input=c, mode="wrap")), mode="wrap"
        )

    # Initialize random data on a 2d square lattice
    def initialize_lattice(self) -> npt.NDArray[np.float64]:
        rng = np.random.default_rng(seed=SEED)
        return rng.choice(
            [-1, 1], (self.N, self.N), p=[0.5 + (self.p / 2), 0.5 - (self.p / 2)]
        )

    # forward Euler method for solving ODEs
    def forward_euler(self, x, func, dt, *fargs) -> npt.NDArray[np.float64]:
        return x + func(*fargs) * dt

    # solver function
    def solve(self) -> npt.NDArray[np.float64]:
        c: npt.NDArray[np.float64] = self.initialize_lattice()
        t = 0

        _, ax = plt.subplots()
        self.plot_lattice(c, ax, t, i=0)
        for i in range(1, self.num_iter + 1):
            fargs: tuple[npt.NDArray[np.float64], float, float] = (
                c,
                self.D,
                self.gamma,
            )
            ax.clear()
            c: npt.NDArray[np.float64] = self.forward_euler(
                c, self.CH_eqn, self.dt, *fargs
            )
            t = np.round(t + self.dt, 6)
            if i % self.frame_iter == 0:
                self.plot_lattice(c, ax, t, i)
        return c

    # create snapshot at time t
    def plot_lattice(self, c, ax, t, i) -> None:
        ax.imshow(c)
        ax.set_xticks([], [])
        ax.set_yticks([], [])
        ax.annotate(
            f"$t = {t:.3f}$",
            xy=(0.05, 0.95),
            xycoords="axes fraction",
            bbox={
                "color": "white",
                "alpha": 0.8,
                "boxstyle": "Round",
                "edgecolor": None,
            },
            ha="left",
            va="top",
            fontsize=14,
        )
        plt.tight_layout()

        # save snapshot
        if not os.path.exists("gifs/tmp"):
            os.makedirs("gifs/tmp")
        plt.savefig(f"gifs/tmp/{i:06d}.png")

        if i in [0, self.num_iter]:
            plt.savefig(
                f"gifs/{i:06d}-spin-decomp-d_{self.D}-gamma_{self.gamma}-p_{self.p}.pdf"
            )

    # create animation from snapshots
    def animate(self) -> None:
        path_in: str = "gifs/tmp/*.png"
        path_out: str = f"gifs/spin-decomp-d_{self.D}-gamma_{self.gamma}-p_{self.p}.gif"
        imgs: list[Image.Image] = []

        # grab all snapshots
        for f in sorted(glob.glob(path_in)):
            img: Image.Image = Image.open(f)
            imgs.append(img.copy())
            img.close()

        # convert snapshots to GIF
        imgs[0].save(
            fp=path_out,
            format="GIF",
            append_images=imgs[1:],
            save_all=True,
            optimize=True,
            duration=1,
            loop=0,
        )

        # delete snapshots
        if os.path.exists("gifs/tmp"):
            shutil.rmtree("gifs/tmp/")


def main(
    N: int, p: float, D: float, gamma: float, num_iter: int, dt: float, frame_iter: int
) -> None:
    ch: CahnHilliard = CahnHilliard(N, p, D, gamma, num_iter, dt, frame_iter)
    ch.solve()
    ch.animate()


if __name__ == "__main__":
    N: int = 500
    p: float = 0.6
    D: float = 200
    gamma: float = 0.5
    num_iter: int = 100000
    dt: float = 0.0002
    frame_iter: int = 100
    print("Beginning calculation ...\n")
    print(f"N: {N}\np: {p}\nD: {D}\ngamma: {gamma}\ndt: {dt}\n")
    main(N, p, D, gamma, num_iter, dt, frame_iter)
    print("\nDone!")
