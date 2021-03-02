import json
import datetime
from logzero import logger

from net.sendMessage import sendMessage
from net import disconnect

def handle(conn, addr, currentUser, server, command):
	try:
		target = command[1]
		if target == currentUser.username:
			pass
		else:
			banReason = " ".join(command[2:])
			for k, v in server.users.items():
				if target == v.username:
					if server.IsNotBanned(v):
						if server.IsValidCommandTarget(currentUser, v):
							sendMessage(v.conn, v.secret, "connectionTerminated", banReason, subtype="kick")

							logger.info("Client " + str(v.addr) + " was banned from the server")

							del server.users[v.eID]
							if v.channel != None:
								server.channels[v.channel].remove(v.eID)

								channelUsers = json.dumps(server.GetChannelUsers(v.channel))

								for eID in server.channels[v.channel]:
									sendMessage(server.users[eID].conn, server.users[eID].secret, "channelUpdate", channelUsers);
								
							v.connectionValid = False
							v.conn.close()

							currentDT = datetime.datetime.now()
							dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
							metadata = ["Server", "#0000FF", dt]

							sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "User " + v.username + " was banned", metadata=metadata)	

							server.cursor.execute("INSERT INTO bannedUsers (eID, IP, dateBanned, reason) values (?,?,?,?)",[v.eID, v.addr[0], dt, banReason])
							server.dbconn.commit()
						else:
							currentDT = datetime.datetime.now()
							dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
							metadata = ["Server", "#0000FF", dt]		
							sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "You cannot execute this command on that user", metadata=metadata)
					else:
						sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", "User " + v.username + " is already banned", metadata=metadata)	
					break			
	except IndexError:
		pass

