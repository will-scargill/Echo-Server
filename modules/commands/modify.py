import json
import datetime
import ast
from logzero import logger

from net.sendMessage import sendMessage

from objects.models.userRoles import userRoles as userRolesObj

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

						query = userRolesObj.select().where(userRolesObj.c.eID == v.eID) 
						
						try:
							userRoles = (server.dbconn.execute(query)).fetchone()
							userRoles = ast.literal_eval(userRoles[1])
						except IndexError:
							query = userRolesObj.insert().values(
								eId = v.eId
							)
							server.dbconn.execute(query)
							userRoles = []

						operation = command[2]
						newRoles = command[3:]
						userHeir = server.GetUserHeir(currentUser)

						if operation == "add":
							for role in newRoles:
								try:
									if roleList[role][0] >= userHeir:
										server.ServerMessage(currentUser, "You cannot add the role - " + role)		
										return False								
									elif role in userRoles:
										server.ServerMessage(currentUser, "User already has the role - " + role)
										return False
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

						query = userRolesObj.update().where(userRolesObj.c.eID == v.eID).values(roles = json.dumps(userRoles))
						server.dbconn.execute(query)

						server.ServerMessage(currentUser, "User " + v.username + "'s roles were modified")
						server.ServerMessage(v, "Your roles were modified")
						return True							
					else:	
						server.ServerMessage(currentUser, "You cannot execute this command on that user")
						return False
			return False
	except IndexError:
		return False