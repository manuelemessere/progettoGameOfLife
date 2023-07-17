'''
Cose da correggere:
1) chiusura improvvisa del gioco dopo tot secondi, chiedendo di salvare il file
2) errore caricamento da file, dice che c'è stato un problema 
3) convalidazione dei dati
4) controllo e sistemazione delle eccezioni per ogni pulsante o momento di comunicaizione con l'utente
5) Aggiungi commenti per spiegare il funzionamento delle diverse parti del codice.
6) Aggiungi controlli per verificare se i valori inseriti dall'utente sono validi (ad esempio, se sono numeri positivi o se il valore di sigma è compreso tra 0 e 1).
7) Evita l'utilizzo di nomi di variabili singole come l, t, sigma poiché possono essere poco descrittivi. È preferibile utilizzare nomi più esplicativi come lato, numero_passi, percentuale_riempimento.
8) Potresti considerare l'aggiunta di una funzione reset_simulation per ripristinare il gioco allo stato iniziale.

riscontro con GUI:
2) Caricamento da file non funziona
3) Se non inserisci i valori non parte, aggiungere eccezione
4) Si chiude autamaticamente quando ti chiede di salvare

'''

import tkinter as tk
from tkinter import filedialog, messagebox
import turtle
import random
import time
import os #per salvare partite

