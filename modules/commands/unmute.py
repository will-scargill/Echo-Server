import json
import datetime
from logzero import logger

from net.sendMessage import sendMessage
from net import disconnect

def handle(conn, addr, currentUser, server, command):
	try:
		target = command[1]
		if target == currentUser.username:
			return False
		else:
			unmuteReason = " ".join(command[2:])
			for k, v in server.users.items():
				if target == v.username:
					if server.IsValidCommandTarget(currentUser, v):
						v.isMuted = False

						currentDT = datetime.datetime.now()
						dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
						metadata = ["Server", "#0000FF", dt]

						sendMessage(v.conn, v.secret, "outboundMessage", "You have been unmuted", metadata=metadata)	
						sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "User " + v.username + " was unmuted", metadata=metadata)	

						logger.info("Client " + str(v.addr) + " was muted")
						return True
					else:
						currentDT = datetime.datetime.now()
						dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
						metadata = ["Server", "#0000FF", dt]		
						sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "You cannot execute this command on that user", metadata=metadata)		
						return False	
			return False			
	except IndexError:
		return False

def gethelp():
    return "unmute : usage : /unmute [target]"
