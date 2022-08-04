import json
from colorhash import ColorHash

from net.sendMessage import sendMessage


def handle(conn, addr, currentUser, server, data):
    dataToSend = server.packagedData[:]
    clientList = []
    for user in server.users.items():
        clientList.append([user[1].username, user[1].eID, user[1].channel, (ColorHash(user[1].username).hex)])
    dataToSend.append(json.dumps(clientList))
    dataToSend = json.dumps(dataToSend)
    sendMessage(conn, currentUser.secret, "serverData", dataToSend)
	
