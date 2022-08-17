import json
import time
from net.sendMessage import sendMessage


def handle(conn, addr, currentUser, server, command):
    try:
        commandsConfig = {}
        with open(r"configs/commands.json", "r") as commandsFile:
            commandsConfig = json.load(commandsFile)

        helpData = []
        for command in commandsConfig.keys():
            exec("import modules.commands.{0}".format(command))
            exec("helpData.append( modules.commands.{0}.gethelp() )".format(command))

        metadata = ["Server", "#0000FF", time.time()]

        sendMessage(currentUser.conn, currentUser.secret, "commandData", json.dumps(helpData), subtype="multiLine", metadata=metadata)
        return True
    except IndexError:
        return False


def gethelp():
    return "help : usage : /help"
