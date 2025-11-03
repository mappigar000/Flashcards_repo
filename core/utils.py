def window_sizer(root, width_percent, height_percentage):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = int(screen_width * width_percent)
    window_height = int(screen_height * height_percentage)

    x_position = int((screen_width - window_width) / 2)
    y_position = int((screen_height - window_height) / 2)

    return f"{window_width}x{window_height}+{x_position}+{y_position}"

def make_grid_expandable(widget, rows=1, cols=1):
    for r in range(rows):
        widget.rowconfigure(r, weight=1)
    for c in range(cols):
        widget.columnconfigure(c, weight=1)