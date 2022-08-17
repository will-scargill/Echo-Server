import json
import time
import ast
from net.sendMessage import sendMessage
from objects.models.userRoles import userRoles


def handle(conn, addr, currentUser, server, command):
    try:
        target = command[1]
        for k, v in server.users.items():
            if target == v.username:
                userData = []
                userData.append("Username: " + v.username)
                userData.append("eID: " + v.eID)
                userAddr = str("IP: " + v.addr[0]) + ":" + str(v.addr[1])
                userData.append(userAddr)
                if v.channel is None:
                    userData.append("No channel")
                else:
                    userData.append("Channel: " + v.channel)

                query = userRoles.select().where(userRoles.c.eID == v.eID)
                allUserRoles = (server.dbconn.execute(query)).fetchone()
                if allUserRoles is not None:
                    allUserRoles = ast.literal_eval(allUserRoles[1])
                    for role in allUserRoles:
                        userData.append("Role: " + role)

                metadata = ["Server", "#0000FF", time.time()]

                sendMessage(currentUser.conn, currentUser.secret, "commandData", json.dumps(userData), subtype="multiLine", metadata=metadata)
                return True
        return False
    except IndexError:
        return False


def gethelp():
    return "whois : usage : /whois [target]"
