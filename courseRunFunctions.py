from EncryptAndDecryptFunction import pprintJsonFormat
import requests
import json
from HttpRequestFunction import *
import re

baseurl = "https://uat-api.ssg-wsg.sg/courses/runs"
deleteCourseRunPayLoad = ''

def getCourseRun(runId):
      resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId))
      return resp

#Create Method for AddCourserunPage
def createCourserun(payload):
      response = postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs" , payload)
      return response

def updateCourserun(runId, payload):
      print("update")
      response = postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId), payload)
      return response


#Delete Method for deleteCourseRunPage 
def deleteCourserun(runId):
      resp = postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId), deleteCourseRunPayLoad)
      return resp

#Update the latest UEN and Course Ref Number payload according to the config file
def updateCourseRunPayload():
      global payload
      print("Update Course Run")
      #load config File
      configInfo = loadFile(config_path)
      configInfoJson = json.loads(configInfo)

      #load courseRunPayload Json File
      courseRunPayload = loadFile("CourseRunPayLoad.json")
      courseRunPayload = json.loads(courseRunPayload)

      courseRunPayload["course"]["courseReferenceNumber"]= "TGS-2020001831"
      courseRunPayload["course"]["trainingProvider"]["uen"] = configInfoJson["UEN"]

      saveJsonFormat(courseRunPayload, "CourseRunPayLoad.json")
      payload = loadFile("CourseRunPayLoad.json")

#This method is to update the courserun payload dynamically for displaying purpose in deleteCourseRunPage 
def getDeleteCourseRunPayLoad(CRN):
      global deleteCourseRunPayLoad
      
      #Set UEN to payload
      config = loadFile(config_path)
      config = json.loads(config)
      uen = config["UEN"]

      deleteCourseRunPayLoad = "{\n    \"course\": {\n        \"courseReferenceNumber\": \"" + CRN + "\",\n        \"trainingProvider\": {\n            \"uen\": \""+ uen + "\"\n        },\n        \"run\": {\n            \"action\": \"delete\"\n        }\n    }\n}"
      return deleteCourseRunPayLoad
      
#This method is to update the curl text dynamically for displaying purpose in deleteCourseRunPage 
def curlPostRequest(text1, payloadToDisplay):
      #Remove Whitespacing new line and tabs for accurate content length
      payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/courses/runs/" + text1,headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
      text =  '{}\n{}\r\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            '----------------Payload Information----------------',
            payloadToDisplay,
      )
      return text
#This method is to update the curl text dynamically for displaying purpose in viewCourseRunPage 
def curlGetRequestViewCourseRun(text1):
      req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/courses/runs/" + text1,headers={'accept':'application/json'}).prepare()
      text =  '{}\n{}\r\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
      )
      return text

def curlGetCourseSession(runId, CRN, sessionMonth):
      #Set UEN to payload
      config = loadFile(config_path)
      config = json.loads(config)
      uen = config["UEN"]
      if CRN != "":
            CRN = "&courseReferenceNumber=" + str(CRN)
      if (sessionMonth != ""):
            sessionMonth = "&sessionMonth=" + str(sessionMonth)
      req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/courses/runs/" + runId + "/sessions?uen=" + uen + CRN +sessionMonth,headers={'accept':'application/json'}).prepare()
      text =  '{}\n{}\r\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
      )
      return text
      
def getCourseSession(runId, CRN, sessionMonth):
      #Set UEN to payload
      config = loadFile(config_path)
      config = json.loads(config)
      uen = config["UEN"]
      print("getCourseSession")
      if CRN != "":
            CRN = "&courseReferenceNumber=" + str(CRN)
      if (sessionMonth != ""):
            sessionMonth = "&sessionMonth=" + str(sessionMonth)
      resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + runId + "/sessions?uen=" + uen + CRN +sessionMonth)
      print(resp.url)
      return resp


#addCourserun()

