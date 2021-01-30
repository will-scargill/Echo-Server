import sqlite3
import time

from modules.colorhash import ColorHash

def logChatHistory(server, user, message, colour):
	server.cursor.execute("INSERT INTO chathistory (username, channel, message, colour, realtime) VALUES (?,?,?,?,?)",[user.username,		
		user.channel,
		message,
		colour,
		time.time()])
	server.dbconn.commit()