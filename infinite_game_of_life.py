from matplotlib.patches import Rectangle
from collections import deque
from matplotlib.animation import FuncAnimation


def infinite_space_animation(data, ax, fig, grid_size, text):

    creatures: dict[tuple[int, int], Rectangle] = {}
    to_add: deque[tuple[int, int]] = deque()
    to_remove: deque[tuple[int, int]] = deque()

    # min_x, max_x, min_y, max_y:
    bounds = [- grid_size / 2 - 0.5, grid_size / 2 + 0.5, - grid_size / 2 - 0.5, grid_size / 2 + 0.5]

    # Set initial axis limits to zoom in
    reset_zoom(ax, text, grid_size, bounds)

    grid_size = data.shape[0]
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i, j]:
                add_creature(j - int(grid_size / 2), int(grid_size / 2) - i, ax, creatures)

    def update(_):
        update_game(ax, creatures, to_remove, to_add, bounds)
        reset_zoom(ax, text, grid_size, bounds)

    return FuncAnimation(fig, update, frames=100, interval=30)


def reset_zoom(ax, text, grid_size, bounds):
    width = max(bounds[1] - bounds[0], bounds[3] - bounds[2])
    padding = width / 20
    ax.set_xlim(bounds[0] - padding, bounds[1] + padding)
    ax.set_ylim(bounds[2] - padding, bounds[3] + padding)
    text.set(f"Zoom: {int(width / grid_size * 100)}%")


def update_game(ax, creatures, to_remove, to_add, bounds):
    # min_x, max_x, min_y, max_y = bounds
    handled = set()
    for (x, y) in creatures.keys():
        if x < bounds[0]:
            bounds[0] = x
        elif x > bounds[1]:
            bounds[1] = x

        if y < bounds[2]:
            bounds[2] = y
        elif y > bounds[3]:
            bounds[3] = y

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i, j) not in handled:
                    handled.add((i, j))
                    update_single(i, j, creatures, to_remove, to_add)

    while len(to_remove):
        i, j = to_remove.pop()
        creatures[(i, j)].remove()
        creatures.pop((i, j))

    while len(to_add):
        i, j = to_add.pop()
        add_creature(i, j, ax, creatures)


def update_single(i, j, creatures, to_remove, to_add):
    living_neighbors = 0
    for k in range(i - 1, i + 2):
        for m in range(j - 1, j + 2):
            if (k, m) != (i, j) and (k, m) in creatures:
                living_neighbors += 1

    if (i, j) in creatures:
        if living_neighbors < 2 or living_neighbors > 3:
            to_remove.append((i, j))
    elif living_neighbors == 3:
        to_add.append((i, j))


def add_creature(i, j, ax, creatures):
    creatures[(i, j)] = Rectangle((i + 0.1, j + 0.1), 1 - 0.2, 1 - 0.2, facecolor='white', fill=True)
    ax.add_patch(creatures[(i, j)])
