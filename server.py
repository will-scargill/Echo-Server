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

        connectionValid = True
        validPassword = server.Authenticate(connectionRequest[1]);
        if validPassword == False:
            connInvalidReason = "Incorrect Password"
            connectionValid = False
            print("Client " + str(addr) + " used incorrect password")
        isNotBanned = server.IsNotBanned(currentUser)
        if isNotBanned == False:
            connInvalidReason = "You are banned from this server"
            connectionValid = False
            print("Client " + str(addr) + " tried to join but was banned")
        validID = server.ValidID(currentUser)
        if validID == False:
            connInvalidReason = "Invalid eID"
            connectionValid = False
            print("Client " + str(addr) + " tried to join but was already connected from the same device")
        validUsername = server.ValidUsername(currentUser)
        currentUser.username = validUsername
        
    except ConnectionResetError:
        print("Client " + str(addr) + " disconnected during handshake")
    
    if connectionValid == True:
        try:
            sendMessage(conn, userSecret, "CRAccepted", "")
            server.AddUser(currentUser)
            sendMessage(conn, userSecret, "serverData", server.packagedData)
            print("Client " + str(addr) + " completed handshake")
            while connectionValid:
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
        except ConnectionResetError:
            print("Received illegal disconnect from client " + str(addr))
            disconnect.handle(conn, addr, currentUser, server, data)
            connectionValid = False
    else:
        print("Client " + str(addr) + " failed handshake");
        sendMessage(conn, userSecret, "CRDenied", connInvalidReason)
        conn.close()       

name = config.GetSetting("name", "Server")
channels = config.GetSetting("channels", "Server")
password = config.GetSetting("password", "Server")
port = config.GetSetting("port", "Server")
clientnums = config.GetSetting("clientnum", "Server")
motd = config.GetSetting("motd", "Server")

server = echo.Echo(name, "127.0.0.1", port, password, channels, motd, clientnums)
server.initDB()
server.StartServer(ClientConnectionThread)

