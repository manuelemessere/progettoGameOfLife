#problema: esegue sequenzialmente il calcolo del gioco; manca la griglia
#togliere le stampe di ogni vita e morte
#pro: usa turtle, divisione in classi
#!/usr/bin/env python
# coding: utf-8

# In[4]:


import turtle
import random

scr = turtle.Screen()
turtle.ht()  # hide turtle
scr.bgcolor("black")
turtle.speed(5) #modificare in modo che l'utente possa selezionare la velocità 
turtle.delay(0)



class Cell:
	def __init__(self, x, y, status, world):
		self.x = x
		self.y = y
		self.world = world
		self.status = status

	def birth(self):

		turtle.up()
		turtle.setpos((self.x*20)-400, (self.y*20)-100) #scoprire cosa significa e come funziona
		turtle.dot(10, "green")

		self.status = True

	def death(self):
		turtle.up()
		turtle.setpos((self.x*20)-400, (self.y*20)-100)
		turtle.dot(10, "black")

		self.status = False

	def __str__(self):
		return "cell status: " + str(self.status)

	# Gets number of live cells in 8 squares around it.
	def get_number_live_neighbours(self):
		counter = 0
		index_original = self.world.conversion(self.x, self.y)
		# Converts co-ordinates to index to be altered and evaluated.
		for i in [0, 1, -1]:
			for j in [0, 1, -1]:
				# only 3 values needs to be changed for 8 surrounding
				index = self.world.conversion(self.x+i, self.y+j)
				if index == index_original:  # all status of neighbours
									#  only therefore exclude asking cell
					continue
				else:
					if self.world.is_cell_alive((self.x + i), (self.y + j)) is True:
						counter += 1
		return counter

	def get_next_status(self):
		#  Gets status of each cell and store them in list to be evaluated after.
		condition = self.world.is_cell_alive(self.x, self.y)
		# print("Debug condition: " + condition)
		# index_current_cell = self.world.conversion(self.x, self.y)

		# print("Debug Index of current cell: " + str(index_current_cell))

		# Conditions for birth and death of cell
		if condition is False:
			if self.get_number_live_neighbours() == 3:
				return "birth"
			else:
				return "keep_dead"
		else:
			if self.get_number_live_neighbours() < 2 or \
							self.get_number_live_neighbours() > 3:
				return "death"
			else:
				return "keep_alive"


# print("Debug", conversion(0,3))
# print("Debug", re_conversion(10))

class World:
	def __init__(self, edge_len):
		self.edge_len = edge_len
		self.nb_live_cells = 0
		self.time = 0
		self.nb_cells = self.edge_len ** 2
		self.list_cells = []

	def creating_grid(self):
		for y in range(self.edge_len):
			for x in range(self.edge_len):
					self.list_cells.append(Cell(x, y, False, self))
		# for c in self.list_cells:
		# print(str(c.x)+str(c.y) + " index number " +
		# str(self.conversion(c.x, c.y)))
		return self.list_cells

	#conversion from x,y coordinates to index
	def conversion(self, x, y):
		x = x
		y = int(y * self.edge_len)
		index = x + y
		return index

		# conversion from index number back to x,y co-ordinates:
	def re_conversion(self, index):
		y = int(index / self.edge_len)
		if y == 0:
			x = index
		else:
			x = int(index - (self.edge_len * y))
		if index in range(len(self.list_cells)):
			return x, y
		else:
			return False

	def is_cell_alive(self, coord_x, coord_y):
		index = self.conversion(coord_x, coord_y)
		if index in range(len(self.list_cells)):
			if self.list_cells[index].status is True:
				return True
			else:
				return False
		else:
			return False

	#stampa i messaggi non necessari
	def tick(self):
		self.time += 1
		query_status = []
		for stat in self.list_cells:
			# Stores all conditions of cells in list
			query_status.append(stat.get_next_status())
		# print(query_status)
		for index in range(len(query_status)):
			# Check for birth and death to update cell
			stat_check = query_status[index]
			if stat_check == "birth":
				print("At time " + str(self.time) + ":" + " Birth at cell: "
										+ str(self.re_conversion(index)))
				self.list_cells[index].birth()
			elif stat_check == "death":
				print("At time " + str(self.time) + ":" + " Death at cell: "
										+ str(self.re_conversion(index)))
				self.list_cells[index].death()

		self.nb_live_cells = 0
		for stat_of_cell in self.list_cells:
			if stat_of_cell.status is True:
				self.nb_live_cells += 1
		print("Number live cells cur generation = " + str(self.nb_live_cells))

	def switch_on(self, x_coord, y_coord):
		index_value = self.conversion(x_coord, y_coord)
		if index_value in range(len(self.list_cells)):
			self.list_cells[index_value].birth()
			self.nb_live_cells += 1
		else:
			return False

	def display_cells(self):
		for i in range(len(self.list_cells)):
			print("cell #" + str(i+1) + ": " + str(self.list_cells[i]))

world1 = World(20)
world1.creating_grid()

for i in range(int((world1.edge_len**2) / 2)):
	world1.switch_on(random.randint(0, world1.edge_len), random.randint(0, world1.edge_len))

while world1.time < 1000:
	world1.tick()
	scr.update()
scr.mainloop()
