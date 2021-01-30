from Crypto.PublicKey import RSA

print("Generating RSA keys...")

key = RSA.generate(4096)

print("Keys generated, exporting...")

pr = key.export_key()
fileOut = open("data/private.pem", "wb")
fileOut.write(pr)
fileOut.close()

print("Exported RSA private key")

pu = key.publickey().export_key()
fileOut = open("data/public.pem", "wb")
fileOut.write(pu)
fileOut.close()

print("Exported RSA public key")
