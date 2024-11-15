import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askstring
import random

# Set up the main application window
root = tk.Tk()
root.title("Virtual Whiteboard")
root.geometry("900x700")
root.configure(bg="#1C1C1C")  # Black background

# Custom Colors and Fonts
toolbar_bg = "#2E2E2E"
canvas_bg = "#FFFFFF"
font = ("Helvetica", 10, "bold")
button_fg = "#1C1C1C"  # Foreground color for button text
button_colors = {
    "Ballpoint Pen": "#B5EAD7",
    "Fountain Pen": "#FFDAC1",
    "Air Brush": "#FF9AA2",
    "Paint Brush": "#B3B3E6",
    "Eraser": "#F7CAC9",
    "Text": "#FCEEB5"  # New color for Text option
}
slider_color = "#A0C4FF"

# Initialize default brush settings
current_color = "black"
brush_size = 10
brush_type = "Ballpoint Pen"
opacity = 1.0
last_x, last_y = None, None

# Functions to handle drawing
def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y
    if brush_type == "Text":
        add_text(event)  # If Text tool is selected, prompt for text input
    else:
        canvas.bind("<B1-Motion>", draw)

def draw(event):
    global last_x, last_y
    x, y = event.x, event.y
    color = blend_color_with_background(current_color, opacity)

    if brush_type == "Ballpoint Pen":
        canvas.create_line(last_x, last_y, x, y, fill=color, width=brush_size, capstyle=tk.ROUND, smooth=True, tags="brush")

    elif brush_type == "Fountain Pen":
        canvas.create_line(last_x, last_y, x, y, fill=color, width=max(1, brush_size - 8), capstyle=tk.BUTT, smooth=True, tags="brush")

    elif brush_type == "Air Brush":
        for _ in range(10):
            offset_x = random.randint(-brush_size, brush_size)
            offset_y = random.randint(-brush_size, brush_size)
            canvas.create_oval(x + offset_x, y + offset_y, x + offset_x + 1, y + offset_y + 1, fill=color, outline="", tags="brush")

    elif brush_type == "Paint Brush":
        canvas.create_line(last_x, last_y, x, y, fill=color, width=brush_size + 20, capstyle=tk.ROUND, smooth=True, tags="brush")

    elif brush_type == "Eraser":
        eraser_width = brush_size * 2
        canvas.create_line(last_x, last_y, x, y, fill=canvas_bg, width=eraser_width, capstyle=tk.ROUND, smooth=True, tags="brush")

    last_x, last_y = x, y

def blend_color_with_background(color, opacity):
    """Blends the brush color with the background color based on opacity."""
    r1, g1, b1 = root.winfo_rgb(color)
    r2, g2, b2 = root.winfo_rgb(canvas_bg)
    
    r = int((r1 * opacity + r2 * (1 - opacity)) / 256)
    g = int((g1 * opacity + g2 * (1 - opacity)) / 256)
    b = int((b1 * opacity + b2 * (1 - opacity)) / 256)
    
    return f"#{r:02x}{g:02x}{b:02x}"

def change_color():
    global current_color
    color = askcolor()[1]
    if color:
        current_color = color

def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

def change_opacity(new_opacity):
    global opacity
    opacity = float(new_opacity) / 100

def set_brush_type(new_type):
    global brush_type
    brush_type = new_type

def add_text(event):
    """Prompts the user to enter text and adds it to the canvas at the clicked position."""
    text = askstring("Text Input", "Enter the text:")
    if text:
        canvas.create_text(event.x, event.y, text=text, fill=current_color, font=("Helvetica", brush_size), tags="text")

def clear_canvas():
    """Clears everything from the canvas."""
    canvas.delete("all")

# Create a Canvas widget for the whiteboard with a border and rounded edges
canvas_frame = tk.Frame(root, bg=toolbar_bg, bd=5, relief="ridge")
canvas_frame.pack(pady=15)
canvas = tk.Canvas(canvas_frame, bg=canvas_bg, width=800, height=500, highlightthickness=0)
canvas.pack()

# Toolbar with color picker, brush size slider, brush type options, and clear button
toolbar = tk.Frame(root, bg=toolbar_bg, padx=10, pady=10)
toolbar.pack(fill="x")

# Clear button (top-left corner)
clear_button = tk.Button(toolbar, text="Clear All", command=clear_canvas, bg="#FFB6C1", fg=button_fg, font=font, padx=10, pady=5, relief="flat")
clear_button.pack(side="left", padx=10, pady=10)

# Color picker button
color_button = tk.Button(toolbar, text="Pick Color", command=change_color, bg="#D4A5A5", fg=button_fg, font=font, padx=5, pady=5, relief="flat")
color_button.pack(side="left", padx=5)

# Brush size slider with a more aesthetically pleasing design
size_slider = tk.Scale(toolbar, from_=1, to=100, orient="horizontal", label="Brush Size", command=change_brush_size,
                       bg=toolbar_bg, fg="white", font=font, troughcolor=slider_color, highlightthickness=0, relief="flat")
size_slider.set(brush_size)
size_slider.pack(side="left", padx=10)

# Opacity slider with matching aesthetic style
opacity_slider = tk.Scale(toolbar, from_=0, to=100, orient="horizontal", label="Opacity", command=change_opacity,
                          bg=toolbar_bg, fg="white", font=font, troughcolor=slider_color, highlightthickness=0, relief="flat")
opacity_slider.set(opacity * 100)
opacity_slider.pack(side="left", padx=10)

# Brush type buttons with individual pastel colors
for brush in button_colors:
    brush_button = tk.Button(toolbar, text=brush, command=lambda b=brush: set_brush_type(b), 
                             bg=button_colors[brush], fg=button_fg, font=font, padx=10, pady=5, relief="flat", width=12)
    brush_button.pack(side="left", padx=5, pady=5)

# Bind the drawing functions to mouse events
canvas.bind("<Button-1>", start_draw)

# Run the application
root.mainloop()
