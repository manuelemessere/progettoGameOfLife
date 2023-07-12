import tkinter as tk
from tkinter import messagebox
import turtle
import random
import time


class GameOfLife:
    def __init__(self, l, t, sigma):
        self.l = l
        self.t = t
        self.sigma = sigma
        self.grid = self.create_grid()

    def create_grid(self):
        grid = []
        for _ in range(self.l):
            row = []
            for _ in range(self.l):
                if random.random() < self.sigma:
                    row.append(1)
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def update_generation(self):
        new_grid = []
        for row in range(self.l):
            new_row = []
            for col in range(self.l):
                count = self.count_neighbors(row, col)
                if self.grid[row][col] == 1:
                    if count < 2 or count > 3:
                        new_row.append(0)
                    else:
                        new_row.append(1)
                else:
                    if count == 3:
                        new_row.append(1)
                    else:
                        new_row.append(0)
            new_grid.append(new_row)
        self.grid = new_grid

    def count_neighbors(self, row, col):
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                neighbor_row = (row + i + self.l) % self.l
                neighbor_col = (col + j + self.l) % self.l
                count += self.grid[neighbor_row][neighbor_col]
        return count


class GameOfLifeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Game of Life')

        self.label_l = tk.Label(self.window, text='Lato (l):')
        self.label_l.pack()
        self.entry_l = tk.Entry(self.window)
        self.entry_l.pack()

        self.label_t = tk.Label(self.window, text='Numero di passi (t):')
        self.label_t.pack()
        self.entry_t = tk.Entry(self.window)
        self.entry_t.pack()

        self.label_sigma = tk.Label(
            self.window, text='Percentuale di riempimento (0<σ<1):')
        self.label_sigma.pack()
        self.entry_sigma = tk.Entry(self.window)
        self.entry_sigma.pack()

        self.button_start = tk.Button(
            self.window, text='Avvia Simulazione', command=self.start_simulation)
        self.button_start.pack()

        self.button_load = tk.Button(
            self.window, text='Carica Simulazione', command=self.load_simulation)
        self.button_load.pack()

        self.window.mainloop()

    def start_simulation(self):
        l = int(self.entry_l.get())
        t = int(self.entry_t.get())
        sigma = float(self.entry_sigma.get())
        self.game = GameOfLife(l, t, sigma)

        turtle_screen = turtle.Screen()
        turtle_screen.title('Game of Life')
        turtle_screen.setup(width=800, height=800)

        turtle_pen = turtle.Turtle()
        turtle_pen.speed(0)
        turtle_pen.hideturtle()

        cell_size = 800 / l

        for _ in range(t):
            self.draw_grid(turtle_pen, cell_size)
            self.game.update_generation()

        if messagebox.askyesno('Salvataggio', 'Salvare lo stato finale su file?'):
            self.save_simulation()

        turtle_screen.bye()

    def load_simulation(self):
        filename = tk.filedialog.askopenfilename(
            title='Carica Simulazione', filetypes=[('Text Files', '*.txt')])
        if filename:
            try:
                with open(filename, 'r') as file:
                    lines = file.readlines()
                    l = len(lines)
                    t = int(self.entry_t.get())
                    sigma = float(self.entry_sigma.get())
                    self.game = GameOfLife(l, t, sigma)
                    for row, line in enumerate(lines):
                        for col, value in enumerate(line.strip()):
                            self.game.grid[row][col] = int(value)

                    turtle_screen = turtle.Screen()
                    turtle_screen.title('Game of Life')
                    turtle_screen.setup(width=800, height=800)

                    turtle_pen = turtle.Turtle()
                    turtle_pen.speed(0)
                    turtle_pen.hideturtle()

                    cell_size = 800 / l

                    for _ in range(t):
                        self.draw_grid(turtle_pen, cell_size)
                        self.game.update_generation()

                    if messagebox.askyesno('Salvataggio', 'Salvare lo stato finale su file?'):
                        self.save_simulation()

                    turtle_screen.bye()

            except Exception as e:
                messagebox.showerror(
                    'Errore', 'Si è verificato un errore durante il caricamento del file.')

    def save_simulation(self):
        filename = tk.filedialog.asksaveasfilename(
            title='Salva Simulazione', defaultextension='.txt')
        if filename:
            try:
                with open(filename, 'w') as file:
                    for row in self.game.grid:
                        line = ''.join(map(str, row))
                        file.write(line + '\n')

                messagebox.showinfo(
                    'Salvataggio', 'Simulazione salvata correttamente.')

            except Exception as e:
                messagebox.showerror(
                    'Errore', 'Si è verificato un errore durante il salvataggio del file.')

    def draw_grid(self, pen, cell_size):
        pen.clear()
        pen.penup()  # Solleva la penna
        for row in range(len(self.game.grid)):
            for col in range(len(self.game.grid[row])):
                x = col * cell_size - 400
                y = 400 - row * cell_size
                pen.goto(x, y)  # Sposta la tartaruga alla nuova posizione
                if self.game.grid[row][col] == 1:
                    pen.pendown()  # Abbassa la penna
                    pen.fillcolor('black')
                    pen.begin_fill()
                    for _ in range(4):
                        pen.forward(cell_size)
                        pen.right(90)
                    pen.end_fill()
                pen.penup()  # Solleva nuovamente la penna dopo aver disegnato una cella
        time.sleep(1)  # Pausa di 1 secondo tra i passi della simulazione


gui = GameOfLifeGUI()
