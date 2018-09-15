import sys, socket, threading, time

live = True
max_width, max_height = 600, 480


class Circle():

	COLOUR_ASSIGN = {
		"0":(255, 0, 0),
		"1":(0, 0, 255),
		"2":(0, 255, 0),
		"3":(255, 255, 0),
		"4":(255, 165, 0)
	}
	def __init__(self, screen, x, y, key):
		

		self.screen = screen
		self.x = x
		self.y = y
		self.key = key
		self.speed = 3
		
		#preset values
		self.colour = self.COLOUR_ASSIGN[key]	#blue
		self.radius = 15
		self.thickness = 3

	def data(self):
		#Max 16 bytes can be sent via socket. Do not exceed
		return "{},{},{}".format(self.key, self.x, self.y)

	def draw_circle(self, notself=False):
		pygame.draw.circle(self.screen, self.colour, (self.x, self.y), self.radius, self.thickness)


	def draw_players(self, string):
		global screen

		string = string.split("-")
		for player in string:
			#print(player, "<<")
			player = player.split(",")
			if player == [""]:continue
			#print(player)
			key, x, y = player[0], int(player[1]), int(player[2])

			#I don't want to draw myself twice, self constants are unified
			if key != self.key:
				pygame.draw.circle(screen, self.COLOUR_ASSIGN[key], (x, y), self.radius, self.thickness)
		#print(string)

	def handle_keys(self):
		#Makes sure circle stays on screen, 10px is the border compensation
		global client
		key = pygame.key.get_pressed()
		if key[pygame.K_DOWN] and self.y < max_height - self.radius -10:
			self.y += self.speed
			if key[pygame.K_SPACE]:
				self.y += self.speed
		if key[pygame.K_UP] and self.y > 0 + self.radius + 10:
			self.y -= self.speed
			if key[pygame.K_SPACE]:
				self.y -= self.speed
	
		if key[pygame.K_LEFT] and self.x > 0 + self.radius + 10:
			self.x -= self.speed
			if key[pygame.K_SPACE]:
				self.x -= self.speed
	
		if key[pygame.K_RIGHT] and self.x < max_width - self.radius - 10:
			self.x += self.speed
			if key[pygame.K_SPACE]:
				self.x += self.speed
	
		if key[pygame.K_ESCAPE]:
			client.send("quit".encode("utf-8"))
			live = False
			pygame.quit()
			time.sleep(.5)
			sys.exit(0)


retry = True
while retry:
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(("127.0.0.1", 12000))
		key = client.recv(10).decode("utf-8")
	except:
		time.sleep(4)
		continue
	retry = not retry

import pygame
pygame.display.set_caption("Reddy Freddy")
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((max_width, max_height))

Player = Circle(screen, max_width//2, max_height//2, key)
while live:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			client.send("quit".encode("utf-8"))
			live = False
			time.sleep(.5)
			pygame.quit()
			sys.exit(0)
	

	screen.fill((0, 0, 0))	#black

	""" Commas seperate data in buffer
	key: 		1 byte
	x coords: 	3 bytes
	y coords:	3 bytes
	color:		0 bytes	<-- key determines this
	commas:		2 bytes
	-------------------
	max total	9 bytes	
	"""
	client.send(Player.data().encode("utf-8"))	#send player statistics
	data = client.recv(50).decode("utf-8")		#receive other clients player information
	#print(data)
	Player.draw_players(data)
	Player.handle_keys()
	Player.draw_circle()
	pygame.display.flip()
	clock.tick(63)
client.close()