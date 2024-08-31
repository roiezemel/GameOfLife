from configuration import configure, save_dialog
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from game_of_life import finite_space_animation
from infinite_game_of_life import infinite_space_animation

GRID_SIZE = 50
MODE = 'finite'


def main():
    data = configure(GRID_SIZE)

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

    def restart():
        root.destroy()
        main()

    tk.Button(bottom_frame, text='Save pattern', command=lambda: save_dialog(data),
              font=('Ariel', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
    tk.Button(bottom_frame, text='Reset', font=('Ariel', 10, 'bold'),
              bg='green', command=restart).pack(side=tk.LEFT)
    tk.Label(bottom_frame, textvariable=text, bg='black', fg='white',
             font=('Ariel', 15)).pack(side=tk.RIGHT)

    ax = fig.subplots()
    fig.patch.set_facecolor('black')  # Figure background color
    ax.set_facecolor('black')  # Axes background color
    ax.axis('off')
    ax.set_aspect('equal')
    # Hide major ticks and labels
    ax.set_xticks([])  # Disable major x-ticks
    ax.set_yticks([])  # Disable major y-ticks
    fig.tight_layout()

    if MODE == 'finite':
        ani = finite_space_animation(data, ax, fig, GRID_SIZE)
    else:
        ani = infinite_space_animation(data, ax, fig, GRID_SIZE, text)

    root.mainloop()


main()
