from HttpRequestFunction import loadFile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from base64 import b64decode, b64encode
import json


configInfo = loadFile("config.json")
configInfoJson = json.loads(configInfo)


certPath = (configInfoJson["certPath"],configInfoJson["keyPath"])
backend = default_backend()
padder = padding.PKCS7(128).padder()
unpadder = padding.PKCS7(128).unpadder()
key = any
iv = (configInfoJson["IV"]).encode()


#encryption Function
def doEncryption(payloadByte):
    global key, certPath
    #preConfiguration
    certPath = (configInfoJson["certPath"],configInfoJson["keyPath"])
    key = b64decode(configInfoJson["key"])
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    padder = padding.PKCS7(128).padder()
    
    encryptor = cipher.encryptor()
    payloadToSend = padder.update(payloadByte) + padder.finalize()
    ct = encryptor.update(payloadToSend) + encryptor.finalize()
    ct_out = b64encode(ct)
    return ct_out

# #decryption
def doDecryption(response):
    global key, certPath
    #preConfiguration
    certPath = (configInfoJson["certPath"],configInfoJson["keyPath"])
    key = b64decode(configInfoJson["key"])
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    unpadder = padding.PKCS7(128).unpadder()

    result = b64decode(response)
    decryptor = cipher.decryptor()
    plain = decryptor.update(result) + decryptor.finalize()
    plain = unpadder.update(plain) + unpadder.finalize()
    return plain

#Display Info In pretty-print(readable) format
def pprintJsonFormat(plain):
    json_load = json.loads(plain.decode())  
    text = json.dumps(json_load, indent = 4)
    print(text)
