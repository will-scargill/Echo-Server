""" Permanently bans a user from the server """
import json
import time
import datetime
from logzero import logger
from net.sendMessage import sendMessage
from objects.models.bannedUsers import bannedUsers


def handle(conn, addr, currentUser, server, command):
    try:
        target = command[1]
        if target == currentUser.username:
            return False
        else:
            banReason = " ".join(command[2:])
            if banReason == "":
                banReason = "No reason given"
            for k, v in server.users.items():
                if target == v.username:
                    if server.IsNotBanned(v):
                        if server.IsValidCommandTarget(currentUser, v):
                            sendMessage(v.conn, v.secret, "connectionTerminated", banReason, subtype="kick")

                            logger.info("Client " + str(v.addr) + " was banned from the server")

                            del server.users[v.eID]
                            if v.channel is not None:
                                server.channels[v.channel].remove(v.eID)

                                channelUsers = json.dumps(server.GetChannelUsers(v.channel))

                                for eID in server.channels[v.channel]:
                                    sendMessage(server.users[eID].conn, server.users[eID].secret, "channelUpdate", json.dumps([channelUsers, v.channel, "ECHO_BANNED"]))

                            v.connectionValid = False
                            v.conn.close()

                            metadata = ["Server", "#0000FF", time.time()]

                            sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "User " + v.username + " was banned", metadata=metadata)

                            currentDT = datetime.datetime.now()
                            dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
                            query = bannedUsers.insert().values(
                                eID=v.eID,
                                IP=v.addr[0],
                                dateBanned=dt,
                                reason=banReason
                            )

                            server.dbconn.execute(query)

                            return True
                        else:
                            metadata = ["Server", "#0000FF", time.time()]
                            sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "You cannot execute this command on that user", metadata=metadata)
                            return False
                    else:
                        metadata = ["Server", "#0000FF", time.time()]
                        sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "User " + v.username + " is already banned", metadata=metadata)
                        return False
            return False
    except IndexError:
        return False


def gethelp():
    return "ban : usage : /ban [user] [reason]"
