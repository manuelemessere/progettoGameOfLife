#problema: esegue sequenzialmente il calcolo del gioco; manca la griglia
#togliere le stampe di ogni vita e morte
#pro: usa turtle, divisione in classi
import turtle
import tkinter as tk
import random

screen = turtle.Screen()
screen.bgcolor("black")
turtle.ht()

turtle.speed(5)
turtle.delay(0)


class GameOfLife:

    def __init__(self, x, y, stato, world):
        self.x = x
        self.y = y
        self.stato = stato
        self.world = world

    def nascita_cella(self):
        turtle.up()
        turtle.goto((self.x * 20) - 400, (self.y * 20) - 100)
        turtle.dot(12, "green")

        self.stato = True

    def morte_cella(self):
        turtle.up()
        turtle.goto((self.x * 20) - 400, (self.y * 20) - 100)
        turtle.dot(12, "black")

        self.stato = False

    def __str__(self):
        return "cell status: " + str(self.stato)

    def numero_vicini_vivi(self):
        contatore = 0
        indice_originale = self.world.conversion(self.x, self.y)

        for i in [0, 1, -1]:
            for j in [0, 1, -1]:
                indice = self.world.conversion(self.x + i, self.y + j)

                if indice == indice_originale:
                    continue
                else:
                    if self.world.cella_viva((self.x + i), (self.y + j)):
                        contatore += 1

        return contatore

    def generazione_successiva(self):
        condizione = self.world.cella_viva(self.x, self.y)

        if condizione is False:
            if self.numero_vicini_vivi() == 3:
                return "nascita"
            else:
                return "rimane morta"
        else:
            if self.numero_vicini_vivi() < 2 or self.numero_vicini_vivi() > 3:
                return "morta"
            else:
                return "rimane viva"


class World:

    def __init__(self, edge_len):
        self.edge_len = edge_len
        self.n_celle_vive = 0
        self.time = 0
        self.n_celle_vive = self.edge_len ** 2
        self.lista_celle = []

    def creazione_griglia(self):
        for y in range(self.edge_len):
            for x in range(self.edge_len):
                self.lista_celle.append(GameOfLife(x, y, False, self))
        return self.lista_celle

    def conversion(self, x, y):
        x = x
        y = int(y * self.edge_len)
        index = x + y
        return index

    def re_conversion(self, index):
        y = int(index / self.edge_len)
        if y == 0:
            x = index
        else:
            x = int(index - (self.edge_len * y))
        if index in range(len(self.lista_celle)):
            return x, y
        else:
            return False

    def cella_viva(self, coordinata_x, coordinata_y):
        indice = self.conversion(coordinata_x, coordinata_y)
        if indice in range(len(self.lista_celle)):
            if self.lista_celle[indice].stato is True:
                return True
            else:
                return False
        else:
            return False

    def tick(self):
        self.time += 1
        query_stato = []

        for stat in self.lista_celle:
            query_stato.append(stat.generazione_successiva())

        for indice in range(len(query_stato)):
            stat_check = query_stato[indice]
            if stat_check == "nascita":
                self.lista_celle[indice].nascita_cella()
            elif stat_check == "morta":
                self.lista_celle[indice].morte_cella()

        self.n_celle_vive = 0

        for stato_celle in self.lista_celle:
            if stato_celle.stato is True:
                self.n_celle_vive += 1
            else:
                return False

    def switch_on(self, coordinata_x, coordinata_y):
        valore_indice = self.conversion(coordinata_x, coordinata_y)
        if valore_indice in range(len(self.lista_celle)):
            self.lista_celle[valore_indice].nascita_cella()
            self.n_celle_vive += 1

    def mostra_celle(self):
        for i in range(len(self.lista_celle)):
            print("cell #" + str(i + 1), str(self.lista_celle[i]))


world1 = World(20)
world1.creazione_griglia()

for i in range(int(int(world1.edge_len ** 2) / 2)):
    world1.switch_on(random.randint(0, world1.edge_len),
                     random.randint(0, world1.edge_len))

while world1.time < 100:
    world1.tick()
    screen.update()
