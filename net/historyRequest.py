import json
from sqlalchemy import text
from net.sendMessage import sendMessage

from modules import encoding


def handle(conn, addr, currentUser, server, data):
	query = text("SELECT COUNT(*) FROM chatHistory WHERE channel=:a")
	numInChannel = ((server.dbconn.execute(query, a=currentUser.channel)).fetchone())[0]


	currentLoaded = 50 + (currentUser.timesRequestedHistory * 15)
	if currentLoaded >= numInChannel:
		pass
	else: # More to load
		currentUser.timesRequestedHistory += 1
		leftToLoad = numInChannel - currentLoaded 
		descLimit = 50 + (currentUser.timesRequestedHistory * 15)
		ascLimit = 15
		if leftToLoad < 15:
			ascLimit = leftToLoad
		query = text("SELECT * FROM (SELECT * FROM (SELECT * FROM chatHistory WHERE channel=:a ORDER BY realtime DESC limit :b) suba ORDER BY realtime ASC limit :c) subb ORDER BY realtime DESC")
		remainingMessages = (server.dbconn.execute(query, a=currentUser.channel, b=descLimit, c=ascLimit)).fetchall()

		sendMessage(currentUser.conn, currentUser.secret, "additionalHistory", json.dumps(encoding.reformatData(remainingMessages)))
