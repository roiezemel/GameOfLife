from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.signal import convolve

KERNEL = np.ones((3, 3), dtype=int)
KERNEL[1, 1] = 0


def update_grid(data, copy_data, cax, ax, fig):
    copy_data[:] = data[:]
    counts = np.round(convolve(data, KERNEL, 'same'))
    data[copy_data & (counts != 2) & (counts != 3)] = 0
    data[np.bitwise_not(copy_data) & (counts == 3)] = 1

    cax.set_data(data)
    fig.canvas.blit(ax.bbox)


def finite_space_animation(initial_config: np.ndarray[int], ax, fig, grid_size):
    # Create an initial grid
    grid_size = [grid_size] * 2
    data = np.zeros(grid_size, dtype=bool)
    copy_data = np.zeros(grid_size, dtype=bool)

    data[:] = initial_config
    cax = ax.imshow(data, cmap='gray', interpolation='nearest', vmin=0, vmax=1)
    cax.set_data(data)

    # Create a background frame for blitting
    fig.canvas.copy_from_bbox(ax.bbox)
    return FuncAnimation(fig, lambda frame: update_grid(data, copy_data, cax, ax, fig), frames=100, interval=30)
