import json
from colorhash import ColorHash
from net.sendMessage import sendMessage


def handle(conn, addr, currentUser, server, data):
    try:
        del server.users[currentUser.eID]
        if currentUser.channel is not None:
            server.channels[currentUser.channel].remove(currentUser.eID)

        for u in server.users.items():
            sendMessage(u[1].conn, u[1].secret, "userlistUpdate", json.dumps([currentUser.username, currentUser.eID, (ColorHash(currentUser.username)).hex, "disconnected"]))

        currentUser.connectionValid = False
        conn.close()
    except KeyError:
        # Client will always send a disconnect message, even if it's already been disconnected by the server i.e. kick/ban
        pass
