from EncryptAndDecryptFunction import *
from HttpRequestFunction import *
import requests
import json


def retrieveSesId():
    # Load the runId saved
    tempFile = open("config.json")
    jsonTempFile = json.load(tempFile)
    runId = jsonTempFile["runId"]
    uen = jsonTempFile["UEN"]
    courseReferenceNumber = jsonTempFile["CourseRefNum"]
    print(runId, uen, courseReferenceNumber)

    # Call a Get HTTP to see if runId exists
    print("Search up for Session ID")
    resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId) + "/sessions" + "?uen="+ str(uen) + "&courseReferenceNumber=" + str(courseReferenceNumber))
    print(resp.text)
    return(resp)


def saveSesIdDetails(resp):
    configInfo = loadFile("config.json")
    configInfo = json.loads(configInfo)
    configInfo["SesId"] = resp.json()["data"]["sessions"][0]["id"]
    saveJsonFormat(configInfo, "config.json")


saveSesIdDetails(retrieveSesId())

def retrieveAttendance():
    tempFile = open("config.json")
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
    tempFile = open("config.json")
    jsonTempFile = json.load(tempFile)
    runId = jsonTempFile["runId"]
    baseAttendanceURL = "https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId) + "/sessions/attendance"
    attendancePayload = loadFile("AttendancePayLoad.json")
    print(attendancePayload)
    ciptertext = doEncryption(attendancePayload.encode())
    response = postHttpRequestJson(baseAttendanceURL, ciptertext.decode())
    print(response)

    if (response.status_code < 400):
        print("Successfully uploaded Attendance")
    else:
        raise Exception