class GameOfLife:
    
    ''' 
     è il costruttore della classe. 
     Viene chiamato quando crei un nuovo oggetto GameOfLife e inizializza le variabili di istanza l, t e sigma 
     con i valori passati come argomenti al costruttore. Questi valori rappresentano rispettivamente 
     la dimensione del lato della griglia, il numero di generazioni da eseguire e la probabilità di avere una cella iniziale attiva. 
     Viene anche chiamato il metodo create_grid() per creare la griglia iniziale.
    '''
    def __init__(self, l, t, sigma):    # Questa riga definisce il metodo speciale __init__, che è il costruttore della classe. Viene chiamato quando crei un nuovo oggetto GameOfLife e accetta tre parametri: l, t, sigma.
        self.l = l                      # Questa riga assegna il valore del parametro l all'attributo di istanza self.l. L'attributo l rappresenta la dimensione del lato della griglia.
        self.t = t                      # Questa riga assegna il valore del parametro t all'attributo di istanza self.t. L'attributo t rappresenta il numero di generazioni da eseguire.
        self.sigma = sigma              # Questa riga assegna il valore del parametro sigma all'attributo di istanza self.sigma. L'attributo sigma rappresenta la probabilità di avere una cella iniziale attiva.
        self.grid = self.create_grid()  # Questa riga chiama il metodo create_grid() e assegna il risultato all'attributo di istanza self.grid. Il metodo create_grid() genera la griglia iniziale del gioco utilizzando i valori di self.l e self.sigma.

    '''
    crea la griglia iniziale per il gioco. 
    Genera una griglia quadrata di dimensione l x l e assegna casualmente il valore 1 o 0 a ciascuna cella in base alla probabilità sigma fornita. 
    Una cella con valore 1 indica che è attiva, mentre 0 indica che è inattiva.
    '''
    def create_grid(self):                          # Questa riga definisce il metodo create_grid all'interno della classe. Il metodo non accetta alcun parametro aggiuntivo, ma utilizza gli attributi di istanza self.l e self.sigma.
        grid = []                                   # Questa riga inizializza una lista vuota chiamata grid che conterrà la griglia del gioco.
        for _ in range(self.l):                     # Questo ciclo for itera per self.l volte, creando righe nella griglia corrispondenti alla dimensione del lato.
            row = []                                # Questa riga inizializza una lista vuota chiamata row, che rappresenterà una riga della griglia.
            for _ in range(self.l):                 # Questo ciclo for itera per self.l volte, creando colonne nella riga corrente.
                if random.random() < self.sigma:    # Questa riga genera un numero casuale compreso tra 0 e 1 utilizzando random.random(). Se il numero generato è inferiore a self.sigma, allora viene aggiunto il valore 1 alla colonna corrente, indicando che la cella è attiva. Altrimenti, viene aggiunto il valore 0, indicando che la cella è inattiva.
                    row.append(1)                    
                else:                               # Se il numero generato non è inferiore a self.sigma, allora viene eseguito il blocco di codice all'interno del else. In questo caso, viene aggiunto il valore 0 alla colonna corrente, indicando che la cella è inattiva.
                    row.append(0)                   
            grid.append(row)                        # Questa riga aggiunge la riga appena creata alla griglia grid.
        return grid                                 # Questa riga restituisce la griglia completa come risultato della funzione.

    '''
    aggiorna la griglia alla generazione successiva del gioco. 
    Crea una nuova griglia vuota e, per ogni cella nella griglia corrente, conta il numero di vicini attivi chiamando il metodo count_neighbors(). 
    Successivamente, applica le regole del gioco: se una cella attiva ha meno di 2 o più di 3 vicini attivi, diventa inattiva nella nuova griglia. 
    Se una cella inattiva ha esattamente 3 vicini attivi, diventa attiva nella nuova griglia. Infine, assegna la nuova griglia all'attributo grid dell'oggetto.
    '''
    def update_generation(self):                        # Questa riga definisce il metodo update_generation all'interno della classe. Il metodo non accetta parametri aggiuntivi ma utilizza l'attributo di istanza self.l e il metodo count_neighbors.
        new_grid = []                                   # Questa riga inizializza una lista vuota chiamata new_grid che conterrà la nuova griglia generata nella generazione successiva.
        for row in range(self.l):                       # Questo ciclo for itera per ogni riga della griglia corrente.
            new_row = []                                # Questa riga inizializza una lista vuota chiamata new_row, che rappresenterà una riga della nuova griglia generata.
            for col in range(self.l):                   # Questo ciclo for itera per ogni colonna nella riga corrente.
                count = self.count_neighbors(row, col)  # Questa riga chiama il metodo count_neighbors passando le coordinate della cella corrente e memorizza il risultato nella variabile count. Il metodo count_neighbors conta il numero di vicini attivi della cella corrente.
                if self.grid[row][col] == 1:            # Questa riga controlla se la cella corrente nella griglia originale è attiva (1).
                    if count < 2 or count > 3:          #  Se la cella corrente è attiva e ha meno di 2 o più di 3 vicini attivi, allora viene eseguito il blocco di codice all'interno di questo if. Viene aggiunto il valore 0 (cella inattiva) alla nuova riga new_row.
                        new_row.append(0)
                    else:                               # Se la cella corrente è attiva e ha esattamente 2 o 3 vicini attivi, viene eseguito il blocco di codice all'interno di questo else. Viene aggiunto il valore 1 (cella attiva) alla nuova riga new_row.
                        new_row.append(1)
                else:                                   # Se la cella corrente nella griglia originale è inattiva (0).
                    if count == 3:                      # Se la cella corrente è inattiva e ha esattamente 3 vicini attivi, viene eseguito il blocco di codice all'interno di questo if. Viene aggiunto il valore 1 (cella attiva) alla nuova riga new_row.
                        new_row.append(1)
                    else:                               # Se la cella corrente è inattiva e non ha esattamente 3 vicini attivi, viene eseguito il blocco di codice all'interno di questo else. Viene aggiunto il valore 0 (cella inattiva) alla nuova riga new_row.
                        new_row.append(0)
            new_grid.append(new_row)                    # Questa riga aggiunge la nuova riga new_row alla nuova griglia new_grid.
        self.grid = new_grid                            # Alla fine del metodo, l'attributo grid della classe viene aggiornato con la nuova griglia new_grid.
        
    '''
     conta il numero di vicini attivi per una determinata cella nella griglia. 
     Scorre le celle adiacenti in un raggio di 1 intorno alla cella di interesse e tiene traccia del numero di celle attive trovate.
    '''    
    def count_neighbors(self, row, col):                        # Questa riga definisce il metodo count_neighbors all'interno della classe. Il metodo accetta due parametri aggiuntivi: row e col, che rappresentano le coordinate della cella di interesse.
        count = 0                                               # Questa riga inizializza la variabile count a 0, che conterà il numero di vicini attivi.
        for i in [-1, 0, 1]:                                    # Questo ciclo for itera attraverso i valori -1, 0 e 1, che rappresentano gli spostamenti possibili nella dimensione verticale della griglia rispetto alla cella di interesse.
            for j in [-1, 0, 1]:                                # Questo ciclo for itera attraverso i valori -1, 0 e 1, che rappresentano gli spostamenti possibili nella dimensione orizzontale della griglia rispetto alla cella di interesse.
                if i == 0 and j == 0:                           # Questa riga controlla se sia i che j sono entrambi 0. Se è vero, significa che la cella di interesse è quella stessa cella in cui stiamo cercando i vicini, quindi viene eseguito il blocco di codice all'interno di questo if.
                    continue                                    # Questa parola chiave fa saltare il resto del blocco di codice all'interno del ciclo più interno, in modo che non venga eseguita alcuna operazione per questa cella stessa.
                neighbor_row = (row + i + self.l) % self.l      # Questa riga calcola l'indice della riga del vicino corrente utilizzando l'aritmetica modulare per assicurarsi che gli indici siano validi anche per le celle al bordo della griglia. Aggiungendo row + i + self.l e quindi calcolando il modulo self.l, otteniamo l'indice corretto.
                neighbor_col = (col + j + self.l) % self.l      # Questa riga calcola l'indice della colonna del vicino corrente utilizzando lo stesso approccio di aritmetica modulare come sopra.
                count += self.grid[neighbor_row][neighbor_col]  # Questa riga incrementa il valore di count aggiungendo il valore della cella corrispondente alla posizione del vicino corrente nella griglia.
        return count                                            # Alla fine del metodo, viene restituito il valore di count, che rappresenta il numero totale di vicini attivi intorno alla cella di interesse.

    '''
    crea un'istanza della classe GameOfLife, stampa la griglia iniziale 
    e successivamente esegue un ciclo di generazioni chiamando il metodo update_generation() 
    e stampando la griglia aggiornata ad ogni passo.
    '''
