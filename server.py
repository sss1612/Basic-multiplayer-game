import socket, threading, sys, time, os

lock = threading.Lock()
#index will be reserved for players data
players = ["" for x in range(5)]
#NAFU
taken = {
	0:False,
	1:False,
	2:False,
	3:False,
	4:False

}

def pprint(lst):
	for x in lst:
		print(x)
	print("---\n")

def debug_msg(string, addr, key):
	print("Looping Thread: {}".format(key))
	print("{}{}{}\ntype: {} len: {}".format(addr, ' >> ', msg, type(msg), len(msg)))

def clear_namespace(key):
	global lock, players
	lock.acquire()
	players[key] = ""
	lock.release()


def on_new_client(clientsocket, addr, key):
	print("Did the function even start?")
	global players
	
	while True:
		
		#exit thread if the connection is lost
		try:
			msg = clientsocket.recv(20).decode("utf-8")
		except:
			msg = "quit"
		#Exit if the player sends 'quit' 
		if msg == "quit":
			clear_namespace(key)
			clientsocket.close()
			return
		lock.acquire()
		players[key] = msg
		lock.release()

		#give a string representation of players
		clientsocket.send("-".join(players).encode("utf-8"))
		#debug_msg(msg, addr, key) 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 12000


s.bind((host, port))
s.listen(5)
print('Server started!')

#Identifies each player in the game
key = 0
while True:

	if key < 4:
		print("Awaiting new connection")
		c, addr = s.accept()
		time.sleep(.1)
		c.send( str(key).encode("utf-8"))
		print('Got connection from', addr)
		try:
			t = threading.Thread(target=on_new_client, args=(c, addr, key) )
		except:
			print("A connection was closed")
		key += 1
		t.daemon = True	#kill thread when the main thread exits
		t.start()
	#os.system("cls")
	#pprint(players)
s.close()