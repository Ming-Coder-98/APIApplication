import base64
import json
from EncryptAndDecryptFunction import doDecryption, doEncryption, pprintJsonFormat
from HttpRequestFunction import getHttpRequest, loadFile, postHttpRequestJson, saveJsonFormat

fileName = "demoConfig.json"
#ASM-2106-000048

def AssessmentInit():
    print("Assessment Init")

def addAssessment():
    updateAttendancePayload()
    addAssessmentURL = "https://uat-api.ssg-wsg.sg/tpg/assessments"
    assessmentPayload = loadFile("AssessmentPayLoad.json")
    ciptertext = doEncryption(assessmentPayload.encode())
    response = postHttpRequestJson(addAssessmentURL, ciptertext.decode())
    plainText = doDecryption(response.text)
    pprintJsonFormat(plainText)
    json_load = json.loads(plainText.decode())

    if (json_load["status"] < 400):
        print("Successfully Add Assessment")
    else:
        raise Exception

def deleteAssessment():
    deleteAssessmentURL = "https://uat-api.ssg-wsg.sg/tpg/assessments/details/ASM-2106-000048"
    payload = "{\"assessment\":{\"action\": \"void\"}}"
    cancelPayloadEncrypt = doEncryption(payload.encode())
    resp = postHttpRequestJson(deleteAssessmentURL, cancelPayloadEncrypt.decode())
    plainText = doDecryption(resp.text)
    pprintJsonFormat(plainText)

#Update the latest Session Id, UEN ,and Course Ref Number payload according to the config file
def updateAttendancePayload():
    #load config File
    configInfo = loadFile(fileName)
    configInfoJson = json.loads(configInfo)

    #load Attendance Json File
    attendancePayload = loadFile("AssessmentPayLoad.json")
    attendancePayload = json.loads(attendancePayload)

    #Update the latest value and save
    attendancePayload["assessment"]["trainingPartner"]["code"] = configInfoJson["code"]
    attendancePayload["assessment"]["course"]["referenceNumber"] = configInfoJson["CourseRefNum"]
    attendancePayload["assessment"]["trainingPartner"]["uen"] = configInfoJson["UEN"]
    attendancePayload["assessment"]["course"]["run"]["id"] = configInfoJson["runId"]
    saveJsonFormat(attendancePayload, "AssessmentPayLoad.json")


