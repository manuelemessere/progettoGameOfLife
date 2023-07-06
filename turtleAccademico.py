#Senza classi, ma con griglia
import turtle
import random
import copy

screen = turtle.Screen()
turtle.setup(1000, 1000)
turtle.title("Conway's Game of Life - PythonTurtle.Academy")
turtle.hideturtle()
turtle.speed(0)
turtle.tracer(0, 0)

grid_turtle = turtle.Turtle()  # turtle for drawing grid
grid_turtle.up()
grid_turtle.hideturtle()
grid_turtle.speed(0)
grid_turtle.pencolor('gray')
grid_turtle.pensize(3)

n = 50  # nxn grid


def draw_line(x1, y1, x2, y2):  # this function draw a line between x1,y1 and x2,y2
    grid_turtle.up()
    grid_turtle.goto(x1, y1)
    grid_turtle.down()
    grid_turtle.goto(x2, y2)


def draw_grid():  # this function draws nxn grid
    x = -400
    for i in range(n + 1):
        draw_line(x, -400, x, 400)
        x += 800 / n
    y = -400
    for i in range(n + 1):
        draw_line(-400, y, 400, y)
        y += 800 / n


life = list()  # create an empty list


def init_lives():
    for i in range(n):
        liferow = []  # a row of lives
        for j in range(n):
            if random.randint(0, 7) == 0:  # 1/7 probability of life
                liferow.append(1)  # 1 means life
            else:
                liferow.append(0)  # 0 means no life
        life.append(liferow)  # add a row to the life list -> life is a list of list


def draw_square(x, y, size):  # draws a filled square
    turtle.up()
    turtle.goto(x, y)
    turtle.down()
    turtle.seth(0)
    turtle.begin_fill()
    for _ in range(4):
        turtle.fd(size)
        turtle.left(90)
    turtle.end_fill()


def draw_life(x, y):  # draws life in (x,y)
    lx = 800 / n * x - 400  # converts x,y to screen coordinate
    ly = 800 / n * y - 400
    draw_square(lx + 1, ly + 1, 800 / n - 2)


def draw_all_life():  # draws all life
    global life
    for i in range(n):
        for j in range(n):
            if life[i][j] == 1:
                draw_life(i, j)  # draw live cells


def num_neighbors(x, y):  # computes the number of life neighbours for cell[x,y]
    total = 0
    for i in range(max(x - 1, 0), min(x + 1, n - 1) + 1):
        for j in range(max(y - 1, 0), min(y + 1, n - 1) + 1):
            total += life[i][j]
    return total - life[x][y]


def update_life():  # update life for each cycle
    global life
    new_life = copy.deepcopy(life)  # make a copy of life
    for i in range(n):
        for j in range(n):
            k = num_neighbors(i, j)
            if k < 2 or k > 3:
                new_life[i][j] = 0
            elif k == 3:
                new_life[i][j] = 1
    life = copy.deepcopy(new_life)  # copy back to life
    turtle.clear()  # clears life in previous cycle
    draw_all_life()
    screen.update()
    screen.ontimer(update_life, 200)  # update life every 0.2 second


draw_grid()
init_lives()
draw_all_life()
screen.update()
grid_turtle.hideturtle()  # Hide the grid turtle
screen.ontimer(update_life, 200)
turtle.done()


#Con le classi, ma senza griglia
import turtle
import random
import copy

class Script:
    def __init__(self, n):
        self.n = n
        self.life = []

    def init_lives(self):
        for i in range(self.n):
            liferow = []
            for j in range(self.n):
                if random.randint(0, 7) == 0:
                    liferow.append(1)
                else:
                    liferow.append(0)
            self.life.append(liferow)

    def num_neighbors(self, x, y):
        total = 0
        for i in range(max(x - 1, 0), min(x + 1, self.n - 1) + 1):
            for j in range(max(y - 1, 0), min(y + 1, self.n - 1) + 1):
                total += self.life[i][j]
        return total - self.life[x][y]

    def update_life(self):
        new_life = copy.deepcopy(self.life)
        for i in range(self.n):
            for j in range(self.n):
                k = self.num_neighbors(i, j)
                if k < 2 or k > 3:
                    new_life[i][j] = 0
                elif k == 3:
                    new_life[i][j] = 1
        self.life = copy.deepcopy(new_life)


class GUI:
    def __init__(self, script, screen):
        self.script = script
        self.screen = screen
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)

    def draw_grid(self):
        self.turtle.up()
        self.turtle.goto(-400, -400)
        self.turtle.down()
        self.turtle.pencolor('gray')
        self.turtle.pensize(3)
        for _ in range(self.script.n + 1):
            self.turtle.forward(800 / self.script.n)
            self.turtle.left(90)
            self.turtle.forward(800)
            self.turtle.right(90)

    def draw_square(self, x, y, size):
        lx = 800 / self.script.n * x - 400
        ly = 800 / self.script.n * y - 400
        self.turtle.up()
        self.turtle.goto(lx + 1, ly + 1)
        self.turtle.down()
        self.turtle.begin_fill()
        for _ in range(4):
            self.turtle.forward(size)
            self.turtle.left(90)
        self.turtle.end_fill()

    def draw_all_life(self):
        for i in range(self.script.n):
            for j in range(self.script.n):
                if self.script.life[i][j] == 1:
                    self.draw_square(i, j, 800 / self.script.n - 2)

    def update_and_draw(self):
        self.script.update_life()
        self.turtle.clear()
        self.draw_all_life()
        self.screen.update()
        self.screen.ontimer(self.update_and_draw, 200)

def main():
    screen = turtle.Screen()
    turtle.setup(1000, 1000)
    turtle.title("Conway's Game of Life - PythonTurtle.Academy")
    turtle.speed(0)
    turtle.tracer(0, 0)

    n = 50
    script = Script(n)
    script.init_lives()

    gui = GUI(script, screen)
    gui.draw_grid()
    gui.draw_all_life()
    screen.update()

    gui.screen.ontimer(gui.update_and_draw, 200)

    turtle.done()

if __name__ == "__main__":
    main()
