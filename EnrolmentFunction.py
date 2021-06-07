from cryptography.hazmat.primitives.ciphers.base import CipherContext
from requests.models import Response
from EncryptAndDecryptFunction import *
from HttpRequestFunction import *

createEnrollmenturl = "https://uat-api.ssg-wsg.sg/tpg/enrolments"

#Manual Deletion
#ref Number: ENR-2106-000120
cancelPayload = "{\"enrolment\":{\"action\":\"Update\"}}"
cancelPayloadurl = "https://uat-api.ssg-wsg.sg/tpg/enrolments/details/ENR-2106-000120"


def enrollmentInitialization():
    print ("enrolment Init")
    #Search Enrolment
    tempFile = open("config.json")
    jsonTempFile = json.load(tempFile)
    enrolmentId = jsonTempFile["enrollRefNum"]

    if (enrolmentId != ""):
        searchUrl = "https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + str(enrolmentId)
        resp = getHttpRequest(searchUrl)
        # print(resp.text)

        plaintext = doDecryption(resp.text)
        # print(plaintext)

        # Delete if exists a record
        json_load = json.loads(plaintext.decode())
        if (int(json_load["status"]) < 400):
            print("There is an Enrolment record")
            cancelEnrolment(enrolmentId)

    #load config File
    configInfo = loadFile("config.json")
    configInfoJson = json.loads(configInfo)

    #load Enrollment Json File
    enrollmentPayload = loadFile("EnrolmentPayLoad.json")
    enrollmentPayloadJson = json.loads(enrollmentPayload)

    #Update the important value in enrolment payload with the latest value in config file
    #enrollmentPayloadJson["enrolment"]["course"]["run"]["id"] = configInfoJson["runId"]
    enrollmentPayloadJson["enrolment"]["course"]["run"]["id"] = 224244
    # enrollmentPayloadJson["enrolment"]["course"]["referenceNumber"] = configInfoJson["CourseRefNum"]
    enrollmentPayloadJson["enrolment"]["course"]["referenceNumber"] = "TGS-2020001831"
    enrollmentPayloadJson["enrolment"]["trainingPartner"]["uen"] = configInfoJson["UEN"]

    saveJsonFormat(enrollmentPayloadJson, "EnrolmentPayLoad.json")

def addEnrolment():

    # resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/224201")
    # print(resp.text)

    print("Add enrolment")
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
    configInfo = loadFile("config.json")
    configInfo = json.loads(configInfo)
    configInfo["enrollRefNum"] = enrolId
    configInfo["code"] = code
    saveJsonFormat(configInfo, "config.json")


enrollmentInitialization()
# resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/224244")
# print(resp.text)
#cancelEnrolment("ENR-2106-000129")


