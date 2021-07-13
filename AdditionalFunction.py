import json


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
      
#Display Info In pretty-print(readable) format
def pprintJsonFormat(plain):
    json_load = json.loads(plain.decode())  
    text = json.dumps(json_load, indent = 4)
    print(text)