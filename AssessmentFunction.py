import base64
import json
from EncryptAndDecryptFunction import doDecryption, doEncryption, pprintJsonFormat
from HttpRequestFunction import getHttpRequest, loadFile, postHttpRequestJson


#ASM-2106-000048

def AssessmentInit():
    print("Assessment Init")

def addAssessment():
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


# addAssessment()
#deleteAssessment()
# resp = getHttpRequest("https://uat-api.ssg-wsg.sg/tpg/assessments/details/ASM-2106-000048")
# #print(resp.text)
# plainText = doDecryption(resp.text)
# pprintJsonFormat(plainText)
