import socket
import threading
import json
from sqlalchemy import create_engine, text, or_
from logzero import logger
import time
import os
import ast
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from modules import commandParser
from modules import config
from modules import encoding
from net.sendMessage import sendMessage
from objects.models.bannedUsers import bannedUsers
from objects.models.chatHistory import chatHistory
from objects.models.chatLogs import chatLogs
from objects.models.commandLogs import commandLogs
from objects.models.pmLogs import pmLogs
from objects.models.userRoles import userRoles
from objects.models.botTokens import botTokens


class Echo():
    def __init__(self, name, ip, host, port, password, channels, motd, nums, compatibleClientVers, strictBanning):
        self.ip = ip
        self.host = host
        self.port = port
        self.name = name
        self.motd = motd
        self.password = password
        self.users = {}
        self.compatibleClientVers = compatibleClientVers
        self.strictBanning = strictBanning

        self.blacklist = []

        self.channels = {}
        for c in channels:
            self.channels[c] = []

        self.numClients = nums
        self.recvControl = True

        self.RSAPublic = None
        self.RSAPrivate = None
        self.RSAPublicToSend = None

        self.packagedData = [json.dumps(channels), motd]

        self.listenerDaemon = None

        self.dbconn = None
        self.engine = None

    def StartServer(self, clientConnectionThread):
        try:
            with open(r"configs/blacklist.txt") as f:
                bl = f.readlines()
                self.blacklist = [x.strip() for x in bl]
        except FileNotFoundError:
            logger.warning("Blacklist file not found, proceeding with empty blacklist")

        try:  # Try to read data from RSA keys to check if they exist
            fileIn = open(r"data/public.pem", "rb")
            fileIn.close()
            fileIn = open(r"data/private.pem", "rb")
            fileIn.close()
        except FileNotFoundError:  # If they don't, generate RSA keys
            logger.warning("Rsa keys not found, generating...")
            exec(open("regenerateRsaKeys.py").read())

        fileIn = open(r"data/private.pem", "rb")  # Read private key
        bytesIn = fileIn.read()
        private = RSA.import_key(bytesIn)
        fileIn.close()

        fileIn = open(r"data/public.pem", "rb")  # Read public key
        bytesIn = fileIn.read()
        public = RSA.import_key(bytesIn)
        fileIn.close()

        self.RSAPublicToSend = bytesIn.decode('utf-8')

        self.RSAPublic = PKCS1_OAEP.new(public)  # Setup public key encryption object
        self.RSAPrivate = PKCS1_OAEP.new(private)  # Setup private key encryption object

        commandParser.init()

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.ip, int(self.port)))
        logger.info("Listening on " + str(self.host) + ":" + str(self.port) + "(" + str(self.numClients) + " clients)")

        self.listenerDaemon = threading.Thread(target=Listener, args=(self, clientConnectionThread))
        self.listenerDaemon.daemon = True
        self.listenerDaemon.start()

    def initAlchemy(self):
        if not os.path.exists("data"):
            os.mkdir("data")

        dbType = os.environ.get("ECHO_DB_TYPE")
        if dbType is None or dbType == "sqlite":
            self.engine = create_engine('sqlite:///data/database.db?check_same_thread=False')
        elif dbType == "mysql":
            dbUser = os.environ.get("ECHO_MYSQL_USER")
            dbHost = os.environ.get("ECHO_MYSQL_HOST")
            dbPass = os.environ.get("ECHO_MYSQL_PASS")
            dbName = os.environ.get("ECHO_MYSQL_DB")
            self.engine = create_engine("mysql+pymysql://{0}:{1}@{2}/{3}".format(dbUser, dbPass, dbHost, dbName))

        bannedUsers.create(self.engine, checkfirst=True)
        chatHistory.create(self.engine, checkfirst=True)
        chatLogs.create(self.engine, checkfirst=True)
        commandLogs.create(self.engine, checkfirst=True)
        pmLogs.create(self.engine, checkfirst=True)
        userRoles.create(self.engine, checkfirst=True)
        botTokens.create(self.engine, checkfirst=True)

        self.dbconn = self.engine.connect()

    def StopServer(self):
        self.recvControl = False
        for k, v in self.users.items():
            sendMessage(v.conn, v.secret, "connectionTerminated", "Server is shutting down", subtype="shutdown")
        logger.info("Server Stopped")

    def AddUser(self, user):
        self.users[user.eID] = user

    def Authenticate(self, userPassword):
        if self.password is None:
            return True

        if userPassword == "":
            userPassword = None

        if userPassword == self.password:
            return True
        else:
            return False

    def AuthenticateBot(self, token):
        query = botTokens.select().where(botTokens.c.token == token)
        matchingToken = (self.dbconn.execute(query)).fetchone()

        if matchingToken is not None:
            return True
        else:
            return False

    def RegisterBot(self, bot):
        for c in self.channels.keys():
            self.channels[c].append(bot.eID)

    def ValidID(self, user):
        if user.eID in self.users:
            return False
        else:
            return True

    def ValidUsername(self, newUser):
        newUser.username = newUser.username.strip()
        for eID in self.users:
            if self.users[eID].username == newUser.username:
                return newUser.username + "_"
        potName = newUser.username
        potName = potName.lower().strip()
        blockedNames = [
            "system",
            "server",
            ""
        ]
        if potName in blockedNames:
            newUser.username = "Clown"
        return newUser.username

    def IsNotBanned(self, user):
        if self.strictBanning == "True":
            query = bannedUsers.select().where(or_(bannedUsers.c.eID == user.eID, bannedUsers.c.eID.IP == user.addr[0]))
        else:
            query = bannedUsers.select().where(bannedUsers.c.eID == user.eID)
            matchingUsers = (self.dbconn.execute(query)).fetchone()
        if matchingUsers is not None:
            return False
        else:
            return True

    def IsServerFull(self):
        if len(self.users) >= self.numClients:
            return True
        else:
            return False

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

            query = userRoles.select().where(userRoles.c.publicKey == user.publickey)
            roleData = (self.dbconn.execute(query)).fetchone()
            if roleData is None:
                return False
            roleData = ast.literal_eval(roleData[1])
            try:
                for role in roleData:
                    if "*" in roleList[role]:
                        return True
                    if commandFlag in roleList[role]:
                        return True
            except KeyError:
                logger.error("eID " + user.eID + " has an invalid role - " + role)

        return False

    def GetChannelUsers(self, channel):
        users = []
        for eID in self.channels[channel]:
            users.append(self.users[eID].username)

        return users

    def GetBasicChannelHistory(self, channel, limit):
        query = text("SELECT * FROM (SELECT * FROM chatHistory WHERE channel=:a ORDER BY realtime DESC LIMIT :b) sub ORDER BY realtime ASC")
        channelHistory = (self.dbconn.execute(query, a=channel, b=limit)).fetchall()
        return encoding.reformatData(channelHistory)

    def GetAllChannelHistory(self, channel):
        query = text("SELECT * FROM chatHistory WHERE channel=:a ORDER BY realtime ASC")
        channelHistory = (self.dbconn.execute(query, a=channel)).fetchall()
        return encoding.reformatData(channelHistory)

    def GetUserFromName(self, username):  # Returns the user object
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def IsValidCommandTarget(self, user, target):
        roleList = {}
        with open(r"configs/roles.json", "r") as roleFile:
            roleList = json.load(roleFile)

        query = userRoles.select().where(userRoles.c.publicKey == user.publickey)
        roleData = (self.dbconn.execute(query)).fetchone()
        if roleData is None:
            return False
        roleData = ast.literal_eval(roleData[1])

        query = userRoles.select().where(userRoles.c.publicKey == target.publickey)
        targetRoles = (self.dbconn.execute(query)).fetchone()
        if targetRoles is None:  # target has no roles
            return True
        targetRoles = ast.literal_eval(targetRoles[1])

        userRoleRankings = []
        for role in roleData:
            try:
                userRoleRankings.append(roleList[role][0])
            except KeyError:
                logger.error("eID " + user.eID + " has an invalid role - " + role)

        targetRoleRankings = []
        for role in targetRoles:
            try:
                targetRoleRankings.append(roleList[role][0])
            except KeyError:
                logger.error("eID " + target.eID + " has an invalid role - " + role)

        try:
            if max(targetRoleRankings) >= max(userRoleRankings):
                return False
            else:
                return True
        except ValueError:  # target has no roles
            return True

    def GetUserHeir(self, user):
        roleList = {}
        with open(r"configs/roles.json", "r") as roleFile:
            roleList = json.load(roleFile)

        query = userRoles.select().where(userRoles.c.publicKey == user.publickey)
        roleData = (self.dbconn.execute(query)).fetchone()
        roleData = ast.literal_eval(roleData[1])
        if roleData is None:
            return False

        userRoleRankings = []
        for role in roleData:
            try:
                userRoleRankings.append(roleList[role][0])
            except KeyError:
                logger.error("eID " + user.eID + " has an invalid role - " + role)
        try:
            return max(userRoleRankings)
        except ValueError:  # target has no roles
            return 0

    def ServerMessage(self, user, content):
        metadata = ["Server", "#0000FF", time.time()]

        sendMessage(user.conn, user.secret, "outboundMessage", content, metadata=metadata)

    def CheckBlacklist(self, message):
        if config.GetSetting("useBlacklist", "Blacklist") == "False":
            return True
        messageSplit = message.split()
        for word in messageSplit:
            if word.lower() in self.blacklist:
                return False
        return True


def Listener(server, clientConnectionThread):
    server.serverSocket.listen(5)
    while server.recvControl is True:
        conn, addr = server.serverSocket.accept()
        threading.Thread(target=clientConnectionThread, args=(conn, addr)).start()  # Start a new thread for the client
    server.serverSocket.shutdown(socket.SHUT_RDWR)
    server.serverSocket.close()
