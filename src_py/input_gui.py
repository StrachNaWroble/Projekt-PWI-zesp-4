import tkinter as tk

COLORS = {
    'white':  '#FFFFFF',
    'yellow': '#FFFF00',
    'green':  '#00FF00',
    'blue':   '#0000FF',
    'red':    '#FF0000',
    'orange': '#FFA500',
    'grey':   '#D3D3D3'
}


class InputGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Siatka kostki")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.current_color = 'white'
        self.create_palette()
        self.grid_frame = tk.Frame(self.root, bg="#eeeeee", padx=25, pady=25)
        self.grid_frame.grid(row=1, column=0, sticky="nsew")
        self.create_grid()
        
    def create_palette(self):
        palette_frame = tk.Frame(self.root, pady=10, bg="#dddddd")
        palette_frame.grid(row=0, column=0, sticky="ew")
        tk.Label(palette_frame, text="Wybierz kolor: ", bg="#dddddd", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        
        for color_name, color_hex in COLORS.items():
            if color_name == 'grey': continue
            button = tk.Button(palette_frame, bg=color_hex, width=4, height=2,
                            command=lambda c=color_name: self.set_brush(c))
            button.pack(side=tk.LEFT, padx=5)
            
    def set_brush(self, color):
        self.current_color = color
        print(f"Wybrano kolor: {color}")

    def create_grid(self):
        for col in range(12):
            self.grid_frame.columnconfigure(col, weight=1)
        for row in range(9):
            self.grid_frame.rowconfigure(row, weight=1)
        faces_layout = {
            'U': (3, 0),
            'L': (0, 3),
            'F': (3, 3),
            'R': (6, 3),
            'B': (9, 3),
            'D': (3, 6)
        }
        for face_name, (offset_x, offset_y) in faces_layout.items():
            self.create_face(face_name, offset_x, offset_y)

    def create_face(self, face_name, offset_x, offset_y):
        for r in range(3):
            for c in range(3):
                text_on_button = ""
                if r == 1 and c == 1:
                    text_on_button = face_name
                button = tk.Button(self.grid_frame, 
                                bg=COLORS['grey'],
                                text=text_on_button,
                                borderwidth=1,
                                relief="solid",
                                font=("Arial", 15, "bold"))
                button.config(command=lambda b=button: self.paint_tile(b))
                button.grid(row=offset_y + r, column=offset_x + c, sticky="nsew", padx=1, pady=1)
                
    def paint_tile(self, button_widget):
        color_hex = COLORS[self.current_color]
        button_widget.configure(bg=color_hex)


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(600, 500) 
    cube_editor = InputGUI(root)
    root.mainloop()
