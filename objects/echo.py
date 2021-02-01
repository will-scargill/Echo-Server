import socket
import threading
import json
import sqlite3
from sqlite3 import OperationalError
import os
import ast
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

from modules import commandParser

class Echo():
	def __init__(self, name, ip, port, password, channels, motd, nums, compatibleClientVers):
		self.ip = ip
		self.port = port
		self.name = name
		self.motd = motd
		self.password = password
		self.users = {}
		self.compatibleClientVers = compatibleClientVers

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

		commandParser.init()

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
		        "columns": "eID TEXT, roles TEXT"
		    },
		    {
		        "name": "chatLogs",
		        "columns": "eID TEXT, IP TEXT, username TEXT, channel TEXT, date TEXT, message TEXT"
		    },
		    {
		        "name": "commandLogs",
		        "columns": "eIDSender TEXT, senderIP TEXT, senderUsername TEXT, eIDTarget TEXT, targetIP TEXT, targetUsername TEXT, channel TEXT, date TEXT, command TEXT, reason TEXT"
		    },
		    {
		        "name": "pmLogs",
		        "columns": "eIDSender TEXT, senderIP TEXT, senderUsername TEXT, eIDTarget TEXT, targetIP TEXT, targetUsername TEXT, channel TEXT, date TEXT, message TEXT"
		    },
		    {
		        "name": "chatHistory",
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
		if newUser.username == "System":
			newUser.username = "Clown"
		return newUser.username

	def IsNotBanned(self, user):
		# Always returns true for now cause i havent done database, cross reference ip and eID
		return True

	def IsValidCommand(self, command):
		commandsConfig = {}
		with open(r"configs/commands.json", "r") as commandsFile:
			commandsConfig = json.load(commandsFile)

		for k, v in commandsConfig.items():
			if command == k:
				return True

	def CanUseCommand(self, user, command):
		commandsToFlags = {}
		with open(r"configs/commands.json", "r") as commandsFile:
			commandsToFlags = json.load(commandsFile)

		commandFlag = commandsToFlags[command]
		
		if commandFlag == "*":
			return True

		roleList = {}
		with open(r"configs/roles.json", "r") as roleFile:
			roleList = json.load(roleFile)

		self.cursor.execute("SELECT roles FROM userRoles WHERE eID=?",[user.eID])
		try:
			userRoles = (list(self.cursor.fetchall()))[0][0]
			userRoles = ast.literal_eval(userRoles)
		except IndexError:
			return False

		try:
			for role in userRoles:
				if "a" in roleList[role]:
					return True
				if commandFlag in roleList[role]:
					return True
		except KeyError:
			print("[Internal Error] eID " + user.eID + " has an invalid role")

		return False

	def GetChannelUsers(self, channel):
		users = []
		for eID in self.channels[channel]:
			users.append(self.users[eID].username)

		return users

	def GetBasicChannelHistory(self, channel, limit):
		self.cursor.execute("SELECT * FROM (SELECT * FROM chatHistory WHERE channel=? ORDER BY realtime DESC LIMIT ?) ORDER BY realtime ASC", [channel, limit])
		channelHistory = self.cursor.fetchall()
		return channelHistory

	def GetAllChannelHistory(self, channel):
		self.cursor.execute("SELECT * FROM chatHistory WHERE channel=? ORDER BY realtime ASC", [channel])
		channelHistory = self.cursor.fetchall()
		return channelHistory