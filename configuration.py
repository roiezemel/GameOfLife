import numpy as np
from tkinter import *
from matplotlib.figure import Figure
from save_patterns import load_pattern, save_pattern
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename

GRID_SIZE = 50
ZOOM = 21  # ZOOM X ZOOM grid
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def configure(data=None):

    if data is None:
        data = np.zeros((GRID_SIZE, GRID_SIZE))

    root = Tk()
    root.title('The Game of Life - Setup')
    root.state('zoomed')

    fig = Figure(facecolor='black', edgecolor='black')
    ax = fig.subplots()
    fig.patch.set_facecolor('black')  # Figure background color
    canvas = FigureCanvasTkAgg(fig, root)

    toolbar = NavigationToolbar2Tk(canvas, root)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def open_pattern():
        nonlocal data
        file_path = askopenfilename(initialdir=CURRENT_DIR + '/patterns')
        pattern = load_pattern(file_path)
        data = np.minimum(data + pattern, 1)
        cax.set_data(data)
        fig.canvas.draw()

    open_pattern_button = Button(toolbar, text='Open pattern', command=open_pattern)
    open_pattern_button.pack(side=LEFT, padx=10)

    done = Button(toolbar, text='Done!', font=('Ariel', 10, 'bold'), bg='green', fg='white', command=root.destroy)
    done.pack(side=LEFT, padx=10)

    ax.set_facecolor('black')  # Axes background color
    cax = ax.imshow(data, cmap='gray', interpolation='nearest', vmin=0, vmax=1)

    # Set aspect ratio to equal to ensure cells are square.txt
    ax.set_aspect('equal')

    # Define grid lines
    ax.set_xticks(np.arange(-0.5, GRID_SIZE, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, GRID_SIZE, 1), minor=True)

    # Hide major ticks and labels
    ax.set_xticks([])  # Disable major x-ticks
    ax.set_yticks([])  # Disable major y-ticks

    # Hide the major ticks
    ax.tick_params(which='both', size=0)  # Hide both major and minor ticks

    # Draw grid lines
    ax.grid(which='minor', color=[0.05] * 3, linestyle='-', linewidth=1.5)

    # Adjust layout to fit the plot into the window
    fig.tight_layout()

    # Zoom settings
    zoom_x_min, zoom_x_max = GRID_SIZE / 2 - ZOOM / 2, GRID_SIZE / 2 + ZOOM / 2  # Define x limits for zoom
    zoom_y_min, zoom_y_max = GRID_SIZE / 2 - ZOOM / 2, GRID_SIZE / 2 + ZOOM / 2  # Define y limits for zoom

    # Set initial axis limits to zoom in
    ax.set_xlim(zoom_x_min - 0.5, zoom_x_max - 0.5)
    ax.set_ylim(zoom_y_max - 0.5, zoom_y_min - 0.5)  # Note: Y-axis is inverted

    pressed = False

    def on_click(event, only_on=False):
        if event.inaxes == ax:
            x, y = int(event.xdata + 0.5), int(event.ydata + 0.5)
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                data[y, x] = 1 if only_on else 1 - data[y, x]  # Toggle cell
                cax.set_data(data)
                fig.canvas.draw()

    def on_press(event):
        nonlocal pressed
        if toolbar.mode == '':
            on_click(event)
            pressed = True

    def on_motion(event):
        if pressed:
            on_click(event, True)

    def on_release(event):
        nonlocal pressed
        if toolbar.mode == '':
            pressed = False

    # Connect the click event to the handler
    fig.canvas.mpl_connect('button_press_event', on_press),
    fig.canvas.mpl_connect('motion_notify_event', on_motion),
    fig.canvas.mpl_connect('button_release_event', on_release)

    root.mainloop()
    return data


def save_dialog(data):
    path = asksaveasfilename(defaultextension=".txt",
                             initialdir=CURRENT_DIR + '/patterns',
                             initialfile='pattern1.txt')
    if path:
        save_pattern(data, path)
