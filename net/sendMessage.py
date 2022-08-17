import json
from modules import encoding
from modules import aes


def chunkstring(string, length):
    return list(string[0 + i:length + i] for i in range(0, len(string), length))


def sendMessage(socket, secret, messagetype, data, subtype="", metadata=[], enc=True):
    if enc is False:
        message = {
            "userid": "0",
            "messagetype": messagetype,
            "data": data,
            "subtype": subtype,
            "metadata": json.dumps(metadata)
        }

        byteData = encoding.EncodePlain(message)
    elif enc is True:
        message = {
            "userid": "0",
            "messagetype": messagetype,
            "data": data,
            "subtype": subtype,
            "metadata": json.dumps(metadata)
        }

        byteData = encoding.EncodePlain(message)

        ciphertext, iv = aes.Encrypt(byteData, secret)
        byteData = encoding.EncodeEncrypted(ciphertext, iv)

    datalist = chunkstring(byteData, 1024)
    for d in datalist:
        socket.send(d)
