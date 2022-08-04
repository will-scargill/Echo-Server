import json
import time
import ast

from net.sendMessage import sendMessage

def handle(conn, addr, currentUser, server, command):
	try:
		roleList = {}
		with open(r"configs/roles.json", "r") as roleFile:
			roleList = json.load(roleFile)

		userData = []
		for k, v in roleList.items():
			userData.append(k + ": " + str(v))


		metadata = ["Server", "#0000FF", time.time()]

		sendMessage(currentUser.conn, currentUser.secret, "commandData", json.dumps(userData), subtype="multiLine", metadata=metadata)
		return True
	except IndexError:
		return False

def gethelp():
    return "getroles : usage : /getroles"
