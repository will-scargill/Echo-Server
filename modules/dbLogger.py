import sqlite3
import datetime, time
from ssl import CHANNEL_BINDING_TYPES

from colorhash import ColorHash

from objects.models.chatHistory import chatHistory
from objects.models.chatLogs import chatLogs
from objects.models.commandLogs import commandLogs
from objects.models.pmLogs import pmLogs

def logChatHistory(server, user, message, colour):
	currentDT = datetime.datetime.now()
	dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))

	query = chatHistory.insert().values(
		username = user.username,
		channel = user.channel,
		date = dt,
		message = message,
		colour = colour,
		realtime = time.time()
	)

	server.dbconn.execute(query)

def logMessage(server, user, message):
	currentDT = datetime.datetime.now()
	dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))

	query = chatLogs.insert().values(
		eID = user.eID,
		IP = str(user.addr),
		username = user.username,
		channel = user.channel,
		date = dt,
		message = message
	)

	server.dbconn.execute(query)

def logCommand(server, user, target, command, success):
	currentDT = datetime.datetime.now()
	dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))

	if target == None:
		eIDTarget = "N/A"
		targetIP = "N/A"
		targetUsername = "N/A"
	else:
		eIDTarget = target.eID
		targetIP = str(target.addr)
		targetUsername = target.username

	query = commandLogs.insert().values(
		eIDSender = user.eID,
		senderIP = str(user.addr),
		senderUsername = user.username,
		eIDTarget = eIDTarget,
		targetIP = targetIP,
		targetUsername = targetUsername,
		channel = user.channel,
		date = dt,
		command = command,
		successful = str(success)
	)

	server.dbconn.execute(query)
	

def logPM(server, user, target, message):
	currentDT = datetime.datetime.now()
	dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))

	query = pmLogs.insert().values(
		eIDSender = user.eID,
		senderIP = str(user.addr),
		senderUsername = user.username,
		eIDTarget = target.eID,
		targetIP = str(target.addr),
		targetUsername = target.username,
		channel = user.channel,
		date = dt,
		message = message
	)

	server.dbconn.execute(query)
