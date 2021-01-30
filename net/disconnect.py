import json

from net.sendMessage import sendMessage


def handle(conn, addr, currentUser, server, data):
	del server.users[currentUser.eID]
	if currentUser.channel != None:
		server.channels[currentUser.channel].remove(currentUser.eID)

		channelUsers = json.dumps(server.GetChannelUsers(currentUser.channel))

		for eID in server.channels[currentUser.channel]:
			sendMessage(server.users[eID].conn, server.users[eID].secret, "channelUpdate", channelUsers);
			
	conn.close()

	