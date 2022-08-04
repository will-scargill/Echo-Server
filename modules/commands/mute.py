import json
import time
from logzero import logger

from net.sendMessage import sendMessage
from net import disconnect

def handle(conn, addr, currentUser, server, command):
	try:
		target = command[1]
		if target == currentUser.username:
			return False
		else:
			muteReason = " ".join(command[2:])
			for k, v in server.users.items():
				if target == v.username:
					if server.IsValidCommandTarget(currentUser, v):
						v.isMuted = True

						metadata = ["Server", "#0000FF", time.time()]

						sendMessage(v.conn, v.secret, "outboundMessage", "You have been muted", metadata=metadata)	
						sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "User " + v.username + " was muted", metadata=metadata)	

						logger.info("Client " + str(v.addr) + " was muted")
						return True
					else:
						metadata = ["Server", "#0000FF", time.time()]		
						sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "You cannot execute this command on that user", metadata=metadata)		
						return False	
			return False			
	except IndexError:
		return False

def gethelp():
    return "mute : usage : /mute [target]"
