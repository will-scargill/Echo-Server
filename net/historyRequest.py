import json

from net.sendMessage import sendMessage


def handle(conn, addr, currentUser, server, data):
	server.cursor.execute("SELECT COUNT(*) FROM chatHistory WHERE channel=?",[currentUser.channel])
	numInChannel = (server.cursor.fetchall())[0][0]
	currentLoaded = currentUser.timesRequestedHistory * 50
	if currentLoaded >= numInChannel:
		pass
	else: # More to load
		currentUser.timesRequestedHistory += 1
		leftToLoad = numInChannel - currentLoaded 
		if leftToLoad < 50:
			descLimit = currentUser.timesRequestedHistory * 50
			ascLimit = (currentUser.timesRequestedHistory - 1) * 50
			server.cursor.execute("SELECT * FROM (SELECT * FROM (SELECT * FROM chatHistory WHERE channel=? ORDER BY realtime DESC limit ?) ORDER BY realtime ASC limit ?) ORDER BY realtime DESC",[currentUser.channel, descLimit, leftToLoad]) 
			remainingMessages = server.cursor.fetchall()
		else:
			descLimit = currentUser.timesRequestedHistory * 50
			ascLimit = (currentUser.timesRequestedHistory - 1) * 50
			server.cursor.execute("SELECT * FROM (SELECT * FROM (SELECT * FROM chatHistory WHERE channel=? ORDER BY realtime DESC limit ?) ORDER BY realtime ASC limit ?) ORDER BY realtime DESC",[currentUser.channel, descLimit, ascLimit]) 
			remainingMessages = server.cursor.fetchall()

		sendMessage(currentUser.conn, currentUser.secret, "additionalHistory", json.dumps(remainingMessages))
