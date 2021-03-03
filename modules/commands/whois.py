import json
import datetime
import ast

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

				server.cursor.execute("SELECT roles FROM userRoles WHERE eID=?",[v.eID])
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
				return True
		return False
	except IndexError:
		return False