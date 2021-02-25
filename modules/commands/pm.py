import json
import datetime

from net.sendMessage import sendMessage
from modules.colorhash import ColorHash
from modules import dbLogger
from modules import config

def handle(conn, addr, currentUser, server, command):
	try:
		target = command[1]
		pmData = command[2:]
		for k, v in server.users.items():
			if target == v.username:
				currentDT = datetime.datetime.now()
				dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
				metadata = ["[PM] " + currentUser.username, ColorHash(currentUser.username).hex, dt]

				sendMessage(currentUser.conn, currentUser.secret, "outboundMessage", " ".join(pmData), metadata=metadata)
				sendMessage(v.conn, v.secret, "outboundMessage", " ".join(pmData), metadata=metadata)

				if config.GetSetting("storePmlogs", "Logging") == "True":
					dbLogger.logPM(server, currentUser, v, " ".join(pmData))	
				break
	except IndexError:
		pass