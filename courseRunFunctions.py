from EncryptAndDecryptFunction import pprintJsonFormat
import requests
import json
from HttpRequestFunction import *


baseurl = "https://uat-api.ssg-wsg.sg/courses/runs"
payload = loadFile("CourseRunPayLoad.json")
deleteCourseRunPayLoad = ''

def saveCourseRunDetails(content):
      configInfo = loadFile("config.json")
      configInfo = json.loads(configInfo)
      configInfo["runId"] = (((content.json())["data"])["runs"])[0]["id"]
      configInfo["UEN"] = ((json.loads(payload)["course"])["trainingProvider"])["uen"]
      configInfo["CourseRefNum"] =  ((json.loads(payload)["course"])["courseReferenceNumber"])
      configInfo["ExtCourseRefNum"] = ((json.loads(payload)["course"])["courseReferenceNumber"])
      saveJsonFormat(configInfo, "config.json")



#If data exists, delete
def courseRunInitialization():

      try:
            #Load the runId saved
            tempFile = open("config.json")
            jsonTempFile = json.load(tempFile)
            runId = jsonTempFile["runId"]
            
            if (runId != ""):
                  #Call a Get HTTP to see if runId exists
                  print("Searching Course Run Id: " + str(runId))
                  resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId))
                  print(resp.status_code)
                  #Deletion
                  if (resp.status_code < 400):
                        deleteCourserun(runId, jsonTempFile["CourseRefNum"], jsonTempFile["UEN"])
                        print("Successfully delete Course Run: " + str(runId))

      except:
            print ("There is an Error reading the File - Initialization")

def getCourseRun(runId):
      resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId))
      return resp

def addCourserun():
      #Update the latest value
      updateCourseRunPayload()

      #payload variable is obtained from CourseRunFunction.py
      response = postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs" , payload)
      saveCourseRunDetails(response)

#Delete Method for deleteCourseRunPage 
def deleteCourserun(runId):
      resp = postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId), deleteCourseRunPayLoad)
      return resp

#Update the latest UEN and Course Ref Number payload according to the config file
def updateCourseRunPayload():
      global payload
      print("Update Course Run")
      #load config File
      configInfo = loadFile("config.json")
      configInfoJson = json.loads(configInfo)

      #load courseRunPayload Json File
      courseRunPayload = loadFile("CourseRunPayLoad.json")
      courseRunPayload = json.loads(courseRunPayload)

      courseRunPayload["course"]["courseReferenceNumber"]= "TGS-2020001831"
      courseRunPayload["course"]["trainingProvider"]["uen"] = configInfoJson["UEN"]

      saveJsonFormat(courseRunPayload, "CourseRunPayLoad.json")
      payload = loadFile("CourseRunPayLoad.json")

#This method is to update the courserun payload dynamically for displaying purpose in deleteCourseRunPage 
def updateEmptyDeleteCourseRunPayLoad(CRN):
      global deleteCourseRunPayLoad
      
      #Set UEN to payload
      config = loadFile("config.json")
      config = json.loads(config)
      uen = config["UEN"]

      deleteCourseRunPayLoad = "{\n    \"course\": {\n        \"courseReferenceNumber\": \"" + CRN + "\",\n        \"trainingProvider\": {\n            \"uen\": \""+ uen + "\"\n        },\n        \"run\": {\n            \"action\": \"delete\"\n        }\n    }\n}"
      return deleteCourseRunPayLoad

def getdeleteCourseRunPayLoad():
      global uen, deleteCourseRunPayLoad
      #Set UEN to payload
      config = loadFile("config.json")
      config = json.loads(config)
      uen = config["UEN"]

      deleteCourseRunPayLoad = "{\n    \"course\": {\n        \"courseReferenceNumber\": \"\",\n        \"trainingProvider\": {\n            \"uen\": \"" + uen + "\"\n        },\n        \"run\": {\n            \"action\": \"delete\"\n        }\n    }\n}"
      return deleteCourseRunPayLoad

#addCourserun()

