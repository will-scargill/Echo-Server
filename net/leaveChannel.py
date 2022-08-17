import json
from net.sendMessage import sendMessage


def handle(conn, addr, currentUser, server, data):
    if currentUser.channel is not None:
        currentUser.timesRequestedHistory = 1
        oldChannel = currentUser.channel

        currentUser.channel = None

        # Update users in old channel (if exists)
        server.channels[oldChannel].remove(currentUser.eID)

        channelUsers = json.dumps(server.GetChannelUsers(oldChannel))

        for eID in server.channels[oldChannel]:
            sendMessage(server.users[eID].conn, server.users[eID].secret, "channelUpdate", channelUsers)
    else:
        sendMessage(conn, currentUser.secret, "errorOccured", "notInChannel")
