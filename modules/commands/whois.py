import json
import datetime

import json

from net.sendMessage import sendMessage

def handle(conn, addr, currentUser, server, command):
	try:
		target = command[1]
		for k, v in server.users.items():
			if target == v.username:
				userData = []
				userData.append("Username: " + v.username)
				userData.append("eID: " + v.eID)
				userAddr = str("IP: " + v.addr[0]) + ":" + str(v.addr[1])
				userData.append(userAddr)
				if v.channel == None:
					userData.append("No channel")
				else:
					userData.append("Channel: " + v.channel)

				currentDT = datetime.datetime.now()
				dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
				metadata = ["Server", "#0000FF", dt]

				sendMessage(currentUser.conn, currentUser.secret, "commandData", json.dumps(userData), subtype="multiLine", metadata=metadata)
	except IndexError:
		pass