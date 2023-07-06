'''codice implementato nuovamente mettendo la logica nella classe Script, l'interfaccia grafica nella classe GUI.
Trovare una soluzione, nel file finale, di usare la classe Script con il modulo turtle con cui
creare la griglia e i movimenti del gioco
'''
import tkinter as tk
import random
'''ciao'''

class Script:
    def __init__(self, rows, cols, cell_size=10, speed=1):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.speed = speed
        self.grid = self.create_grid()
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg='white')
        self.canvas.pack()
        self.window.resizable(False, False)
        self.window.title('Game of Life')

        self.draw_grid()
        self.create_buttons()
        self.window.mainloop()

    def create_grid(self):
        grid = []
        for row in range(self.rows):
            grid.append([])
            for col in range(self.cols):
                grid[row].append(random.randint(0, 1))
        return grid

    def draw_grid(self):
        self.canvas.delete('all')
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if self.grid[row][col] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='orange', outline='black')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')

    def update(self):
        new_grid = []
        for row in range(self.rows):
            new_grid.append([])
            for col in range(self.cols):
                new_grid[row].append(self.get_new_cell_state(row, col))
        self.grid = new_grid
        self.draw_grid()
        self.window.after(500//self.speed, self.update)

    def get_new_cell_state(self, row, col):
        num_neighbours = self.get_num_neighbours(row, col)
        if self.grid[row][col] == 1:
            if num_neighbours < 2 or num_neighbours > 3:
                return 0
            elif num_neighbours == 2 or num_neighbours == 3:
                return 1
        else:
            if num_neighbours == 3:
                return 1
            else:
                return 0

    def get_num_neighbours(self, row, col):
        num_neighbours = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbour_row = row + i
                neighbour_col = col + j
                if neighbour_row < 0 or neighbour_row >= self.rows or neighbour_col < 0 or neighbour_col >= self.cols:
                    continue
                num_neighbours += self.grid[neighbour_row][neighbour_col]
        return num_neighbours

    def run(self):
        self.update()

    def reset(self):
        self.grid = self.create_grid()
        self.draw_grid()

    def create_buttons(self):
        self.start_button = tk.Button(self.window, text='Start', command=self.run)
        self.start_button.pack(side='left')
        self.stop_button = tk.Button(self.window, text='Stop', command=self.window.destroy)
        self.stop_button.pack(side='left')
        self.reset_button = tk.Button(self.window, text='Reset', command=self.reset)
        self.reset_button.pack(side='left')
        
    def change_speed(self, speed):
        self.speed = int(speed)

class GUI:
    def __init__(self, rows, cols, cell_size=10, speed=1):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=cols*cell_size, height=rows*cell_size, bg='white')
        self.canvas.pack()
        self.window.resizable(False, False)
        self.window.title('Game of Life')

        self.game = Script(rows, cols, cell_size, speed)
        self.draw_grid()
        self.create_buttons()
        self.create_label()
        self.window.mainloop()

    def draw_grid(self):
        self.game.draw_grid()

    def create_buttons(self):
        self.start_button = tk.Button(self.window, text='Start', command=self.game.run)
        self.start_button.pack(side='left')
        self.stop_button = tk.Button(self.window, text='Stop', command=self.window.destroy)
        self.stop_button.pack(side='left')
        self.reset_button = tk.Button(self.window, text='Reset', command=self.game.reset)
        self.reset_button.pack(side='left')
        self.speed_slider = tk.Scale(self.window, from_=1, to=10, orient='horizontal', label='Speed', command=self.game.change_speed)
        self.speed_slider.pack(side='left')

    def create_label(self):
        self.generation_label = tk.Label(self.window, text='Generation: 0')
        self.generation_label.pack(side='bottom')

    def update_generation(self):
        self.generation_label.config(text='Generation: {}'.format(self.game.generation))
        
rows = 20
cols = 20
cell_size = 20
speed = 1

gui = GUI(rows, cols, cell_size, speed)
