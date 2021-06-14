import requests
import json

keyPath = ""
certPath = ""
#Preload keypath and certPath
def httpRequestInit():
      
      global keyPath, certPath
      config = loadFile("config.json")
      config = json.loads(config)
      keyPath = config["keyPath"]
      certPath = config["certPath"]

def getHttpRequest(request_url):
      httpRequestInit()
      response = requests.get(request_url, cert = (certPath,keyPath))
      #printResponse(response)
      return response
      
#payload must not be in Bytes
def postHttpRequest(request_url, payload):
      httpRequestInit()
      print("Post Http Request")
      print (certPath)
      response = requests.post(request_url, data = payload,cert = (certPath,keyPath))
      print(response.status_code)
      printResponse(response)
      print(response.status_code)
      return response

#payload must not be in Bytes
#Reminder: doEncryption Function return in Byte
#Use this if Encryption is needed
def postHttpRequestJson(request_url, payload):
      httpRequestInit()
      print("Post Http Request")
      response = requests.post(request_url, json = payload,cert =  (certPath,keyPath))
      #printResponse(response)
      return response

def loadFile(payloadFileName):
      global payload
      #This is a template to load the file
      courseRunPayload = open(payloadFileName, "r")
      payload = courseRunPayload.read()
      return payload

def saveJsonFormat(content, fileName):
      with open(fileName, 'w') as f:
            json.dump(content, f, indent=4)

def printResponse(response):
      print("Status Code: ", response.status_code)
      print(response.text)

httpRequestInit()