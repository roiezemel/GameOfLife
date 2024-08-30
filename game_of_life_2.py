from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from collections import deque
from configuration import configure, save_dialog
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


GRID_SIZE = 30
creatures: dict[tuple[int, int], Rectangle] = {}
to_add: deque[tuple[int, int]] = deque()
to_remove: deque[tuple[int, int]] = deque()
min_x, max_x, min_y, max_y = [- GRID_SIZE / 2 - 0.5, GRID_SIZE / 2 + 0.5, - GRID_SIZE / 2 - 0.5, GRID_SIZE / 2 + 0.5]


def init():
    # Set initial axis limits to zoom in
    reset_zoom()
    fig.patch.set_facecolor('black')  # Figure background color
    ax.set_facecolor('black')  # Axes background color
    ax.axis('off')
    ax.set_aspect('equal')
    # Hide major ticks and labels
    ax.set_xticks([])  # Disable major x-ticks
    ax.set_yticks([])  # Disable major y-ticks
    fig.tight_layout()

    grid_size = data.shape[0]
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i, j]:
                add_creature(j - int(grid_size / 2), int(grid_size / 2) - i)


def reset_zoom():
    width = max(max_x - min_x, max_y - min_y)
    padding = width / 20
    ax.set_xlim(min_x - padding, max_x + padding)
    ax.set_ylim(min_y - padding, max_y + padding)
    text.set(f"Zoom: {int(width / GRID_SIZE * 100)}%")


def update(_):
    global min_x, min_y, max_x, max_y
    handled = set()
    for (x, y) in creatures.keys():
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x

        if y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i, j) not in handled:
                    handled.add((i, j))
                    update_single(i, j)

    while len(to_remove):
        i, j = to_remove.pop()
        creatures[(i, j)].remove()
        creatures.pop((i, j))

    while len(to_add):
        i, j = to_add.pop()
        add_creature(i, j)

    reset_zoom()


def update_single(i, j):
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


def add_creature(i, j):
    creatures[(i, j)] = Rectangle((i + 0.1, j + 0.1), 1 - 0.2, 1 - 0.2, facecolor='white', fill=True)
    ax.add_patch(creatures[(i, j)])

def main():
    global fig, canvas, text, ax, data

    data = configure()
    root = tk.Tk()
    root.configure(bg='black')
    root.state('zoomed')
    root.title('The Game of Life')
    fig = Figure()
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    bottom_frame = tk.Frame(root, bg='black')
    bottom_frame.pack(fill=tk.BOTH, pady=(0, 30), padx=30)

    text = tk.StringVar(value='Zoom: 100%')

    def restart():  # TODO: There is a problem with restarting, some bug...
        global data, fig, ax, canvas, text
        root.destroy()
        reset()
        main()

    tk.Button(bottom_frame, text='Save pattern', command=lambda: save_dialog(data),
                            font=('Ariel', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
    tk.Button(bottom_frame, text='Restart', font=('Ariel', 10, 'bold'),
              bg='green', command=restart).pack(side=tk.LEFT)
    tk.Label(bottom_frame, textvariable=text, bg='black', fg='white',
             font=('Ariel', 15)).pack(side=tk.RIGHT)

    ax = fig.subplots()
    init()

    ani = FuncAnimation(fig, update, frames=100, interval=30)
    root.mainloop()

def reset():
    global data, fig, ax, canvas, text, creatures, to_add, to_remove, min_x, max_x, min_y, max_y
    data, fig, ax, canvas, text = [None] * 5
    creatures = {}
    to_add = deque()
    to_remove = deque()
    min_x, max_x, min_y, max_y = [- GRID_SIZE / 2 - 0.5, GRID_SIZE / 2 + 0.5, - GRID_SIZE / 2 - 0.5,
                                  GRID_SIZE / 2 + 0.5]


data, fig, ax, canvas, text = [None] * 5
main()
