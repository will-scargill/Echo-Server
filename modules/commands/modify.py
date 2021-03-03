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
			return False
		else:
			for k, v in server.users.items():
				if target == v.username:
					if server.IsValidCommandTarget(currentUser, v):
						roleList = {}
						with open(r"configs/roles.json", "r") as roleFile:
							roleList = json.load(roleFile)

						server.cursor.execute("SELECT roles FROM userRoles WHERE eID=?",[v.eID])
						try:
							userRoles = (list(server.cursor.fetchall()))[0][0]
							userRoles = ast.literal_eval(userRoles)
						except IndexError:
							server.cursor.execute("INSERT INTO userRoles (eID) values (?)",[v.eID])
							server.dbconn.commit()
							userRoles = []

						operation = command[2]
						newRoles = command[3:]
						userHeir = server.GetUserHeir(currentUser)

						if operation == "add":
							for role in newRoles:
								try:
									if roleList[role][0] >= userHeir:
										server.ServerMessage(currentUser, "You cannot add the role - " + role)										
									elif role in userRoles:
										server.ServerMessage(currentUser, "User already has the role - " + role)
									else:
										userRoles.append(role.lower())
								except KeyError:
									server.ServerMessage(currentUser, "Role '" + role + "' does not exist")
						elif operation == "remove":
							for role in newRoles:
								try:
									userRoles.remove(role.lower())
								except ValueError:
									pass

						server.cursor.execute("UPDATE userRoles SET roles=? WHERE eID=?",[json.dumps(userRoles), v.eID])
						server.dbconn.commit()

						server.ServerMessage(currentUser, "User " + v.username + "'s roles were modified")
						server.ServerMessage(v, "Your roles were modified")
						return True							
					else:	
						server.ServerMessage(currentUser, "You cannot execute this command on that user")
						return False
			return False
	except IndexError:
		return False