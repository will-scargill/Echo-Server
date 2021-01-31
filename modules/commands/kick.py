import json
import datetime

from net.sendMessage import sendMessage
from net import disconnect

def handle(conn, addr, currentUser, server, command):
	try:
		target = command[1]
		for k, v in server.users.items():
			if target == v.username:
				sendMessage(v.conn, v.secret, "connectionTerminated", "", subtype="kick")

				print("Client " + str(v.addr) + " was kicked from the server")

				del server.users[v.eID]
				if v.channel != None:
					server.channels[v.channel].remove(v.eID)

					channelUsers = json.dumps(server.GetChannelUsers(v.channel))

					for eID in server.channels[v.channel]:
						sendMessage(server.users[eID].conn, server.users[eID].secret, "channelUpdate", channelUsers);
					
				v.connectionValid = False
				sendMessage(v.conn, v.secret, "connectionTerminated", "", subtype="kick")
				v.conn.close()

				currentDT = datetime.datetime.now()
				dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
				metadata = ["Server", "#0000FF", dt]

				sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "User " + v.username + " was kicked", metadata=metadata)	
				break			
	except IndexError:
		pass