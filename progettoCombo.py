'''
Codice implementato mettendo un mix degli altri tre codici.
Cose da aggiungere:
1)Inserimento dei tre valori inseriti dall'utente se si inzia il gioco
2)Possibilità di caricare il gioco da file o iniziare una nuova partita
3)Possibilità di salvare il gioco su un file
4)Aggiustare l'interfaccia grafica
'''
import turtle
import tkinter as tk
import random
import copy

class GameOfLife:
    def __init__(self, rows, cols):
        """
        Inizializza un'istanza del Gioco della Vita con le dimensioni specificate.
        Crea una griglia casuale di dimensioni rows x cols, dove ogni cella può essere 0 (morta) o 1 (viva).

        Args:
            rows (int): Numero di righe della griglia.
            cols (int): Numero di colonne della griglia.
        """
        self.rows = rows
        self.cols = cols
        self.grid = self.create_grid()

    def create_grid(self):
        """
        Crea una griglia casuale di dimensioni rows x cols.

        Returns:
            list: Una lista di liste rappresentante la griglia.
        """
        grid = []
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                row.append(random.choice([0, 1]))
            grid.append(row)
        return grid

    def toggle_cell(self, row, col):
        """
        Inverte lo stato di una cella nella posizione specificata.

        Args:
            row (int): Indice della riga della cella.
            col (int): Indice della colonna della cella.
        """
        self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0

    def is_cell_alive(self, row, col):
        """
        Verifica se una cella è viva.

        Args:
            row (int): Indice della riga della cella.
            col (int): Indice della colonna della cella.

        Returns:
            bool: True se la cella è viva, False altrimenti.
        """
        return self.grid[row][col] == 1

    def count_neighbors(self, row, col):
        """
        Conta il numero di vicini vivi di una cella.

        Args:
            row (int): Indice della riga della cella.
            col (int): Indice della colonna della cella.

        Returns:
            int: Numero di vicini vivi.
        """
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                neighbor_row = (row + i + self.rows) % self.rows
                neighbor_col = (col + j + self.cols) % self.cols
                count += self.grid[neighbor_row][neighbor_col]
        return count

    def update_generation(self):
        """
        Aggiorna la griglia alla generazione successiva applicando le regole del Gioco della Vita.
        """
        new_grid = []
        for row in range(self.rows):
            new_row = []
            for col in range(self.cols):
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

class GameOfLifeGUI:
    def __init__(self, game, rows, cols, cell_size, speed):
        """
        Inizializza l'interfaccia grafica del Gioco della Vita utilizzando Tkinter.

        Args:
            game (GameOfLife): Istanza del Gioco della Vita.
            rows (int): Numero di righe della griglia.
            cols (int): Numero di colonne della griglia.
            cell_size (int): Dimensione delle celle in pixel.
            speed (int): Velocità di aggiornamento in millisecondi.
        """
        self.game = game
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.speed = speed

        self.window = tk.Tk()
        self.window.title('Game of Life')

        self.canvas = tk.Canvas(self.window, width=cols * cell_size, height=rows * cell_size)
        self.canvas.pack()

        self.draw_grid()

        self.update()

        self.window.mainloop()

    def draw_grid(self):
        """
        Disegna la griglia sulla canvas.
        """
        self.canvas.delete('all')
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if self.game.is_cell_alive(row, col):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')

    def update(self):
        """
        Aggiorna la griglia e ridisegna la canvas alla generazione successiva.
        """
        self.game.update_generation()
        self.draw_grid()
        self.window.after(1000 // self.speed, self.update)

class GameOfLifeApp:
    def __init__(self, rows, cols, cell_size, speed):
        """
        Inizializza l'applicazione del Gioco della Vita.

        Args:
            rows (int): Numero di righe della griglia.
            cols (int): Numero di colonne della griglia.
            cell_size (int): Dimensione delle celle in pixel.
            speed (int): Velocità di aggiornamento in millisecondi.
        """
        self.game = GameOfLife(rows, cols)
        self.gui = GameOfLifeGUI(self.game, rows, cols, cell_size, speed)

rows = 20
cols = 20
cell_size = 20
speed = 1
app = GameOfLifeApp(rows, cols, cell_size, speed)
