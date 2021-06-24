import re
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

def addEnrolment(enrolmentPayload):
    createEnrollmenturl = "https://uat-api.ssg-wsg.sg/tpg/enrolments"

    ciptertext = doEncryption(enrolmentPayload.encode())
    response = postHttpRequestJson(createEnrollmenturl, ciptertext.decode())
    return response.text

def cancelEnrolment(enrolmentId):
    print("Cancel Enrolment")
    cancelPayloadurl = "https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + str(enrolmentId)
    cancelPayload = "{\"enrolment\":{\"action\":\"Cancel\"}}"
    
    cancelPayloadEncrypt = doEncryption(cancelPayload.encode())
    resp = postHttpRequestJson(cancelPayloadurl, cancelPayloadEncrypt.decode())
    plainText = doDecryption(resp.text)
    pprintJsonFormat(plainText)


def saveEnrolmentId(enrolId, code):
    configInfo = loadFile(fileName)
    configInfo = json.loads(configInfo)
    configInfo["enrollRefNum"] = enrolId
    configInfo["code"] = code
    saveJsonFormat(configInfo, fileName)


#This method is to update the curl text dynamically for displaying purpose in AddEnrolment Page 
def displayPostRequestEnrolment(payloadToDisplay):
      #Remove Whitespacing new line and tabs for accurate content length
    try:
        payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
    except :
        payloadToSend = payloadToDisplay
    
    req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/enrolments",headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
    text =  '{}\n{}\r\n{}\r\n\r\n{}\n{}'.format(
        '----------------Request Information----------------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        '----------------Payload Information----------------',
        payloadToDisplay,
    )
    return text
#enrollmentInitialization()
#addEnrolment()
#resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/224565")\
# resp = getHttpRequest("https://uat-api.ssg-wsg.sg/trainingproviders/201003953Z/courses")
# print(resp.text)
# cancelEnrolment("ENR-2106-000767")