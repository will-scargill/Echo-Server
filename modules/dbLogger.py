import sqlite3
import datetime, time

from colorhash import ColorHash

from objects.models.chatHistory import chatHistory
from objects.models.chatLogs import chatLogs
from objects.models.commandLogs import commandLogs

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
	server.cursor.execute("INSERT INTO pmLogs (eIDSender, senderIP, senderUsername, eIDTarget, targetIP, targetUsername, channel, date, message) VALUES (?,?,?,?,?,?,?,?,?)",[user.eID,		
		str(user.addr),
		user.username,
		target.eID,
		str(target.addr),
		target.username,
		user.channel,
		dt,
		message])
	server.dbconn.commit()

