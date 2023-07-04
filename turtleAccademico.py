#problema: non segue i movimenti del gioco
import turtle
import random
import copy

screen = turtle.Screen()
turtle.setup(1000, 1000)
turtle.title("Conway's Game of Life - PythonTurtle.Academy")
turtle.speed(0)
turtle.tracer(0, 0)

n = 50  # nxn grid

def draw_line(x1, y1, x2, y2):  # this function draw a line between x1,y1 and x2,y2
    turtle.up()
    turtle.goto(x1, y1)
    turtle.down()
    turtle.goto(x2, y2)


def draw_grid():  # this function draws nxn grid
    turtle.pencolor('gray')
    turtle.pensize(3)
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
    for i in range(n):
        for j in range(n):
            if life[i][j] == 1:
                draw_life(i, j)  # draw live cells


def num_neighbors(x, y):  # computes the number of life neighbours for cell[x,y]
    sum = 0
    for i in range(max(x - 1, 0), min(x + 1, n - 1) + 1):
        for j in range(max(y - 1, 0), min(y + 1, n - 1) + 1):
            sum += life[i][j]
    return sum - life[x][y]


def update_life():  # update life for each cycle
    global life
    newlife = copy.deepcopy(life)  # make a copy of life
    changed_cells = []

    for i in range(n):
        for j in range(n):
            k = num_neighbors(i, j)
            if k < 2 or k > 3:
                newlife[i][j] = 0
                if life[i][j] == 1:
                    changed_cells.append((i, j))
            elif k == 3 and life[i][j] == 0:
                newlife[i][j] = 1
                changed_cells.append((i, j))

    life = copy.deepcopy(newlife)  # copy back to life

    for cell in changed_cells:
        draw_life(cell[0], cell[1])

    screen.update()
    screen.ontimer(update_life, 200)  # update life every 0.2 seconds


draw_grid()
init_lives()
draw_all_life()
update_life()

turtle.done()
