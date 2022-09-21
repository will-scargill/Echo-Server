from logzero import logger
from objects.models.userRoles import userRoles


def handle(conn, addr, currentUser, server, command):
    with open(r"data/key.txt", "r+") as f:
        key = f.read()
        if key == "LOCKED":
            logger.warning("User " + currentUser.username + " successfully used the letmein command")
            logger.warning("The key has already been used. Please delete the key file if it is needed again")
            return False
        elif key == command[1]:
            query = userRoles.insert().values(
                publicKey=currentUser.publickey,
                roles='["admin"]'
            )
            server.dbconn.execute(query)
            f.seek(0)
            f.write("LOCKED")
            f.truncate()
            server.ServerMessage(currentUser, "You have been given the admin role. Key file is now locked")
            return True
        else:
            server.ServerMessage(currentUser, "Incorrect key")
            return False


def gethelp():
    return "letmein : usage : /letmein [key]"
