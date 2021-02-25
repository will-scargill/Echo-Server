import json
import sys
import datetime
from logzero import logger

from modules import dbLogger
from modules import config

from net.sendMessage import sendMessage

importedCommands = {}

def init():
	commandsConfig = {}
	with open(r"configs/commands.json", "r") as commandsFile:
		commandsConfig = json.load(commandsFile)

	for command in commandsConfig.keys():
		exec("import modules.commands.{0}".format(command))
		exec("importedCommands[command] = modules.commands.{0}.handle".format(command))

def parse(conn, addr, currentUser, server, data):
	splitCommand = data["data"].split()
	if server.IsValidCommand(splitCommand[0][1:]):
		if server.CanUseCommand(currentUser, splitCommand[0][1:]):
			logger.info("Client " + str(currentUser.addr) + " ran command " + splitCommand[0][1:])
			#exec("from modules.commands.{0} import handle as {1}Handle".format(splitCommand[0][1:],splitCommand[0][1:]))
			#exec("{0}Handle(conn, addr, currentUser, server, splitCommand)".format(splitCommand[0][1:]))
			importedCommands[splitCommand[0][1:]](conn, addr, currentUser, server, splitCommand)

			if config.GetSetting("storeCommandlogs", "Logging") == "True":
				try:
					userObj = server.GetUserFromName(splitCommand[1])
				except IndexError:
					userObj = None
				if splitCommand[0][1:] == "pm":
					dbLogger.logCommand(server, currentUser, userObj, " ".join(splitCommand[:2]))
				else:
					dbLogger.logCommand(server, currentUser, userObj, data["data"])
		else:
			currentDT = datetime.datetime.now()
			dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
			metadata = ["Server", "#0000FF", dt]
			sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "You do not have permission to perform this command", metadata=metadata)
