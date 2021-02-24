import json
import datetime
import ast
from logzero import logger

from net.sendMessage import sendMessage
from net import disconnect

def handle(conn, addr, currentUser, server, command):
	try:
		target = command[1]
		if target == currentUser.username:
			pass
		else:
			for k, v in server.users.items():
				if target == v.username:
					server.cursor.execute("SELECT roles FROM userRoles WHERE eID=?",[v.eID])
					try:
						userRoles = (list(server.cursor.fetchall()))[0][0]
						userRoles = ast.literal_eval(userRoles)
					except IndexError:
						return False

					operation = command[2]
					newRoles = command[3:]
					if operation == "add":
						for role in newRoles:
							userRoles.append(role.lower())
					elif operation == "remove":
						for role in newRoles:
							try:
								userRoles.remove(role.lower())
							except ValueError:
								pass

					server.cursor.execute("UPDATE userRoles SET roles=? WHERE eID=?",[json.dumps(userRoles), v.eID])
					server.dbconn.commit()

					currentDT = datetime.datetime.now()
					dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
					metadata = ["Server", "#0000FF", dt]

					sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "User " + v.username + "'s roles were modified", metadata=metadata)	
					sendMessage(v.conn, v.secret, "outboundMessage", "Your roles were modified", metadata=metadata)
					break			
	except IndexError:
		pass