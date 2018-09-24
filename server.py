import socket, threading, sys, time, os

#index will be reserved for players data

class Server():
	MAX_LISTENERS = 5
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
		"""
		Args:
			host (str): The first parameter
			port (int): The second parameter

    	Attributes:
        	msg (str): Human readable string describing the exception.
        	code (int): Exception error code.
        	server (socket inst)
		"""
		self.host = host
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#Some machine don't agree without this
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))
		self.server.listen(self.MAX_LISTENERS)
#		self.run()


	def run(self):
		"""Run the server and listen to connections"""
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
		"""Checks for availible connecting places"""
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
		"""Restores client key upon disconnecting"""
		self.Lock.acquire()

		self.Keys[key] = True
		self.Player_data.pop(key)

		self.Lock.release()


	def start_new_thread(self, conn, addr, key):
		"""Create a new thread to send and receive data from client"""

		thread = threading.Thread(target=self.on_new_client, args=(conn, addr, key) )
		thread.daemon = True	#kill thread when the main thread exits
		thread.start()
	

	def on_new_client(self, clientsocket, addr, key):
		"""Handles client data transfer through sockets"""
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
			#['0,300,240']

			lst = [v for v in self.Player_data.values()]
			print(lst)
			clientsocket.send("-".join(lst).encode("utf-8"))
			#debug_msg(msg, addr, key) 
		print("Graceful exit")


#SELF MADE SETUP EXAMPLE
def main():
	#host, port = "127.0.0.1", 12000
	host, port = "136.206.10.186", 12000
	if len(sys.argv) > 1:
		arg1, arg2 = sys.argv[1].split(":")
		host, port = arg1, int(arg2)

	server = Server(host, port)	#returns socket object to be issued with existing connections
	server.run()#I could have made the server start in __init__, But I like red button privileges.

if __name__ == "__main__":
	main()