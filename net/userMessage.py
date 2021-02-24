import json
import datetime

from net.sendMessage import sendMessage
from modules.colorhash import ColorHash
from modules import logger
from modules import commandParser

def handle(conn, addr, currentUser, server, data):
	if data["data"][0] == "/": # Command 
		commandParser.parse(conn, addr, currentUser, server, data)
	elif currentUser.channel == None:
		pass
	elif currentUser.isMuted == True:
		currentDT = datetime.datetime.now()
		dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
		metadata = ["Server", "#0000FF", dt]

		sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "You are muted", metadata=metadata)
	else: # Message
		mChannel = currentUser.channel
		channelUsers = server.channels[mChannel]
		colour = ColorHash(currentUser.username)
		currentDT = datetime.datetime.now()
		dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
		metadata = [currentUser.username, colour.hex, dt]

		for eID in channelUsers:
			sendMessage(server.users[eID].conn, server.users[eID].secret, "outboundMessage", data["data"], metadata=metadata)

		logger.logChatHistory(server, currentUser, data["data"], colour.hex)