import json
import datetime

from net.sendMessage import sendMessage
from modules.colorhash import ColorHash
from modules import logger

def handle(conn, addr, currentUser, server, data):
	if currentUser.channel == None:
		pass
	else:
		mChannel = currentUser.channel
		channelUsers = server.channels[mChannel]
		colour = ColorHash(currentUser.username)
		currentDT = datetime.datetime.now()
		dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
		metadata = [currentUser.username, colour.hex, dt]

		for eID in channelUsers:
			sendMessage(server.users[eID].conn, server.users[eID].secret, "outboundMessage", data["data"], metadata=metadata)

		logger.logChatHistory(server, currentUser, data["data"], colour.hex)