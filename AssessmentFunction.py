import base64
import json

import requests
from EncryptAndDecryptFunction import doDecryption, doEncryption, pprintJsonFormat
from HttpRequestFunction import getHttpRequest, loadFile, postHttpRequestJson, saveJsonFormat

fileName = "demoConfig.json"
#ASM-2106-000048

def AssessmentInit():
    print("Assessment Init")

def addAssessment():
    updateAssessmentPayload()
    addAssessmentURL = "https://uat-api.ssg-wsg.sg/tpg/assessments"
    assessmentPayload = loadFile("AssessmentPayLoad.json")
    ciptertext = doEncryption(assessmentPayload.encode())
    response = postHttpRequestJson(addAssessmentURL, ciptertext.decode())
    plainText = doDecryption(response.text)
    pprintJsonFormat(plainText)
    json_load = json.loads(plainText.decode())

    if (json_load["status"] < 400):
        print("Successfully Add Assessment")
        saveAssessmentRefNumber(json_load["data"]["assessment"]["referenceNumber"])
    else:
        raise Exception

def deleteAssessment():
    deleteAssessmentURL = "https://uat-api.ssg-wsg.sg/tpg/assessments/details/ASM-2106-000048"
    payload = "{\"assessment\":{\"action\": \"void\"}}"
    cancelPayloadEncrypt = doEncryption(payload.encode())
    resp = postHttpRequestJson(deleteAssessmentURL, cancelPayloadEncrypt.decode())
    plainText = doDecryption(resp.text)
    pprintJsonFormat(plainText)

#Update the latest Run Id, UEN ,and Course Ref Number payload according to the config file
def updateAssessmentPayload():
    #load config File
    configInfo = loadFile(fileName)
    configInfoJson = json.loads(configInfo)

    #load Attendance Json File
    assessmentPayload = loadFile("AssessmentPayLoad.json")
    assessmentPayload = json.loads(assessmentPayload)

    #Update the latest value and save
    assessmentPayload["assessment"]["trainingPartner"]["code"] = configInfoJson["code"]
    assessmentPayload["assessment"]["course"]["referenceNumber"] = configInfoJson["CourseRefNum"]
    assessmentPayload["assessment"]["trainingPartner"]["uen"] = configInfoJson["UEN"]
    assessmentPayload["assessment"]["course"]["run"]["id"] = configInfoJson["runId"]
    saveJsonFormat(assessmentPayload, "AssessmentPayLoad.json")

def saveAssessmentRefNumber(assessmentRefNumber):
    configInfo = loadFile(fileName)
    configInfo = json.loads(configInfo)
    configInfo["AssessmentRefNum"] = assessmentRefNumber
    saveJsonFormat(configInfo, fileName)

def displayViewAssessment(crn):
    req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/tpg/assessments/details/" + crn,headers={'accept':'application/json'}).prepare()
    text =  '{}\n{}\r\n{}\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            'Decryption: Required'
      )
    return text