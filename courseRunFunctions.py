import requests
import json
from HttpRequestFunction import *

baseurl = "https://uat-api.ssg-wsg.sg/courses/runs"
payload = loadFile("CourseRunPayLoad.json")

def saveCourseRunDetails(content):
      configInfo = loadFile("config.json")
      configInfo = json.loads(configInfo)
      configInfo["StatusCode"] = content.status_code
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
            # payload = "{\"course\":{\"courseReferenceNumber\":\"TGS-2020000697\",\"trainingProvider\":{\"uen\":\"199900650G\"},\"run\":{\"action\":\"delete\"}}}"
            # postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/223999", payload)



def addCourserun():

      #payload variable is obtained from CourseRunFunction.py
      response = postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs" , payload)
      saveCourseRunDetails(response)

def deleteCourserun(runId, crn, uen):
      payload = "{\"course\":{\"courseReferenceNumber\":\"" + crn + "\",\"trainingProvider\":{\"uen\":\"" + uen + "\"},\"run\":{\"action\":\"delete\"}}}"
      postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId), payload)


#Manual Delete
#payload = "{\"course\":{\"courseReferenceNumber\":\"TGS-2020000703\",\"trainingProvider\":{\"uen\":\"199900650G\"},\"run\":{\"action\":\"delete\"}}}"
#postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/224183", payload)
#deleteCourserun(runId, crn, "199900650G")