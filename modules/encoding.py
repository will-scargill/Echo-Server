import json
import base64

from modules import aes

def DecodePlain(byteData):
	jsonData = byteData.decode('utf-8')
	dictData = json.loads(jsonData)
	return dictData

def EncodePlain(dictData):
	jsonData = json.dumps(dictData)
	byteData = jsonData.encode('utf-8')
	return byteData

def EncodeEncrypted(ciphertext, iv):
	jsonData = json.dumps([ciphertext, iv])
	byteData = jsonData.encode('utf-8')
	return byteData

def DecodeEncrypted(encryptedData, key):
	jsonEncrypted = encryptedData.decode('utf-8')
	listEncrypted = json.loads(jsonEncrypted)
	jsonData = aes.Decrypt(listEncrypted[0], key, listEncrypted[1])
	dictData = json.loads(jsonData)
	return dictData

def reformatData(data):
	for i in range(len(data)):
		data[i] = list(data[i])
	return data