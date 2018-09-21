# Basic-multiplayer-game
Modules - Python3, pygame, multiplayer, sockets, threading, localhost

Run server.py
Run client.py, use the arrow keys to move the circle on screen.
Optionally 5 clients can connect to the server. All players are visible to eachother

client.py is easily configurable to work across LAN, match both host and ports across the 2 files.

-----------
DESCRIPTION
-----------
Crude working (hopefully on your machine) example of simple information transfer between clients on localhost with a
yet again crude python server.

This does nothing other than allowing the movement of the circle on screen via arrow keys and viewing other connected clients.

Current design flaws:

-Client crashes if server crashes

-Server design can only handle up to 4 clients. (Intended to be 5)

(WARNING. Some issues with connecting 5 clients to a server. Reason yet unknown)
