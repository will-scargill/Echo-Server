import sqlite3
import datetime, time

from modules.colorhash import ColorHash

def logChatHistory(server, user, message, colour):
	currentDT = datetime.datetime.now()
	dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
	server.cursor.execute("INSERT INTO chatHistory (username, channel, date, message, colour, realtime) VALUES (?,?,?,?,?,?)",[user.username,		
		user.channel,
		dt,
		message,
		colour,
		time.time()])
	server.dbconn.commit()

def logMessage(server, user, message):
	currentDT = datetime.datetime.now()
	dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
	server.cursor.execute("INSERT INTO chatLogs (eID, IP, username, channel, date, message) VALUES (?,?,?,?,?,?)",[user.eID,		
		str(user.addr),
		user.username,
		user.channel,
		dt,
		message])
	server.dbconn.commit()

def logCommand(server, user, target, command, success):
	currentDT = datetime.datetime.now()
	dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
	
	if target == None:
		server.cursor.execute("INSERT INTO commandLogs (eIDSender, senderIP, senderUsername, eIDTarget, targetIP, targetUsername, channel, date, command, successful) VALUES (?,?,?,?,?,?,?,?,?,?)",[user.eID,		
			str(user.addr),
			user.username,
			"N/A",
			"N/A",
			"N/A",
			user.channel,
			dt,
			command,
			str(success)])
		server.dbconn.commit()
	else:
		server.cursor.execute("INSERT INTO commandLogs (eIDSender, senderIP, senderUsername, eIDTarget, targetIP, targetUsername, channel, date, command, successful) VALUES (?,?,?,?,?,?,?,?,?,?)",[user.eID,		
			str(user.addr),
			user.username,
			target.eID,
			str(target.addr),
			target.username,
			user.channel,
			dt,
			command,
			str(success)])
		server.dbconn.commit()

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

