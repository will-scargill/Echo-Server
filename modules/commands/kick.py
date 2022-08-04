import json
import time
import socket
from logzero import logger
from colorhash import ColorHash

from net.sendMessage import sendMessage
from net import disconnect

def handle(conn, addr, currentUser, server, command):
	try:
		target = command[1]
		if target == currentUser.username:
			return False
		else:
			kickReason = " ".join(command[2:])
			if kickReason == "":
				kickReason = "No reason given"
			for k, v in server.users.items():
				if target == v.username:
					if server.IsValidCommandTarget(currentUser, v):
						sendMessage(v.conn, v.secret, "connectionTerminated", kickReason, subtype="kick")

						logger.info("Client " + str(v.addr) + " was kicked from the server")

						disconnect.handle(v.conn, v.addr, v, server, [])

						metadata = ["Server", "#0000FF", time.time()]

						sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "User " + v.username + " was kicked", metadata=metadata)	
						return True
					else:
						metadata = ["Server", "#0000FF", time.time()]		
						sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "You cannot execute this command on that user", metadata=metadata)
						return False
			return False
	except IndexError:
		return False

def gethelp():
    return "kick : usage : /kick [user] [reason]"
