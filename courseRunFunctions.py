import os
import requests
import json

baseurl = "https://uat-api.ssg-wsg.sg/courses/runs"
certPath = ('/Users/User/KeyAndCert/CorpPass/cert.pem', '/Users/User/KeyAndCert/CorpPass/key.pem')
payload = ''
demoInfo = {
      "StatusCode": "",
      "UEN":"",
      "CourseRefNum": "",
      "ExtCourseRefNum": "",
      "runId":""
}

#If data exists, delete
def initialization():
      print("initialization Function")

      try:
            #Load the runId saved
            tempFile = open("config.json")
            jsonTempFile = json.load(tempFile)
            runId = jsonTempFile["runId"]
            

            #Call a Get HTTP to see if runId exists
            print("Search Existing runId")
            resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId))
            
            #Deletion
            if (resp.status_code < 400):
                  print("Deletion")
                  payload = "{\"course\":{\"courseReferenceNumber\":\"TGS-2020000697\",\"trainingProvider\":{\"uen\":\"199900650G\"},\"run\":{\"action\":\"delete\"}}}"
                  postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId), payload)
      except:
            print ("There is an Error reading the File - Initialization")
            payload = "{\"course\":{\"courseReferenceNumber\":\"TGS-2020000697\",\"trainingProvider\":{\"uen\":\"199900650G\"},\"run\":{\"action\":\"delete\"}}}"
            postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/223874", payload)

def getHttpRequest(request_url):
      response = requests.get(request_url, cert = certPath)
      #printResponse(response)
      return response
      
def postHttpRequest(request_url, payload):
      print("Post Http Request")
      response = requests.post(request_url, data = payload,cert = certPath)
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

def saveContent(content, fileName):
      global demoInfo

      demoInfo["StatusCode"] = content.status_code
      demoInfo["runId"] = (((content.json())["data"])["runs"])[0]["id"]
      demoInfo["UEN"] = ((json.loads(payload)["course"])["trainingProvider"])["uen"]
      demoInfo["CourseRefNum"] =  ((json.loads(payload)["course"])["courseReferenceNumber"])
      demoInfo["ExtCourseRefNum"] = ((json.loads(payload)["course"])["courseReferenceNumber"])
      saveJsonFormat(demoInfo, fileName)
