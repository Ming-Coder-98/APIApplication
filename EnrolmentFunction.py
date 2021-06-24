import json

from cryptography.hazmat.primitives.ciphers.base import CipherContext
from requests.models import Response
from EncryptAndDecryptFunction import *
from HttpRequestFunction import *
import re


fileName = "demoConfig.json"

def enrollmentInitialization():
    print ("enrolment Init")
    #Search Enrolment
    tempFile = open(fileName)
    jsonTempFile = json.load(tempFile)
    enrolmentId = jsonTempFile["enrollRefNum"]

    if (enrolmentId != ""):
        searchUrl = "https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + str(enrolmentId)
        resp = getHttpRequest(searchUrl)
        plaintext = doDecryption(resp.text)

        # Delete if exists a record
        json_load = json.loads(plaintext.decode())
        if (int(json_load["status"]) < 400):
            print("There is an Enrolment record")
            cancelEnrolment(enrolmentId)

def addEnrolment():
    updateEnrolmentPayload()
    createEnrollmenturl = "https://uat-api.ssg-wsg.sg/tpg/enrolments"

    enrollmentPayload = loadFile("EnrolmentPayLoad.json")
    ciptertext = doEncryption(enrollmentPayload.encode())
    response = postHttpRequestJson(createEnrollmenturl, ciptertext.decode())
    plainText = doDecryption(response.text)
    pprintJsonFormat(plainText)
    json_load = json.loads(plainText.decode())
    
    #Update the enrolment Ref Number in config.json
    if (json_load["status"] < 400):
        print("Successfully Add Enrolment")
        saveEnrolmentId(json_load["data"]["enrolment"]["referenceNumber"], json.loads(enrollmentPayload)["enrolment"]["trainingPartner"]["code"])
    else:
        raise Exception

def cancelEnrolment(enrolmentId):
    print("Cancel Enrolment")
    cancelPayloadurl = "https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + str(enrolmentId)
    cancelPayload = "{\"enrolment\":{\"action\":\"Cancel\"}}"
    
    cancelPayloadEncrypt = doEncryption(cancelPayload.encode())
    resp = postHttpRequestJson(cancelPayloadurl, cancelPayloadEncrypt.decode())
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent=4)
    return text


#This method is to update the curl text dynamically for displaying purpose in deleteEnrolmentPage
def curlPostRequest(text1, payloadToDisplay):
      #Remove Whitespacing new line and tabs for accurate content length
      payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + text1,headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
      text =  '{}\n{}\r\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            '----------------Payload Information----------------',
            payloadToDisplay,
      )
      return text


# This method is to update the courserun payload dynamically for displaying purpose in deleteCourseRunPage
def getDeleteEnrolmentPayLoad():
    global deleteEnrolmentPayLoad

    deleteEnrolmentPayLoad = "{\n    \"enrolment\": {\n        \"action\": \"" + "Cancel" + "\"\n    }   \n}"
    return deleteEnrolmentPayLoad



def saveEnrolmentId(enrolId, code):
    configInfo = loadFile(fileName)
    configInfo = json.loads(configInfo)
    configInfo["enrollRefNum"] = enrolId
    configInfo["code"] = code
    saveJsonFormat(configInfo, fileName)

#Update the latest Run Id, UEN ,and Course Ref Number payload according to the config file
def updateEnrolmentPayload():
    #load config File
    configInfo = loadFile(fileName)
    configInfoJson = json.loads(configInfo)

    #load Enrollment Json File
    enrollmentPayload = loadFile("EnrolmentPayLoad.json")
    enrollmentPayloadJson = json.loads(enrollmentPayload)

    enrollmentPayloadJson["enrolment"]["course"]["run"]["id"] = configInfoJson["runId"]
    enrollmentPayloadJson["enrolment"]["course"]["referenceNumber"] = configInfoJson["CourseRefNum"]
    enrollmentPayloadJson["enrolment"]["trainingPartner"]["uen"] = configInfoJson["UEN"]
    saveJsonFormat(enrollmentPayloadJson, "EnrolmentPayLoad.json")


def getEnrolment(enrolmentRefNo):
    resp = getHttpRequest("https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + str(enrolmentRefNo))
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text


#This method is to update the curl text dynamically for displaying purpose in viewEnrolmentPage
def curlGetRequestViewEnrolment(text1):
      req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + text1,headers={'accept':'application/json'}).prepare()
      text =  '{}\n{}\r\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
      )
      return text


#enrollmentInitialization()
#addEnrolment()
#resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/224565")\
# resp = getHttpRequest("https://uat-api.ssg-wsg.sg/trainingproviders/201003953Z/courses")
# print(resp.text)
#cancelEnrolment("ENR-2106-000284")
