import requests
import json
certPath = ('/Users/User/KeyAndCert/CorpPass/cert.pem', '/Users/User/KeyAndCert/CorpPass/key.pem')

def getHttpRequest(request_url):
      response = requests.get(request_url, cert = certPath)
      #printResponse(response)
      return response
      
def postHttpRequest(request_url, payload):
      print("Post Http Request")
      response = requests.post(request_url, data = payload,cert = certPath)
      printResponse(response)
      return response

def postHttpRequestJson(request_url, payload):
      print("Post Http Request")
      response = requests.post(request_url, json = payload,cert = certPath)
      printResponse(response)
      return response

def loadPayload(payloadFileName):
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
