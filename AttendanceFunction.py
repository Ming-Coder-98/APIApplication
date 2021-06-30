import re
from EncryptAndDecryptFunction import *
from HttpRequestFunction import *
import requests
import json

fileName = "demoConfig.json"

def retrieveSesId():
    # Load the runId saved
    tempFile = open(fileName)
    jsonTempFile = json.load(tempFile)
    runId = jsonTempFile["runId"]
    uen = jsonTempFile["UEN"]
    courseReferenceNumber = jsonTempFile["CourseRefNum"]
    #print(runId, uen, courseReferenceNumber)

    # Call a Get HTTP to see if runId exists
    print("Search up for Session ID")
    resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId) + "/sessions" + "?uen="+ str(uen) + "&courseReferenceNumber=" + str(courseReferenceNumber))
    print(resp.text)
    return resp


def saveSesIdDetails(resp):
    configInfo = loadFile(fileName)
    configInfo = json.loads(configInfo)
    configInfo["SesId"] = resp.json()["data"]["sessions"][0]["id"]
    saveJsonFormat(configInfo, fileName)


def retrieveAttendance():
    tempFile = open(fileName)
    jsonTempFile = json.load(tempFile)
    runId = jsonTempFile["runId"]
    uen = jsonTempFile["UEN"]
    courseReferenceNumber = jsonTempFile["CourseRefNum"]
    sesId = jsonTempFile["SesId"]
    baseRetrieveAttendanceurl = "https://uat-api.ssg-wsg.sg/courses/runs/"
    response = getHttpRequest(baseRetrieveAttendanceurl + str(runId) + "/sessions/attendance?uen=" + str(uen) + "&courseReferenceNumber=" + str(courseReferenceNumber) + "&sessionId=" + str(sesId))
    result = doDecryption(response.text)
    pprintJsonFormat(result)


def uploadAttendance():

    saveSesIdDetails(retrieveSesId())
    updateAttendancePayload()

    tempFile = open(fileName)
    jsonTempFile = json.load(tempFile)
    runId = jsonTempFile["runId"]
    baseAttendanceURL = "https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId) + "/sessions/attendance"
    attendancePayload = loadFile("AttendancePayLoad.json")
    ciptertext = doEncryption(attendancePayload.encode())
    response = postHttpRequestJson(baseAttendanceURL, ciptertext.decode())
    print(response.text)

    if (response.status_code < 400):
        print("Successfully uploaded Attendance")
    else:
        raise Exception


#Update the latest Session Id, UEN ,and Course Ref Number payload according to the config file
def updateAttendancePayload():
    #load config File
    configInfo = loadFile(fileName)
    configInfoJson = json.loads(configInfo)

    #load Attendance Json File
    attendancePayload = loadFile("AttendancePayLoad.json")
    attendancePayload = json.loads(attendancePayload)

    #Update the latest value and save
    attendancePayload["course"]["sessionID"] = configInfoJson["SesId"]
    attendancePayload["course"]["referenceNumber"] = configInfoJson["CourseRefNum"]
    attendancePayload["uen"] = configInfoJson["UEN"]

    saveJsonFormat(attendancePayload, "AttendancePayLoad.json")

def getSessionAttendance(runId, uen, crn, sessionId):
    if uen != '':
        uen = "?uen=" + uen
    if crn != '':
        crn = "&courseReferenceNumber=" + crn
    if sessionId != '':
        sessionId = "&sessionId=" + sessionId
    resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + runId + "/sessions/attendance" + uen + crn + sessionId)
    print(resp)
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text

#This method is to update the curl text dynamically for displaying purpose in viewEnrolmentPage
def displayViewSession(runId, uen, crn, sessionId):
    if uen != '':
        uen = "?uen=" + uen
    if crn != '':
            crn = "&courseReferenceNumber=" + crn
    if sessionId != '':
        sessionId = "&sessionId=" + sessionId
    req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/courses/runs/" + runId + "/sessions/attendance" + uen + crn + sessionId,headers={'accept':'application/json'}).prepare()
    text =  '{}\n{}\r\n{}\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            'Decryption: Required'
      )
    return text

#This method is to update the curl text dynamically for displaying purpose in AddAttendancePage
def curlRequestUploadAttendance(runId, payloadToDisplay):
     # Remove Whitespacing new line and tabs for accurate content length
      payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/courses/runs/" +  str(runId) + "/sessions/attendance" ,headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
      text =  '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
          req.method + ' ' + req.url,
          '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
          'Encryption: Required\n',
          '----------------Payload Information----------------',
          payloadToDisplay,
      )
      return text


def uploadAttendanceFn(runId, attendancePayload):
    baseAttendanceURL = "https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId) + "/sessions/attendance"
    ciptertext = doEncryption(attendancePayload.encode())
    response = postHttpRequestJson(baseAttendanceURL, ciptertext.decode())
    #print(response.text)
    return response.text
