import json
import time
import ast
from net.sendMessage import sendMessage
from objects.models.userRoles import userRoles


def handle(conn, addr, currentUser, server, command):
    try:
        userData = []
        userData.append("Username: " + currentUser.username)
        userData.append("eID: " + currentUser.eID)
        userAddr = str("IP: " + currentUser.addr[0]) + ":" + str(currentUser.addr[1])
        userData.append(userAddr)
        if currentUser.channel is None:
            userData.append("No channel")
        else:
            userData.append("Channel: " + currentUser.channel)

        query = userRoles.select().where(userRoles.c.eID == currentUser.eID)
        roleData = (server.dbconn.execute(query)).fetchone()
        if roleData is None:
            pass
        else:
            roleData = ast.literal_eval(roleData[1])
            for role in roleData:
                userData.append("Role: " + role)

        metadata = ["Server", "#0000FF", time.time()]

        sendMessage(currentUser.conn, currentUser.secret, "commandData", json.dumps(userData), subtype="multiLine", metadata=metadata)
        return True
    except IndexError:
        return False


def gethelp():
    return "self : usage : /self"
