import requests
import json
from HttpRequestFunction import *

baseurl = "https://uat-api.ssg-wsg.sg/courses/runs"
payload = loadPayload("CourseRunPayLoad.json")

def saveContent(content, fileName):

      global demoInfo
      configInfo = loadPayload("config.json")
      configInfo = json.loads(configInfo)
      configInfo["StatusCode"] = content.status_code
      configInfo["runId"] = (((content.json())["data"])["runs"])[0]["id"]
      configInfo["UEN"] = ((json.loads(payload)["course"])["trainingProvider"])["uen"]
      configInfo["CourseRefNum"] =  ((json.loads(payload)["course"])["courseReferenceNumber"])
      configInfo["ExtCourseRefNum"] = ((json.loads(payload)["course"])["courseReferenceNumber"])
      saveJsonFormat(configInfo, fileName)


#If data exists, delete
def courseRunInitialization():
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
            postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/223947", payload)


