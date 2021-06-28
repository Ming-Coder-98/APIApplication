import re
import json

from cryptography.hazmat.primitives.ciphers.base import CipherContext
from requests.models import Response
from EncryptAndDecryptFunction import *
from HttpRequestFunction import *

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
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent=4)
    return text

def updateEnrolment(referenceNumber, payload):
    url = "https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + str(referenceNumber)
    payloadEncrypted = doEncryption(payload.encode())
    resp = postHttpRequestJson(url, payloadEncrypted.decode())
    return resp.text 


def getEnrolment(enrolmentRefNo):
    resp = getHttpRequest("https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + str(enrolmentRefNo))
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text


def updateEnrolmentFee(enrolmentRefNo):
    updateEnrolmentFeeURL = ("https://uat-api.ssg-wsg.sg/tpg/enrolments/feeCollections/" + str(enrolmentRefNo))

    UpdateEnrolmentFeeEncrypt = doEncryption(updateEnrolmentFeePayLoad.encode())
    resp = postHttpRequestJson(updateEnrolmentFeeURL, UpdateEnrolmentFeeEncrypt.decode())
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text


#This method is to update the curl text dynamically for displaying purpose in deleteEnrolmentPage
def curlPostRequest(text1, payloadToDisplay):
      #Remove Whitespacing new line and tabs for accurate content length
      payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + text1,headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
      text =  '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            'Encryption: Required\nDecryption: Required',
            '----------------Payload Information----------------',
            payloadToDisplay,
      )
      return text


# This method is to update the courserun payload dynamically for displaying purpose in deleteEnrolmentPage
def getDeleteEnrolmentPayLoad():
    global deleteEnrolmentPayLoad
    deleteEnrolmentPayLoad = "{\n    \"enrolment\": {\n        \"action\": \"" + "Cancel" + "\"\n    }   \n}"
    return deleteEnrolmentPayLoad


#This method is to update the curl text dynamically for displaying purpose in AddEnrolment Page 
def displayPostRequestEnrolment(refnumber, payloadToDisplay):
      #Remove Whitespacing new line and tabs for accurate content length
    try:
        payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
    except :
        payloadToSend = payloadToDisplay
    
    req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/enrolments/" + refnumber,headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
    text =  '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
        '----------------Request Information----------------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        'Encryption: Required\nDecryption: Required',
        '----------------Payload Information----------------',
        payloadToDisplay,
    )
    return text



# This method is to update the courserun payload dynamically for displaying purpose in deleteEnrolmentPage
def getUpdateEnrolmentFeePayLoad(status):
    global updateEnrolmentFeePayLoad

    updateEnrolmentFeePayLoad = "{\n    \"enrolment\": {\n        \"fees\": " + "{" + "\n          \"collectionStatus\": \"" + status + "\" \n        } \n     }   \n }"
    return updateEnrolmentFeePayLoad



#This method is to update the curl text dynamically for displaying purpose in UpdateEnrolmentFee
def curlPostRequestUpdateEnrolmentFee(text1, payloadToDisplay):
      #Remove Whitespacing new line and tabs for accurate content length
      payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/enrolments/feeCollections/" + text1,headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
      text =  '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            'Encryption: Required\nDecryption: Required',
            '----------------Payload Information----------------',
            payloadToDisplay,
      )
      return text


#This method is to update the curl text dynamically for displaying purpose in viewEnrolmentPage
def curlGetRequestViewEnrolment(text1):
      req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + text1,headers={'accept':'application/json'}).prepare()
      text =  '{}\n{}\r\n{}\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            'Decryption: Required'
      )
      return text



#enrollmentInitialization()
#addEnrolment()
#resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/224565")\
# resp = getHttpRequest("https://uat-api.ssg-wsg.sg/trainingproviders/201003953Z/courses")
# print(resp.text)
# cancelEnrolment("ENR-2106-000767")