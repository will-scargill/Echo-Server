import json
import datetime
import ast

from net.sendMessage import sendMessage

def handle(conn, addr, currentUser, server, command):
	try:
		roleList = {}
		with open(r"configs/roles.json", "r") as roleFile:
			roleList = json.load(roleFile)

		commandsConfig = {}
		with open(r"configs/commands.json", "r") as commandsFile:
			commandsConfig = json.load(commandsFile)
		
		helpData = []
		for command in commandsConfig.keys():
		    exec("import modules.commands.{0}".format(command))
		    exec("helpData.append( modules.commands.{0}.gethelp() )".format(command))

		currentDT = datetime.datetime.now()
		dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
		metadata = ["Server", "#0000FF", dt]

		sendMessage(currentUser.conn, currentUser.secret, "commandData", json.dumps(helpData), subtype="multiLine", metadata=metadata)
		return True
	except IndexError:
		return False

def gethelp():
	return "help : usage : /help"
