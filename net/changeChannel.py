import json

from net.sendMessage import sendMessage


def handle(conn, addr, currentUser, server, data):
	if data["data"] in server.channels:
		currentUser.timesRequestedHistory = 1
	
		oldChannel = None
		if currentUser.channel == None:
			firstJoin = True
		else:
			firstJoin = False
			oldChannel = currentUser.channel
		
		currentUser.channel = data["data"]
		server.channels[data["data"]].append(currentUser.eID)

		# Update old channel data
		if firstJoin == False:
			server.channels[oldChannel].remove(currentUser.eID)

		# Update users in the new channel

		channelUpdate = [currentUser.username, oldChannel, data["data"]]
		
		for user in server.users.items():
			sendMessage(user[1].conn, user[1].secret, "channelUpdate", json.dumps(channelUpdate))

		# Send message history

		channelHistory = server.GetBasicChannelHistory(currentUser.channel, 50);
		sendMessage(currentUser.conn, currentUser.secret, "channelHistory", json.dumps(channelHistory))

	else:
		sendMessage(conn, currentUser.secret, "errorOccured", "invalidChannel")
