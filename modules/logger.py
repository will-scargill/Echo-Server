import sqlite3
import datetime, time

from modules.colorhash import ColorHash

def logChatHistory(server, user, message, colour):
	currentDT = datetime.datetime.now()
	dt = str(currentDT.strftime("%d-%m-%Y %H:%M:%S"))
	server.cursor.execute("INSERT INTO chathistory (username, channel, date, message, colour, realtime) VALUES (?,?,?,?,?,?)",[user.username,		
		user.channel,
		dt,
		message,
		colour,
		time.time()])
	server.dbconn.commit()