from EncryptAndDecryptFunction import *
from HttpRequestFunction import *
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

    # response = resp.text()
    # response['uen'] = str(uen)
    # response['runId'] = str(runId)
    # response['courseReferenceNumber'] = str(courseReferenceNumber)
    # print(response)
    # saveSesIdDetails(response)

retrieveSesId()


def saveSesIdDetails(resp):
    configInfo = loadFile("config.json")
    configInfo = json.loads(configInfo)
    configInfo["SesId"] = resp.json()["data"]["sessions"][0]["id"]
    saveJsonFormat(configInfo, "config.json")
print(configInfo)

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

retrieveAttendance()


