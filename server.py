import socket
import threading
import json
import base64
import sqlite3
import os, sys
import datetime

from objects import echo, user
from modules import encoding
from modules import aes
from modules import config

from net.sendMessage import sendMessage
from net import changeChannel
from net import userMessage
from net import disconnect
from net import historyRequest
from net import leaveChannel

def ClientConnectionThread(conn, addr):
    try:
        print("Client connected from " + str(addr))
        
        byteData = conn.recv(1024) # Receive serverInfoRequest
        data = encoding.DecodePlain(byteData) 
        
        sendMessage(conn, "", "serverInfo", server.RSAPublicToSend, enc=False)

        byteData = conn.recv(1024) # Receive clientSecret
        data = encoding.DecodePlain(byteData)

        userSecret = server.RSAPrivate.decrypt(base64.b64decode(data["data"]))

        sendMessage(conn, userSecret, "gotSecret", "")

        byteData = conn.recv(1024) # Receive connectionRequest
        data = encoding.DecodeEncrypted(byteData, userSecret)

        connectionRequest = json.loads(data["data"])

        currentUser = user.User(data["userid"], connectionRequest[0], userSecret, addr, conn)

        currentUser.connectionValid = True
        isServerFull = server.IsServerFull()
        if isServerFull:
            connInvalidReason = "Server is full"
            currentUser.connectionValid = False
            print("Client " + str(addr) + " tried to join but the server was full")
        validPassword = server.Authenticate(connectionRequest[1]);
        if validPassword == False:
            connInvalidReason = "Incorrect Password"
            currentUser.connectionValid = False
            print("Client " + str(addr) + " used incorrect password")
        isNotBanned = server.IsNotBanned(currentUser)
        if isNotBanned == False:
            connInvalidReason = "You are banned from this server"
            currentUser.connectionValid = False
            print("Client " + str(addr) + " tried to join but was banned")
        validID = server.ValidID(currentUser)
        if validID == False:
            connInvalidReason = "Invalid eID"
            currentUser.connectionValid = False
            print("Client " + str(addr) + " tried to join but was already connected from the same device")
        if connectionRequest[2] not in server.compatibleClientVers:
            connInvalidReason = "Incompatible Client version"
            currentUser.connectionValid = False
            print("Client " + str(addr) + " tried to join but was has an incompatible client version")
        validUsername = server.ValidUsername(currentUser)
        currentUser.username = validUsername
        
    except ConnectionResetError:
        print("Client " + str(addr) + " disconnected during handshake")
    
    if currentUser.connectionValid == True:
        try:
            sendMessage(conn, userSecret, "CRAccepted", "")
            server.AddUser(currentUser)
            sendMessage(conn, userSecret, "serverData", server.packagedData)
            print("Client " + str(addr) + " completed handshake")
            while currentUser.connectionValid:
                    byteData = conn.recv(1024)
                    data = encoding.DecodeEncrypted(byteData, currentUser.secret)
                    print("Received messagetype " + data["messagetype"] + " from client " + str(addr))
                    if data["messagetype"] == "disconnect":
                        disconnect.handle(conn, addr, currentUser, server, data) 
                        break
                    elif data["messagetype"] == "userMessage":
                        userMessage.handle(conn, addr, currentUser, server, data) 
                    elif data["messagetype"] == "changeChannel":
                        changeChannel.handle(conn, addr, currentUser, server, data)
                    elif data["messagetype"] == "historyRequest":
                        historyRequest.handle(conn, addr, currentUser, server, data)
                    elif data["messagetype"] == "leaveChannel":
                        leaveChannel.handle(conn, addr, currentUser, server, data)
        except ConnectionResetError:
            print("Received illegal disconnect from client " + str(addr))
            disconnect.handle(conn, addr, currentUser, server, data)
            currentUser.connectionValid = False
        except ConnectionAbortedError as e:
            if currentUser.connectionValid == False:
                pass
            else:
                print(e)
    else:
        print("Client " + str(addr) + " failed handshake");
        sendMessage(conn, userSecret, "CRDenied", connInvalidReason)
        conn.close()

    conn.close()

name = config.GetSetting("name", "Server")
channels = config.GetSetting("channels", "Server")
password = config.GetSetting("password", "Server")
port = config.GetSetting("port", "Server")
clientnums = config.GetSetting("clientnum", "Server")
motd = config.GetSetting("motd", "Server")
compatibleClientVers = config.GetSetting("compatibleClientVers", "Server")
strictBanning = config.GetSetting("strictBanning", "Server")


server = echo.Echo(name, "127.0.0.1", port, password, channels, motd, clientnums, compatibleClientVers, strictBanning)
server.initDB()
server.StartServer(ClientConnectionThread)

