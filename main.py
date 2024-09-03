from configuration import configure, save_dialog
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from default_game_of_life import finite_space_animation
from infinite_game_of_life import infinite_space_animation

GRID_SIZE = 50
INFINITE_MODE = 'infinite'
NORMAL_MODE = 'normal'


def main():
    data, mode = configure(GRID_SIZE)

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
    tk.Button(bottom_frame, text='Reconfigure', font=('Ariel', 10, 'bold'),
              bg='green', command=restart).pack(side=tk.LEFT, padx=(0, 10))

    def change_speed(s):
        interval = round(1000 / int(s))
        if s == '100':
            interval = 0
        ani.event_source.interval = interval
        ani._interval = interval

    speed = tk.Scale(bottom_frame, orient=tk.HORIZONTAL, from_=1, to=100, command=change_speed,
                     bg='black', activebackground='green', borderwidth=1,
                     highlightthickness=0, showvalue=False,
                     sliderrelief=tk.FLAT)
    speed.pack(side=tk.LEFT)
    speed.set(int(1000 / 30))

    if mode == INFINITE_MODE:
        tk.Label(bottom_frame, textvariable=text, bg='black', fg='white',
                 font=('Ariel', 15)).pack(side=tk.RIGHT)

    ax = fig.subplots()
    fig.patch.set_facecolor('black')  # Figure background color
    ax.set_facecolor('black')  # Axes background color
    if mode == NORMAL_MODE:
        ax.spines[:].set_color('white')

    ax.set_aspect('equal')
    # Hide major ticks and labels
    ax.set_xticks([])  # Disable major x-ticks
    ax.set_yticks([])  # Disable major y-ticks
    fig.tight_layout()

    if mode == NORMAL_MODE:
        ani = finite_space_animation(data, ax, fig, GRID_SIZE)
    else:
        ani = infinite_space_animation(data, ax, fig, GRID_SIZE, text)

    root.mainloop()


main()
