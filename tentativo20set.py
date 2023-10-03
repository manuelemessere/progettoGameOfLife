import tkinter as tk
from tkinter import filedialog, messagebox
import turtle
import random
import time
import os
import numpy as np


class GameOfLife:
    def __init__(self, l, t, sigma, loadedGrid=None):
        self.l = l
        self.t = t
        self.sigma = sigma
        self.grid = (
            self.create_grid() if loadedGrid is None else loadedGrid
        )  # Controlla se la griglia è già stata caricata, altrimenti la recupera

    def create_grid(self):
        grid = []
        pdr = int(
            self.sigma * self.l * self.l
        )  # Prima era: self.sigma * self.l * self.l --> prd = Percentuale di riempimento
        for i in range(self.l):  # qua si itera per le righe
            row = []
            for j in range(self.l):  # qua per le colonne
                if random.random() < self.sigma and pdr != 0:
                    row.append(1)
                    pdr -= 1
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def update_generation(self):
        new_grid = [[0] * self.l for i in range(self.l)]  # Vedere cosa fa qua
        for row in range(self.l):
            for col in range(self.l):
                count = self.count_neighbors(row, col)
                if self.grid[row][col] == 1:
                    if count < 2 or count > 3:
                        new_grid[row][col] = 0
                    else:
                        new_grid[row][col] = 1
                else:
                    if count == 3:
                        new_grid[row][col] = 1
                    else:
                        new_grid[row][col] = 0
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
        self.window.title("Game of Life")

        self.l = None
        self.t = None
        self.sigma = None
        self.loadedSimulation = None

        self.setup_Gui()

        self.current_filename = None

        self.turtle_pen = None
        self.game = None

        self.window.mainloop()

    def setup_Gui(
        self,
    ):  # Ho aggiunto una nuova funzione che contenga i frame e label su suggerimento perché più ordinato
        # Frame per i pulsanti
        button_frame = tk.Frame(self.window, border=30)
        button_frame.pack(side="top")
        self.button_start = tk.Button(
            button_frame, text="Nuova Simulazione", command=self.new_simulation
        )
        self.button_start.pack()
        self.button_load = tk.Button(
            button_frame, text="Carica Simulazione", command=self.load_simulation
        )
        self.button_load.pack()

        # Frame per le entry e le label
        entry_frame = tk.Frame(self.window, border=30)
        entry_frame.pack()

        self.label_l = tk.Label(entry_frame, text="Lato (l):")
        self.label_l.pack()

        self.entry_l = tk.Entry(entry_frame)
        self.entry_l.config(state="disabled")
        self.entry_l.pack()

        self.label_t = tk.Label(entry_frame, text="Numero di passi (t):")
        self.label_t.pack()

        self.entry_t = tk.Entry(entry_frame)
        self.entry_t.config(state="disabled")
        self.entry_t.bind("<FocusIn>", self.entry_t_click)
        self.entry_t.pack()

        self.label_sigma = tk.Label(
            entry_frame, text="Percentuale di riempimento (0<σ<1):"
        )
        self.label_sigma.pack()

        self.entry_sigma = tk.Entry(entry_frame)
        self.entry_sigma.config(state="disabled")
        self.entry_sigma.pack()

        frame_avvio_sim = tk.Frame(self.window, border=30)
        frame_avvio_sim.pack(side="bottom")
        self.pulsante_avvio = tk.Button(
            frame_avvio_sim, text="Avvia simulazione", command=self.start_simulation
        )
        self.pulsante_avvio.pack()

    def entry_t_click(self, event):
        # Controlla se il testo nell'Entry è il suggerimento
        if self.entry_t.get() == "Inserisci il valore di t":
            self.entry_t.delete(0, tk.END)

    # Gestisce i parametri che vengono inseriti dall'utente
    def start_simulation(self):
        try:
            self.l = (
                int(self.entry_l.get()) if self.l is None else self.l
            )  # Invece di is prima c'era ==; in questo modo controlla se l fa parte di new_simulation o load
            self.t = int(self.entry_t.get())
            self.sigma = (
                float(self.entry_sigma.get()) if self.sigma is None else self.sigma
            )  # Invece di is prima c'era ==;
            self.game = GameOfLife(self.l, self.t, self.sigma, self.loadedSimulation)
            self.draw_turtle()
        except ValueError as e:
            messagebox.showerror("Errore", "Inserisci valori validi per l, t e sigma.")
            return

    def new_simulation(self):
        # Imposta i parametri a None
        self.l = None
        self.t = None
        self.sigma = None
        self.loadedSimulation = None
        self.current_filename = None

        # Cancella il testo nelle Entry
        self.entry_l.config(state="normal")
        self.entry_l.delete(0, tk.END)  # Cancella il testo nell'Entry l
        self.entry_t.config(state="normal")
        self.entry_t.delete(0, tk.END)  # Cancella il testo nell'Entry t
        self.entry_sigma.config(state="normal")
        self.entry_sigma.delete(0, tk.END)  # Cancella il testo nell'Entry sigma

    def draw_turtle(self):
        try:
            l = self.l
            t = self.t

            self.turtle_screen = turtle.Screen()
            self.turtle_screen.title("Game of Life")
            self.turtle_screen.setup(width=800, height=800, startx=400)

            turtle.TurtleScreen._RUNNING = True
            self.turtle_pen = turtle.Turtle()
            self.turtle_pen.speed(1)
            self.turtle_pen.hideturtle()

            cell_size = 800 / l

            for _ in range(t):
                self.draw_grid(self.turtle_pen, cell_size)
                self.game.update_generation()

            if (
                self.loadedSimulation is None and self.current_filename is None
            ):  # Verifica se è una nuova simulazione
                self.salvataggio = messagebox.showinfo(message="Simulazione terminata.")
                self.save_simulation()
            else:  # Verifica che la partita sia stata avviata da Carica simulazione
                sovrascrittura = messagebox.showinfo(message="Simulazione terminata.")
                if sovrascrittura:
                    self.save_simulation()

            self.turtle_screen.bye()

        except IndexError as e:
            messagebox.showerror(
                "Errore",
                "Indice fuori dai limiti durante la visualizzazione della griglia: {}".format(
                    str(e)
                ),
            )

        except tk.TclError as e:
            messagebox.showinfo("Errore", "La simulazione è stata interrotta.")

        except ZeroDivisionError as e:
            messagebox.showinfo(
                "Errore", "Il valore inserito in l deve essere maggiore di 0."
            )

        except Exception as e:
            messagebox.showerror(
                "Errore",
                "Errore durante la visualizzazione della griglia: {}".format(str(e)),
            )

    def load_simulation(self):
        self.entry_t.config(state="normal")
        self.entry_sigma.config(state="normal")
        self.entry_l.config(state="normal")

        filename = tk.filedialog.askopenfilename(
            title="Carica Simulazione", filetypes=[("Text Files", "*.txt")]
        )

        # Sono stati aggiunti questi due if per evitare che scattasserro eccezioni
        if not filename:
            # L'utente ha annullato la selezione dei file
            return

        if not os.path.exists(filename):
            # Il file non esiste
            messagebox.showerror("Errore", "File non trovato.")

        try:
            file = np.loadtxt(filename, dtype=int)
            loaded_simulation = file

            aliveLen = len(file[file == 1])
            total_cells = len(np.asarray(file).ravel())
            sigma = aliveLen / total_cells
            l = len(file)

            # Reimposta i valori delle Entry solo se il file è stato caricato correttamente, aggiunto per far in modo che i valori non rimanessero salvati dalle vecchie simulazioni
            self.entry_l.delete(0, tk.END)
            self.entry_l.insert(tk.END, str(l))

            self.entry_t.delete(0, tk.END)

            self.entry_sigma.delete(0, tk.END)
            self.entry_sigma.insert(tk.END, str(sigma))

            if self.t is None:
                self.entry_t.insert(tk.END, "Inserisci il valore di t")

            # Assegna il nuovo file e i nuovi valori alle variabili di classe
            self.loadedSimulation = loaded_simulation
            self.current_filename = filename
            self.l = l
            self.sigma = sigma

        except (PermissionError, IOError):
            # Errore durante accesso o I/O durante la lettura del file
            messagebox.showerror(
                "Errore", "Errore durante accesso o di I/O durante la lettura del file"
            )
            return
        except Exception as e:
            # Gestione di altre eccezioni
            messagebox.showerror(
                "Errore", "Si è verificato un errore durante il caricamento del file."
            )
            return
        # Se tutto va bene, puoi mostrare un messaggio di successo
        messagebox.showinfo(
            "Caricamento completato", "Il file è stato caricato con successo"
        )

    # la funzione save_simulation crea dei problemi perché il current name si attiva nel momento in
    # cui si sbaglia e si assegna lo stesso nome a un'altra simulazione
    # controllare che il testo no funzioni adeguatamente

    """Errori riportati:
    1) [Errno 2] No such file or directory: OK
    2) local variable 'filename' referenced before assignment --> UnboundLocalError OK
    3) [Errno 17] File exists: '/Users/clarissarizzello/Progetti_python/game_of_life/data/a.txt' --> correlato al punto sotto
    4) se nella parte in cui si chiede se si vogliono salvare i progressi con un nuovo nome, se si inserisce il nome di un file già esistente dà l'errore mostrato sopra[Errno17] 
    5) fare la stessa cosa che ho fatto per quando si avvia una nuova simulazione anche per la simulazione caricata in modo che se si preme no esso chiude la finestra con il messaggio salvataggio annullato
    6) Vedere se va bene il fatto che apra due volte volte la finestra per new_overwritename --> la prima quando si dice il nome per la prima volta e segnala
        che è già stato utilizzato e la seconda quando si preme ok per procedere e apre nuovamente la finestra dove scrivere il nome del file
    """

    def save_simulation(self):
        if (
            self.loadedSimulation is not None and self.current_filename is not None
        ):  # controlla che la simulazione sia fatta partire da Carica Simulazione
            try:
                sovrascrivere = messagebox.askyesnocancel(
                    message="Vuoi sovrascrivere la simulazione caricata precedentemente?"
                )
                if sovrascrivere:
                    with open(self.current_filename, "w") as loaded_file:
                        for row in self.game.grid:
                            line = " ".join(map(str, row))
                            loaded_file.write(line + "\n")
                    messagebox.showinfo(
                        message="I progressi sono stati sovrascritti con successo."
                    )
                elif (
                    sovrascrivere is None
                ):  # se l'utente preme cancel il salvataggio viene annullato
                    messagebox.showinfo(message="Salvataggio annullato.")
                    return
                else:  # se l'utente preme no, si apre una nuova finestra che chiede se si vogliono salvare i progressi in una nuova simulazione
                    save_as_new = messagebox.askyesno(
                        message="Vuoi salvare i nuovi progressi in una nuova simulazione?"
                    )  # modificare questo messaggio orribile
                    if save_as_new:
                        overwrite_filename = tk.filedialog.asksaveasfilename(
                            title="Salva Simulazione", defaultextension=".txt"
                        )
                        with open(overwrite_filename, "x") as overwriteFile:
                            for row in self.game.grid:
                                line = " ".join(map(str, row))
                                overwriteFile.write(line + "\n")
                        messagebox.showinfo(
                            message="I progressi sono stati salvati con un nuovo nome."
                        )

                    else:
                        messagebox.showinfo(message="Salvataggio annullato.")
                        return

            except FileExistsError as e:
                if os.path.exists(new_filename):
                    while True:
                        okCancel = messagebox.askokcancel(
                            message="Il nome selezionato è già stato utilizzato. Vuoi procedere?"
                        )
                        if okCancel:
                            new_overwritename = tk.filedialog.asksaveasfilename(
                                title="Salva Simulazione", defaultextension=".txt"
                            )
                            with open(new_overwritename, "w") as overWriteFile:
                                for i in self.game.grid:
                                    line = " ".join(map(str, i))
                                    overWriteFile.write(line + "\n")
                            messagebox.showinfo(
                                message="La simulazione è stata salvata con un nuovo nome."
                            )
                            break
                        else:
                            messagebox.showinfo(message="Salvataggio annullato.")

            except FileNotFoundError as e:
                messagebox.showerror(message="Salvataggio annullato.")
                return

        else:

            try:
                salvataggio = messagebox.askyesno(
                    message="Vuoi salvare la simulazione?"
                )
                if not salvataggio:
                    messagebox.showinfo(message="Salvataggio annullato.")
                    return

                if salvataggio:
                    filename = tk.filedialog.asksaveasfilename(
                        title="Salva Simulazione", defaultextension=".txt"
                    )  # permette di salvare la nuova partita con estensione txt

                    if not filename:
                        messagebox.showinfo(message="Salvataggio annullato.")
                        return

                    if os.path.exists(filename) and self.loadedSimulation is None:
                        while True:
                            sostituzione = messagebox.askyesno(
                                message="Il nome è già in uso. Vuoi sovrascrivere la simulazione?"
                            )
                            if sostituzione:

                                with open(filename, "w") as newFile:
                                    for row in self.game.grid:
                                        line = " ".join(map(str, row))
                                        newFile.write(line + "\n")
                                messagebox.showinfo(
                                    message="La simulazione è stata sovrascritta con successo."
                                )
                                break

                            else:
                                new_filename = tk.filedialog.asksaveasfilename(
                                    title="Salva Simulazione", defaultextension=".txt"
                                )
                                if not new_filename:
                                    messagebox.showinfo(
                                        message="Sovrascrittura annullata."
                                    )
                                    return
                                filename = new_filename

                    else:
                        with open(filename, "x") as file:
                            for row in self.game.grid:
                                line = " ".join(map(str, row))
                                file.write(line + "\n")
                        messagebox.showinfo(
                            message="La nuova simulazione è stata salvata con successo."
                        )

            except FileNotFoundError as e:
                messagebox.showerror(
                    "Errore", "Il file non è stato trovato."
                )  # chiedere a chatgpt un messaggio più idoneo

            except IOError as e:
                messagebox.showerror(
                    "Errore",
                    "Errore di I/O durante il salvataggio del file: {}".format(str(e)),
                )

            except Exception as e:
                messagebox.showerror(
                    "Errore",
                    "Si è verificato un errore durante il salvataggio del file: {}".format(
                        str(e)
                    ),
                )

    def draw_grid(self, pen, cell_size):
        pen.reset()
        turtle_screen = pen.getscreen()
        turtle_screen.tracer(0)

        pen.hideturtle()

        pen.penup()
        x_start = -400
        y_start = 400

        for col in range(self.l + 1):
            x = x_start + col * cell_size
            y1 = y_start
            y2 = y_start - self.l * cell_size
            pen.goto(x, y1)
            pen.pendown()
            pen.goto(x, y2)
            pen.penup()

        for row in range(self.l + 1):
            y = y_start - row * cell_size
            x1 = x_start
            x2 = x_start + self.l * cell_size
            pen.goto(x1, y)
            pen.pendown()
            pen.goto(x2, y)
            pen.penup()

        for row in range(self.l):
            for col in range(self.l):
                x = x_start + col * cell_size + 1
                y = y_start - row * cell_size - 1

                pen.penup()
                pen.goto(x, y)

                if self.game.grid[row][col] == 1:
                    pen.pendown()
                    pen.fillcolor("black")
                    pen.begin_fill()
                    for _ in range(4):
                        pen.forward(cell_size - 2)
                        pen.right(90)
                    pen.end_fill()

        turtle_screen.update()
        time.sleep(1)


gui = GameOfLifeGUI()
