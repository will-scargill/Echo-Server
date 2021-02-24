import json
import datetime
import ast

from net.sendMessage import sendMessage

def handle(conn, addr, currentUser, server, command):
	try:
		userData = []
		userData.append("Username: " + currentUser.username)
		userData.append("eID: " + currentUser.eID)
		userAddr = str("IP: " + currentUser.addr[0]) + ":" + str(currentUser.addr[1])
		userData.append(userAddr)
		if currentUser.channel == None:
			userData.append("No channel")
		else:
			userData.append("Channel: " + currentUser.channel)

		server.cursor.execute("SELECT roles FROM userRoles WHERE eID=?",[currentUser.eID])
		try:
			userRoles = (list(server.cursor.fetchall()))[0][0]
			userRoles = ast.literal_eval(userRoles)
		except IndexError:
			return False

		for role in userRoles:
			userData.append("Role: " + role)

		currentDT = datetime.datetime.now()
		dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
		metadata = ["Server", "#0000FF", dt]

		sendMessage(currentUser.conn, currentUser.secret, "commandData", json.dumps(userData), subtype="multiLine", metadata=metadata)
	except IndexError:
		pass