def test_game_of_life():            # Vedere se metterla
    # Test per la classe GameOfLife
    game = GameOfLife(10, 5, 0.5)
    print(game.grid)

    for _ in range(game.t):
        game.update_generation()
        print(game.grid)

'''
Questa classe combina gli aspetti dell'interfaccia utente tramite Tkinter e la visualizzazione grafica del gioco tramite Turtle. 
L'interazione dell'utente avviene attraverso i campi di inserimento e i pulsanti, consentendo di avviare, caricare e salvare simulazioni del "Gioco della vita".
'''
class GameOfLifeGUI:
    
    '''
    viene inizializzata una finestra principale utilizzando la libreria Tkinter (tk.Tk()). 
    Vengono anche creati vari elementi dell'interfaccia utente come etichette (tk.Label), campi di inserimento (tk.Entry) e pulsanti (tk.Button). 
    La finestra viene quindi avviata tramite il metodo mainloop().
    '''
    def __init__(self):                                                             # Questa riga definisce il metodo __init__, che è il costruttore della classe GameOfLifeGUI. Non accetta argomenti aggiuntivi.
        self.window = tk.Tk()                                                       # Questa riga crea una nuova finestra utilizzando la libreria Tkinter (tk.Tk()) e assegna l'oggetto finestra alla variabile di istanza self.window.
        self.window.title('Game of Life')                                           # Questa riga imposta il titolo della finestra come "Game of Life".

        self.is_closing = False  # Flag per la chiusura                             # Questa riga inizializza una variabile di istanza chiamata is_closing e la imposta su False. Questa variabile verrà utilizzata come flag per indicare se la finestra sta per essere chiusa.

        self.label_l = tk.Label(self.window, text='Lato (l):')                      # Questa riga crea un widget di etichetta (Label) con il testo "Lato (l):" e lo associa alla finestra self.window. L'etichetta sarà utilizzata per indicare l'input del lato della griglia.
        self.label_l.pack()                                                         # Questa riga posiziona l'etichetta nella finestra utilizzando il metodo pack().
        self.entry_l = tk.Entry(self.window)                                        # Questa riga crea un widget di input (Entry) e lo associa alla finestra self.window. Sarà utilizzato per inserire il valore del lato della griglia.
        self.entry_l.pack()                                                         # Questa riga posiziona l'input nella finestra utilizzando il metodo pack().

        self.label_t = tk.Label(self.window, text='Numero di passi (t):')           # Le righe successive seguono lo stesso schema per creare etichette e campi di inserimento per i valori del numero di passi (self.label_t e self.entry_t) e la percentuale di riempimento (self.label_sigma e self.entry_sigma).
        self.label_t.pack()                                                         #
        self.entry_t = tk.Entry(self.window)                                        #
        self.entry_t.pack()                                                         #

        self.label_sigma = tk.Label(                                                
            self.window, text='Percentuale di riempimento (0<σ<1):')                #
        self.label_sigma.pack()                                                     #
        self.entry_sigma = tk.Entry(self.window)                                    #
        self.entry_sigma.pack()                                                     #

        self.button_start = tk.Button(                          
            self.window, text='Avvia Simulazione', command=self.start_simulation)   # Questa riga crea un pulsante (Button) con il testo "Avvia Simulazione" e lo associa alla finestra self.window. Il pulsante chiamerà il metodo start_simulation quando viene premuto.
        self.button_start.pack()                                                    # Questa riga posiziona il pulsante nella finestra utilizzando il metodo pack().

        self.button_load = tk.Button(
            self.window, text='Carica Simulazione', command=self.load_simulation)   # Questa riga crea un altro pulsante (Button) con il testo "Carica Simulazione" e lo associa alla finestra self.window. Il pulsante chiamerà il metodo load_simulation quando viene premuto.
        self.button_load.pack()                                                     # Questa riga posiziona il secondo pulsante nella finestra utilizzando il metodo pack().

        # Associa il metodo on_closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)                   # Questa riga associa il metodo on_closing alla chiusura della finestra, in modo che venga eseguito quando l'utente cerca di chiudere la finestra.

        self.window.mainloop()                                                      # Questa riga avvia il ciclo principale dell'interfaccia grafica Tkinter, che gestisce gli eventi e gli aggiornamenti della finestra. Il programma rimarrà in questo ciclo finché la finestra non viene chiusa dall'utente.

    '''
    viene chiamato quando viene premuto il pulsante "Avvia Simulazione". 
    Recupera i valori inseriti negli elementi di inserimento (entry_l, entry_t, entry_sigma), 
    converte i valori in tipi appropriati e crea un'istanza della classe GameOfLife. 
    Quindi utilizza la libreria Turtle per visualizzare la simulazione del gioco sulla finestra creata precedentemente.
    '''
    def start_simulation(self):                                 # Questa riga definisce il metodo start_simulation all'interno della classe GameOfLifeGUI. Il metodo non accetta argomenti aggiuntivi.
        l = int(self.entry_l.get())                             # Questa riga recupera il valore inserito nel campo di inserimento entry_l (che rappresenta il lato della griglia) e lo converte in un intero utilizzando la funzione int(). Il valore convertito viene assegnato alla variabile l.
        t = int(self.entry_t.get())                             # Questa riga recupera il valore inserito nel campo di inserimento entry_t (che rappresenta il numero di passi) e lo converte in un intero utilizzando la funzione int(). Il valore convertito viene assegnato alla variabile t.
        sigma = float(self.entry_sigma.get())                   # Questa riga recupera il valore inserito nel campo di inserimento entry_sigma (che rappresenta la percentuale di riempimento) e lo converte in un valore float utilizzando la funzione float(). Il valore convertito viene assegnato alla variabile sigma.
        self.game = GameOfLife(l, t, sigma)                     # Questa riga crea un'istanza della classe GameOfLife utilizzando i valori l, t e sigma ottenuti dai campi di inserimento. L'istanza viene assegnata all'attributo di istanza self.game.
        self.l = l  # Inizializza l'attributo 'l' nella classe  # Questa riga inizializza l'attributo di istanza l nella classe GameOfLifeGUI con il valore di l ottenuto dai campi di inserimento.

        turtle_screen = turtle.Screen()                         # Questa riga crea un oggetto Screen dalla libreria Turtle e lo assegna alla variabile turtle_screen. Sarà utilizzato per la visualizzazione grafica della simulazione.
        turtle_screen.title('Game of Life')                     # Questa riga imposta il titolo della finestra di visualizzazione Turtle come "Game of Life".
        turtle_screen.setup(width=800, height=800)              # Questa riga imposta le dimensioni della finestra di visualizzazione Turtle su 800x800 pixel.

        turtle_pen = turtle.Turtle()                            # Questa riga crea un oggetto Turtle dalla libreria Turtle e lo assegna alla variabile turtle_pen. Sarà utilizzato per disegnare la griglia e le celle colorate.
        turtle_pen.speed(0)                                     # Questa riga imposta la velocità del pennarello Turtle a 0, il che significa che si muoverà alla massima velocità.
        turtle_pen.hideturtle()                                 # Questa riga nasconde il pennarello Turtle in modo che non sia visibile durante il disegno della griglia e delle celle.

        cell_size = 800 / l                                     # Questa riga calcola la dimensione delle celle sulla base del lato l e le dimensioni della finestra di visualizzazione. Divide la larghezza (800) per il lato l per ottenere la dimensione di ogni cella.

        for _ in range(t):                                      # Questo ciclo for itera per t volte, che rappresenta il numero di passi della simulazione.
            self.draw_grid(turtle_pen, cell_size)               # Questa riga chiama il metodo draw_grid passando il pennarello turtle_pen e la dimensione delle celle cell_size. Il metodo draw_grid si occupa di disegnare la griglia e le celle colorate sulla finestra di visualizzazione.
            self.game.update_generation()                       # Questa riga chiama il metodo update_generation dell'oggetto self.game (un'istanza della classe GameOfLife). Questo metodo aggiorna la generazione del gioco.

        turtle_screen.bye()                                     # Questa riga chiude la finestra di visualizzazione Turtle.
        self.on_closing()                                       # Questa riga chiama il metodo on_closing per gestire la chiusura della finestra principale.

    '''
    viene chiamato quando viene premuto il pulsante "Carica Simulazione". 
    Apre una finestra di dialogo per selezionare un file di testo (.txt) contenente una griglia per il gioco. 
    Legge il file, analizza le informazioni per ottenere la dimensione della griglia, crea un'istanza della classe GameOfLife 
    e popola la griglia con i valori letti dal file. Successivamente, utilizza la libreria Turtle per visualizzare la simulazione del gioco sulla finestra.
    '''
    def load_simulation(self):                                                              # Questa riga definisce il metodo load_simulation all'interno della classe GameOfLifeGUI. Il metodo non accetta argomenti aggiuntivi.
        filename = filedialog.askopenfilename(
            title='Carica Simulazione', filetypes=[('Text Files', '*.txt')])                # Questa riga apre una finestra di dialogo per selezionare un file da caricare. La finestra di dialogo mostra solo i file di testo con estensione .txt. Il percorso completo del file selezionato viene assegnato alla variabile filename.
        if filename:                                                                        # Questa riga controlla se filename contiene un percorso di file valido (cioè se l'utente ha selezionato un file e non ha annullato la finestra di dialogo).
            try:                                                                            # Questa riga inizia un blocco di codice che verrà eseguito e gestito in caso di eccezioni.
                with open(filename, 'r') as file:                                           # Questa riga apre il file specificato da filename in modalità di lettura ('r') utilizzando un blocco with. Ciò garantisce che il file venga chiuso correttamente alla fine, indipendentemente da eventuali eccezioni.
                    lines = file.readlines()                                                # Questa riga legge tutte le righe del file e le memorizza nella lista lines.
                    l = len(lines)                                                          # Questa riga calcola la lunghezza della lista lines e la assegna alla variabile l. Questo valore rappresenta il lato della griglia basato sul numero di righe nel file.
                    t = int(self.entry_t.get())                                             # Questa riga recupera il valore del numero di passi dal campo di inserimento entry_t e lo converte in un intero utilizzando la funzione int(). Il valore convertito viene assegnato alla variabile t.
                    sigma = float(self.entry_sigma.get())                                   # Questa riga recupera il valore della percentuale di riempimento dal campo di inserimento entry_sigma e lo converte in un valore float utilizzando la funzione float(). Il valore convertito viene assegnato alla variabile sigma.
                    self.game = GameOfLife(l, t, sigma)                                     # Questa riga crea un'istanza della classe GameOfLife utilizzando i valori l, t e sigma ottenuti dal file e dai campi di inserimento. L'istanza viene assegnata all'attributo di istanza self.game.
                    for row, line in enumerate(lines):                                      # Questo ciclo for itera attraverso le righe nella lista lines, assegnando l'indice della riga a row e il contenuto della riga a line.
                        for col, value in enumerate(line.strip()):                          # Questo ciclo for itera attraverso i caratteri nella riga line (dopo aver rimosso gli spazi iniziali e finali con strip()), assegnando l'indice del carattere a col e il carattere stesso a value.
                            self.game.grid[row][col] = int(value)                           # Questa riga converte il valore del carattere value in un intero utilizzando int() e lo assegna alla cella corrispondente nella griglia self.game.grid utilizzando gli indici row e col.

                    turtle_screen = turtle.Screen()                                         # Le righe da 10 a 13 seguono lo stesso schema del codice nel metodo start_simulation per creare la finestra di visualizzazione Turtle, il pennarello e la dimensione delle celle.
                    turtle_screen.title('Game of Life')                                     #
                    turtle_screen.setup(width=800, height=800)                              #

                    turtle_pen = turtle.Turtle()                                            #
                    turtle_pen.speed(0)                                                     #
                    turtle_pen.hideturtle()                                                 #

                    cell_size = 800 / l                                                     #

                    for _ in range(t):                                                      # Questo ciclo for itera per t volte, che rappresenta il numero di passi della simulazione.
                        self.draw_grid(turtle_pen, cell_size)                               # Questa riga chiama il metodo draw_grid passando il pennarello turtle_pen e la dimensione delle celle cell_size. Il metodo draw_grid si occupa di disegnare la griglia e le celle colorate sulla finestra di visualizzazione.
                        self.game.update_generation()                                       # Questa riga chiama il metodo update_generation dell'oggetto self.game (un'istanza della classe GameOfLife). Questo metodo aggiorna la generazione del gioco.

                    turtle_screen.bye()                                                     # Questa riga chiude la finestra di visualizzazione Turtle.
                    self.on_closing()                                                       # Questa riga chiama il metodo on_closing per gestire la chiusura della finestra principale.

            except Exception as e:                                                          # Questa riga cattura qualsiasi eccezione che si verifica all'interno del blocco try e la assegna alla variabile e. Ma non esiste e..
                messagebox.showerror(                   
                    'Errore', 'Si è verificato un errore durante il caricamento del file.') # Questa riga mostra una finestra di dialogo di errore che indica all'utente che si è verificato un errore durante il caricamento del file.
    '''
    viene chiamato quando viene premuto il pulsante "Salva Simulazione". 
    Apre una finestra di dialogo per selezionare il percorso di destinazione e il nome del file di testo (.txt) 
    in cui verrà salvata la griglia corrente del gioco.
    '''
    def save_simulation(self):                                                              # Questa riga definisce il metodo save_simulation all'interno della classe GameOfLifeGUI. Il metodo non accetta argomenti aggiuntivi.
        filename = filedialog.asksaveasfilename(
            title='Salva Simulazione', defaultextension='.txt')                             # Questa riga apre una finestra di dialogo per selezionare il percorso e il nome del file in cui salvare la simulazione. Il titolo della finestra di dialogo è impostato su "Salva Simulazione" e l'estensione predefinita del file è .txt. Il percorso completo del file selezionato viene assegnato alla variabile filename.
        if filename:                                                                        # Questa riga controlla se filename contiene un percorso di file valido (cioè se l'utente ha selezionato un percorso e non ha annullato la finestra di dialogo).
            try:                                                                            # Questa riga inizia un blocco di codice che verrà eseguito e gestito in caso di eccezioni.
                with open(filename, 'w') as file:                                           # Questa riga apre il file specificato da filename in modalità di scrittura ('w') utilizzando un blocco with. Ciò garantisce che il file venga chiuso correttamente alla fine, indipendentemente da eventuali eccezioni.
                    for row in self.game.grid:                                              # Questo ciclo for itera attraverso le righe della griglia self.game.grid.
                        line = ''.join(map(str, row))                                       # Questa riga converte ogni elemento della riga in una stringa utilizzando la funzione str() e li concatena in una singola stringa senza spazi intermedi utilizzando join(). Il risultato viene assegnato alla variabile line.
                        file.write(line + '\n')                                             # Questa riga scrive la stringa line nel file, seguita da un carattere di nuova riga (\n), per rappresentare una riga nella griglia.

                messagebox.showinfo(
                    'Salvataggio', 'Simulazione salvata correttamente.')                    # Questa riga mostra una finestra di dialogo informativa che indica all'utente che la simulazione è stata salvata correttamente.

            except Exception as e:                                                          # Questa riga cattura qualsiasi eccezione che si verifica all'interno del blocco try e la assegna alla variabile e.
                messagebox.showerror(
                    'Errore', 'Si è verificato un errore durante il salvataggio del file.') # Questa riga mostra una finestra di dialogo di errore che indica all'utente che si è verificato un errore durante il salvataggio del file.

    '''
     viene utilizzato per disegnare la griglia e le celle colorate utilizzando la libreria Turtle. 
     Questo metodo viene chiamato ad ogni passo della simulazione per aggiornare la visualizzazione della griglia.
    '''
    def draw_grid(self, pen, cell_size):                        # Questa riga definisce il metodo draw_grid all'interno della classe GameOfLifeGUI. Il metodo accetta due argomenti: pen, che rappresenta il pennarello Turtle, e cell_size, che rappresenta la dimensione di una singola cella nella griglia.
        pen.reset()                                             # Questa riga resetta il pennarello Turtle allo stato iniziale.
        turtle_screen = pen.getscreen()                         # Questa riga ottiene l'oggetto Screen associato al pennarello Turtle.
        turtle_screen.tracer(0)                                 # Questa riga disattiva l'animazione automatica, consentendo di visualizzare immediatamente le modifiche sulla finestra di visualizzazione.

        pen.hideturtle()  # Nascondi la freccia di turtle       # Questa riga nasconde la freccia del pennarello Turtle.

        # Disegna la griglia fissa
        pen.penup()                                             # Questa riga alza la penna del pennarello in modo che non venga disegnata alcuna linea durante i movimenti.
        x_start = -400                                          # Queste righe definiscono le coordinate di partenza per il disegno della griglia.
        y_start = 400                                           # 

        # Disegna le linee verticali
        for col in range(self.l + 1):                           # Questo ciclo for itera attraverso le colonne della griglia più una colonna extra per disegnare la griglia fissa.
            x = x_start + col * cell_size                       # Le righe da 9 a 13 disegnano le linee verticali della griglia. La variabile x rappresenta la coordinata x di una linea verticale, mentre y1 e y2 rappresentano le coordinate y iniziale e finale della linea. Il pennarello si sposta alla posizione (x, y1), abbassa la penna, si sposta alla posizione (x, y2), alza la penna e passa alla colonna successiva.
            y1 = y_start                                        #
            y2 = y_start - self.l * cell_size                   #
            pen.goto(x, y1)                                     #
            pen.pendown()                                       #
            pen.goto(x, y2)                                     #
            pen.penup()                                         #

        # Disegna le linee orizzontali
        for row in range(self.l + 1):                           # Questo ciclo for itera attraverso le righe della griglia più una riga extra per disegnare la griglia fissa.
            y = y_start - row * cell_size                       # Le righe da 11 a 15 disegnano le linee orizzontali della griglia. La variabile y rappresenta la coordinata y di una linea orizzontale, mentre x1 e x2 rappresentano le coordinate x iniziale e finale della linea. Il pennarello si sposta alla posizione (x1, y), abbassa la penna, si sposta alla posizione (x2, y), alza la penna e passa alla riga successiva.
            x1 = x_start                                        #
            x2 = x_start + self.l * cell_size                   #
            pen.goto(x1, y)                                     #
            pen.pendown()                                       #
            pen.goto(x2, y)                                     #
            pen.penup()                                         # 

        # Disegna le celle colorate
        for row in range(len(self.game.grid)):                  #Le righe da 17 a 28 disegnano le celle colorate della griglia.     
            for col in range(len(self.game.grid[row])):         #I cicli for nidificati iterano attraverso ogni cella nella griglia del gioco self.game.grid.
                x = x_start + col * cell_size + 1               #Le variabili row e col rappresentano le coordinate della cella nella griglia. La variabile x rappresenta la coordinata x dell'angolo in alto a sinistra della cella, mentre y rappresenta la coordinata y dell'angolo in alto a sinistra della cella.
                y = y_start - row * cell_size - 1               #Il pennarello si sposta alla posizione (x, y), alza la penna, controlla il valore della cella nella griglia del gioco e se è 1 (viva), disegna un quadrato riempito di colore nero.

                pen.penup()                                     #Il pennarello riempie il quadrato iterando quattro volte, spostandosi in avanti di una distanza pari alla dimensione di una cella ridotta di 2 unità e ruotando a destra di 90 gradi dopo ogni movimento.
                pen.goto(x, y)                                  #Alla fine, il pennarello termina il riempimento e passa alla cella successiva.

                if self.game.grid[row][col] == 1:               #
                    pen.pendown()                               #
                    pen.fillcolor('black')                      #
                    pen.begin_fill()                            #
                    for _ in range(4):                          #
                        pen.forward(cell_size - 2)              #
                        pen.right(90)                           #
                    pen.end_fill()                              #

        turtle_screen.update()                                  # Questa riga aggiorna la finestra di visualizzazione Turtle per mostrare il disegno aggiornato.
        time.sleep(1)                                           # Questa riga mette in pausa l'esecuzione per 1 secondo, consentendo di visualizzare la griglia per un breve periodo prima di passare alla generazione successiva.

    '''
     viene chiamato quando viene chiusa la finestra principale. 
     Se l'utente conferma di voler salvare lo stato corrente del gioco, chiama il metodo save_simulation() per salvare la griglia corrente su un file di testo.
    '''
    
    def on_closing(self):                                                                   # Questa riga definisce il metodo on_closing all'interno della classe GameOfLifeGUI. Il metodo non accetta argomenti aggiuntivi.
        if self.is_closing:                                                                 # Questa riga verifica se il flag is_closing è impostato. Se il flag è già impostato, significa che la finestra di gioco è in fase di chiusura e il metodo esce senza eseguire ulteriori azioni.
            return                                                                          # 

        self.is_closing = True  # Imposta il flag di chiusura                               # Questa riga imposta il flag is_closing su True. Questo indica che la finestra di gioco sta per essere chiusa.

        if messagebox.askyesno('Salvataggio', 'Vuoi salvare lo stato corrente del gioco?'): # Questa riga mostra una finestra di dialogo di conferma con il titolo "Salvataggio" e il messaggio "Vuoi salvare lo stato corrente del gioco?". L'utente può selezionare "Yes" o "No". Se l'utente seleziona "Yes", il blocco di codice successivo viene eseguito. Se l'utente seleziona "No", il blocco successivo viene saltato.
            self.save_simulation()                                                          # Questa riga chiama il metodo save_simulation per salvare lo stato corrente del gioco.

        self.window.destroy()                                                               # Questa riga distrugge la finestra principale dell'applicazione. Chiude effettivamente l'applicazione.


if __name__ == '__main__':                      # Questa riga controlla se lo script viene eseguito come modulo principale. Il blocco di codice successivo verrà eseguito solo se lo script viene eseguito direttamente e non importato come modulo in un altro script.
    # Esegui il test della classe GameOfLife
    test_game_of_life()                         # Questa riga chiama la funzione test_game_of_life() per eseguire il test della classe GameOfLife. Questa funzione stampa la griglia iniziale e la griglia dopo ogni generazione.

    # Crea e avvia l'interfaccia grafica        
    gui = GameOfLifeGUI()                       # Questa riga crea un'istanza della classe GameOfLifeGUI e la assegna alla variabile gui. Questo avvia l'interfaccia grafica del gioco della vita.
