import base64
import json
import re

import requests
from EncryptAndDecryptFunction import doDecryption, doEncryption, pprintJsonFormat
from HttpRequestFunction import getHttpRequest, loadFile, postHttpRequestJson, saveJsonFormat

def deleteAssessment():
    deleteAssessmentURL = "https://uat-api.ssg-wsg.sg/tpg/assessments/details/ASM-2106-000048"
    payload = "{\"assessment\":{\"action\": \"void\"}}"
    cancelPayloadEncrypt = doEncryption(payload.encode())
    resp = postHttpRequestJson(deleteAssessmentURL, cancelPayloadEncrypt.decode())
    plainText = doDecryption(resp.text)
    pprintJsonFormat(plainText)

def getAssessment(crn):
    resp = getHttpRequest("https://uat-api.ssg-wsg.sg/tpg/assessments/details/" + crn)
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text
def displayViewAssessment(crn):
    req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/tpg/assessments/details/" + crn,headers={'accept':'application/json'}).prepare()
    text =  '{}\n{}\r\n{}\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            'Decryption: Required',
      )
    return text


#This method is to update the curl text dynamically for displaying purpose in SearchAssessmentPage
def curlRequestSearchAssessment(payloadToDisplay):
     # Remove Whitespacing new line and tabs for accurate content length
      payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/assessments/search" ,headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
      text =  '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
          req.method + ' ' + req.url,
          '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
          'Encryption: Required\nDecryption: Required',
          '----------------Payload Information----------------',
          payloadToDisplay,
      )
      return text

#This method is to update the curl text dynamically for displaying purpose in SearchAssessmentPage
def displayUpdateAssessment(refNum,payloadToDisplay):
     # Remove Whitespacing new line and tabs for accurate content length
      payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/assessments/details/" + refNum ,headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
      text =  '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
          req.method + ' ' + req.url,
          '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
          'Encryption: Required\nDecryption: Required',
          '----------------Payload Information----------------',
          payloadToDisplay,
      )
      return text



def searchAssessment(searchAssessmentPayload):
    searchAssessmentURL = ("https://uat-api.ssg-wsg.sg/tpg/assessments/search")

    searchAssessmentEncrypt = doEncryption(searchAssessmentPayload.encode())
    resp = postHttpRequestJson(searchAssessmentURL, searchAssessmentEncrypt.decode())
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text


def updateAssessment(refNum, payload):
    updateAssessmentURL = "https://uat-api.ssg-wsg.sg/tpg/assessments/details/" + refNum
    updateAssessmenEncrypt = doEncryption(payload.encode())
    resp = postHttpRequestJson(updateAssessmentURL, updateAssessmenEncrypt.decode())
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text