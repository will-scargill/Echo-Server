import json
import datetime
import time

from net.sendMessage import sendMessage
from colorhash import ColorHash
from modules import config
from modules import dbLogger
from modules import commandParser


def handle(conn, addr, currentUser, server, data):
	if data["data"][0] == "/": # Command 
		commandParser.parse(conn, addr, currentUser, server, data)
	elif currentUser.channel == None:
		pass
	elif currentUser.isMuted == True:
		metadata = ["Server", "#0000FF", time.time()]

		sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "You are muted", metadata=metadata)
	else: # Message
		if server.CheckBlacklist(data["data"]):
			mChannel = currentUser.channel
			channelUsers = server.channels[mChannel]
			colour = ColorHash(currentUser.username)
			metadata = [currentUser.username, colour.hex, time.time()]

			for eID in channelUsers:
				sendMessage(server.users[eID].conn, server.users[eID].secret, "outboundMessage", data["data"], metadata=metadata)

			dbLogger.logChatHistory(server, currentUser, data["data"], colour.hex)

			if config.GetSetting("storeChatlogs", "Logging") == "True":
				dbLogger.logMessage(server, currentUser, data["data"])
		else:
			if config.GetSetting("kickOnUse", "Blacklist") == "True":
				sendMessage(currentUser.conn, currentUser.secret, "connectionTerminated", config.GetSetting("kickReason", "Blacklist"), subtype="kick")
				del server.users[currentUser.eID]
				if currentUser.channel != None:
					server.channels[currentUser.channel].remove(currentUser.eID)

					channelUsers = json.dumps(server.GetChannelUsers(currentUser.channel))

					for eID in server.channels[currentUser.channel]:
						sendMessage(server.users[eID].conn, server.users[eID].secret, "channelUpdate", channelUsers);
					
				currentUser.connectionValid = False
				currentUser.conn.close()

				logger.info("Client " + str(v.addr) + " was kicked from the server")
			else:
				server.ServerMessage(currentUser, "You used a word on the blacklist and your message was not sent.")
