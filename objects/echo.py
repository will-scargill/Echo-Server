import socket
import threading
import json
import sqlite3
from sqlite3 import OperationalError
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

class Echo():
	def __init__(self, name, ip, port, password, channels, motd, nums):
		self.ip = ip
		self.port = port
		self.name = name
		self.motd = motd
		self.password = password
		self.users = {}

		self.channels = {}
		for c in channels:
			self.channels[c] = []

		self.numClients = nums
		self.recvControl = True

		self.RSAPublic = None
		self.RSAPrivate = None
		self.RSAPublicToSend = None

		self.packagedData = json.dumps([json.dumps(channels), motd])

		self.dbconn = None
		self.cursor = None

	def StartServer(self, clientConnectionThread):
		try: # Try to read data from RSA keys to check if they exist
		    fileIn = open(r"data/public.pem", "rb")
		    fileIn.close()
		    fileIn = open(r"data/private.pem", "rb")
		    fileIn.close()
		except: # If they don't, generate RSA keys
		    print("Rsa keys not found, generating...")
		    exec(open("regenerateRsaKeys.py").read())

		fileIn = open(r"data/private.pem", "rb") # Read private key
		bytesIn = fileIn.read()
		private = RSA.import_key(bytesIn)
		fileIn.close()

		fileIn = open(r"data/public.pem", "rb") # Read public key
		bytesIn = fileIn.read()
		public = RSA.import_key(bytesIn) 
		fileIn.close()

		self.RSAPublicToSend = bytesIn.decode('utf-8')

		self.RSAPublic = PKCS1_OAEP.new(public) # Setup public key encryption object
		self.RSAPrivate = PKCS1_OAEP.new(private) # Setup private key encryption object

		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.bind((self.ip, int(self.port)))

		print("Listening on " + str(self.ip) + ":" + str(self.port) + "(" + str(self.numClients) + " clients)")

		self.serverSocket.listen(self.numClients)
		while self.recvControl == True:
			conn, addr = self.serverSocket.accept()
			threading.Thread(target=clientConnectionThread, args=(conn,addr)).start() # Start a new thread for the client

	def initDB(self):
		if os.path.exists("data"):
			self.dbconn = sqlite3.connect(r"data/database.db", check_same_thread=False) # Connect to the database
			self.cursor = self.dbconn.cursor() # Setup sqlite cursor
		else:
			os.mkdir("data")
			self.dbconn = sqlite3.connect(r"data/database.db", check_same_thread=False) # Connect to the database
			self.cursor = self.dbconn.cursor() # Setup sqlite cursor

		tables = [
		    {
		        "name": "bannedUsers",
		        "columns": "eID TEXT, IP TEXT, dateBanned TEXT, reason TEXT"
		    },
		    {
		        "name": "userRoles",
		        "columns": "eID TEXT, flags TEXT, permLevel TEXT"
		    },
		    {
		        "name": "chatlogs",
		        "columns": "eID TEXT, IP TEXT, username TEXT, channel TEXT, date TEXT, message TEXT"
		    },
		    {
		        "name": "commandlogs",
		        "columns": "eIDSender TEXT, senderIP TEXT, senderUsername TEXT, eIDTarget TEXT, targetIP TEXT, targetUsername TEXT, channel TEXT, date TEXT, command TEXT, reason TEXT"
		    },
		    {
		        "name": "pmlogs",
		        "columns": "eIDSender TEXT, senderIP TEXT, senderUsername TEXT, eIDTarget TEXT, targetIP TEXT, targetUsername TEXT, channel TEXT, date TEXT, message TEXT"
		    },
		    {
		        "name": "chathistory",
		        "columns": "username TEXT, channel TEXT, date TEXT, message TEXT, colour TEXT, realtime INTEGER"
		    }
		]

		for table in tables: # Create database tables if they don't exist
		    self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [table["name"]])
		    data = self.cursor.fetchall()
		    if len(data) <= 0:  # If table doesn't exist
		        self.cursor.execute("CREATE TABLE " + table["name"] + " (" + table["columns"] + ")")

	def StopServer(self):
		self.recvControl = False
		print("Server Stopped")

	def AddUser(self, user):
		self.users[user.eID] = user

	def Authenticate(self, userPassword):
		if userPassword == self.password:
			return True
		else:
			return False

	def ValidID(self, user):
		if user.eID in self.users:
			return False
		else:
			return True

	def ValidUsername(self, newUser):
		for eID in self.users:
			if self.users[eID].username == newUser.username:
				return newUser.username + "_"
			else:
				return newUser.username
		return newUser.username

	def IsNotBanned(self, user):
		# Always returns true for now cause i havent done database, cross reference ip and userid
		return True

	def GetChannelUsers(self, channel):
		users = []
		for eID in self.channels[channel]:
			users.append(self.users[eID].username)

		return users

	def GetBasicChannelHistory(self, channel, limit):
		self.cursor.execute("SELECT * FROM (SELECT * FROM chathistory WHERE channel=? ORDER BY realtime DESC LIMIT ?) ORDER BY realtime ASC", [channel, limit])
		channelHistory = self.cursor.fetchall()
		return channelHistory
