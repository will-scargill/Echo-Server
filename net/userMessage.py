import json

from net.sendMessage import sendMessage
from modules.colorhash import ColorHash
from modules import logger

def handle(conn, addr, currentUser, server, data):
	mChannel = currentUser.channel
	channelUsers = server.channels[mChannel]
	colour = ColorHash(currentUser.username)
	datetime = "ph"
	metadata = [currentUser.username, colour.hex, datetime]

	for eID in channelUsers:
		sendMessage(server.users[eID].conn, server.users[eID].secret, "outboundMessage", data["data"], metadata=metadata)

	logger.logChatHistory(server, currentUser, data["data"], colour.hex)