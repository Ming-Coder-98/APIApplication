import requests
import json
from HttpRequestFunction import *

baseurl = "https://uat-api.ssg-wsg.sg/courses/runs"
payload = loadFile("CourseRunPayLoad.json")

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



def addCourserun():
      #Update the latest value
      updateCourseRunPayload()

      #payload variable is obtained from CourseRunFunction.py
      response = postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs" , payload)
      saveCourseRunDetails(response)

def deleteCourserun(runId, crn, uen):
      payload = "{\"course\":{\"courseReferenceNumber\":\"" + crn + "\",\"trainingProvider\":{\"uen\":\"" + uen + "\"},\"run\":{\"action\":\"delete\"}}}"
      postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId), payload)

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

      courseRunPayload["course"]["courseReferenceNumber"]= configInfoJson["CourseRefNum"]
      courseRunPayload["course"]["trainingProvider"]["uen"] = configInfoJson["UEN"]

      saveJsonFormat(courseRunPayload, "CourseRunPayLoad.json")
      payload = loadFile("CourseRunPayLoad.json")

# addCourserun()
#Manual Delete
#payload = "{\"course\":{\"courseReferenceNumber\":\"TGS-2020000703\",\"trainingProvider\":{\"uen\":\"199900650G\"},\"run\":{\"action\":\"delete\"}}}"
#postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/224183", payload)
#deleteCourserun(runId, crn, "199900650G")

