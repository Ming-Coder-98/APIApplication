from cryptography.hazmat.primitives.ciphers.base import CipherContext
from requests.models import Response
from EncryptAndDecryptFunction import *
from HttpRequestFunction import *


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
    pprintJsonFormat(plainText)
    
    #Remove the enrolment Ref Number in config.json
    json_load = json.loads(plainText.decode())
    if (json_load["status"] < 400):
        print("Successfully Cancel Enrolment")
        saveEnrolmentId("","")


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


enrollmentInitialization()
#addEnrolment()
#resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/224565")\
# resp = getHttpRequest("https://uat-api.ssg-wsg.sg/trainingproviders/201003953Z/courses")
# print(resp.text)
#cancelEnrolment("ENR-2106-000284")
