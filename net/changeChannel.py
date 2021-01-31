import json

from net.sendMessage import sendMessage


def handle(conn, addr, currentUser, server, data):
	if data["data"] in server.channels:
		currentUser.timesRequestedHistory = 1
		
		if currentUser.channel == None:
			firstJoin = True
		else:
			firstJoin = False
			oldChannel = currentUser.channel

		currentUser.channel = data["data"]
		server.channels[data["data"]].append(currentUser.eID)

		# Update users in old channel (if exists)
		if firstJoin == False:
			server.channels[oldChannel].remove(currentUser.eID)

			channelUsers = json.dumps(server.GetChannelUsers(oldChannel))

			for eID in server.channels[oldChannel]:
				sendMessage(server.users[eID].conn, server.users[eID].secret, "channelUpdate", channelUsers);


		# Update users in the new channel

		channelUsers = json.dumps(server.GetChannelUsers(data["data"]))

		for eID in server.channels[data["data"]]:
			sendMessage(server.users[eID].conn, server.users[eID].secret, "channelUpdate", channelUsers);

		# Send message history

		channelHistory = server.GetBasicChannelHistory(currentUser.channel, 50);
		sendMessage(currentUser.conn, currentUser.secret, "channelHistory", json.dumps(channelHistory));

	else:
		sendMessage(conn, currentUser.secret, "errorOccured", "invalidChannel")