import json
import datetime
from logzero import logger

from net.sendMessage import sendMessage
from net import disconnect

def handle(conn, addr, currentUser, server, command):
	try:
		target = command[1]
		if target == currentUser.username:
			pass
		else:
			muteReason = " ".join(command[2:])
			for k, v in server.users.items():
				if target == v.username:
					v.isMuted = True

					currentDT = datetime.datetime.now()
					dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
					metadata = ["Server", "#0000FF", dt]

					sendMessage(v.conn, v.secret, "outboundMessage", "You have been muted", metadata=metadata)	
					sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "User " + v.username + " was muted", metadata=metadata)	

					logger.info("Client " + str(v.addr) + " was muted")
					
					break			
	except IndexError:
		pass