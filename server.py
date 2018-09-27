import socket, threading, sys, time, os

#index will be reserved for players data

class Server():
	Lock = threading.Lock()
	Player_data = {}

	Keys = {
		"0":True,
		"1":True,
		"2":True,
		"3":True,
		"4":True,
	}

	def __init__(self, host, port):

		self.host = host
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#Some machine don't agree without this
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))
		self.server.listen(5)
#		self.run()


	def run(self):

		print('Server started!')
		print("Listening on - {}:{}".format(self.host, self.port))

		while True:
			if self.has_free_key():
				
				print("Awaiting new connection")

				conn, addr = self.server.accept()
				key = self.allocate_key()
				conn.send(key.encode("utf-8"))
				
				print('Got connection from', addr)
				self.start_new_thread(conn, addr, key)

			time.sleep(.1)
		s.close()


	def has_free_key(self):
		for value in self.Keys.values():
			if value:
				return value
		return False

	def allocate_key(self):
		for key, value in self.Keys.items():
			if value:
				#key is taken, set to false
				self.Lock.acquire()
				self.Keys[key] = False
				self.Lock.release()
				print(self.Keys)
				return key

	def restore_key(self, key):
		self.Lock.acquire()

		self.Keys[key] = True
		self.Player_data.pop(key)

		self.Lock.release()


	def start_new_thread(self, conn, addr, key):
		thread = threading.Thread(target=self.on_new_client, args=(conn, addr, key) )
		thread.daemon = True	#kill thread when the main thread exits
		thread.start()
	

	def on_new_client(self, clientsocket, addr, key):
		print("Did the function even start?")
		
		while True:
			
			#exit thread if the connection is lost
			try:
				msg = clientsocket.recv(20).decode("utf-8")
			except:
				print("Connection ended abruptly")
				msg = "quit"
			#Exit if the player sends 'quit' 
			if msg == "quit":
				self.restore_key(key)
				clientsocket.shutdown(socket.SHUT_RDWR)
				clientsocket.close()
				print("Client: {} has disconnected".format(key))
				break

			self.Lock.acquire()
			self.Player_data[key] = msg
			self.Lock.release()

			#give a string representation of players
			"""['0,300,240']"""

			lst = [v for v in self.Player_data.values()]
			print(lst)
			clientsocket.send("-".join(lst).encode("utf-8"))
			#debug_msg(msg, addr, key) 
		print("Graceful exit")


	def pprint(lst):
		for x in lst:
			print(x)
		print("---\n")

	
	def debug_msg(string, addr, key):
		print("Looping Thread: {}".format(key))
		print("{}{}{}\ntype: {} len: {}".format(addr, ' >> ', msg, type(msg), len(msg)))

	


def main():
	#host, port = "192.168.0.7", 12000
	host, port = "127.0.0.1", 12000
	if len(sys.argv) > 1:
		arg1, arg2 = sys.argv[1].split(":")
		host, port = arg1, int(arg2)

	server = Server(host, port)	#returns socket object to be issued with existing connections
	server.run()

if __name__ == "__main__":
	main()