import socket, time, sys, pygame
class Player():
	MAX_WIDTH = 600
	MAX_HEGIHT = 480

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


	def draw_players(self, data):
		global screen

		data = data.split("-")
		print(data)
		for player in data:
			#print(player, "<<")
			player = player.split(",")
			if player == [""]:continue
			#print(player)
			key, x, y =  player #unpacking player 

			#I don't want to draw myself twice, self constants are unified
			if key != self.key:
				pygame.draw.circle(self.screen, self.COLOUR_ASSIGN[key], (int(x), int(y)), self.radius, self.thickness)
		#print(data) <--- player data, uncomment to reveal style

	def handle_keys(self, client):
		#Makes sure circle stays on screen, 10px is the border compensation
		key = pygame.key.get_pressed()
		if key[pygame.K_DOWN] and self.y < self.MAX_HEGIHT - self.radius -10:
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
	
		if key[pygame.K_RIGHT] and self.x < self.MAX_WIDTH - self.radius - 10:
			self.x += self.speed
			if key[pygame.K_SPACE]:
				self.x += self.speed
	
		if key[pygame.K_ESCAPE]:
			client.send("quit".encode("utf-8"))
			live = False
			pygame.quit()
			time.sleep(.5)
			sys.exit(0)

def find_connection(address):

	while True:
		try:
			client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#IPV4, tcp
			client.connect(address)
			key = client.recv(10).decode("utf-8")
		except:
			time.sleep(4)
			print("Searching for host", address)
			continue
		return client, key
		#socket obj, int
		


def main():

	#host, port = "192.168.0.7", 12000
	host, port = "127.0.0.1", 12000

	client, key = find_connection((host, port))

	pygame.init()
	
	live = True
	screen = pygame.display.set_mode((Player.MAX_WIDTH, Player.MAX_HEGIHT))
	clock = pygame.time.Clock()

	player = Player(screen, Player.MAX_WIDTH//2, Player.MAX_HEGIHT//2, key)
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
		client.send(player.data().encode("utf-8"))	#send player statistics
		data = client.recv(128).decode("utf-8")		#receive other clients player information
		#print(data)
		player.draw_players(data)
		player.handle_keys(client)
		player.draw_circle()
		pygame.display.flip()
		clock.tick(63)
	client.close()

if __name__ == "__main__":
	main()