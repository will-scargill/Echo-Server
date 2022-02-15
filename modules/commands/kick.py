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
			kickReason = " ".join(command[2:])
			if kickReason == "":
				kickReason = "No reason given"
			for k, v in server.users.items():
				if target == v.username:
					if server.IsValidCommandTarget(currentUser, v):
						sendMessage(v.conn, v.secret, "connectionTerminated", kickReason, subtype="kick")

						logger.info("Client " + str(v.addr) + " was kicked from the server")

						del server.users[v.eID]
						if v.channel != None:
							server.channels[v.channel].remove(v.eID)

							channelUsers = json.dumps(server.GetChannelUsers(v.channel))

							for eID in server.channels[v.channel]:
								sendMessage(server.users[eID].conn, server.users[eID].secret, "channelUpdate", channelUsers);
							
						v.connectionValid = False
						v.conn.close()

						currentDT = datetime.datetime.now()
						dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
						metadata = ["Server", "#0000FF", dt]

						sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "User " + v.username + " was kicked", metadata=metadata)	
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
    return "kick : usage : /kick [user] [reason]"
