from cryptography.hazmat.primitives.ciphers.base import CipherContext
from EncryptAndDecryptFunction import *
from HttpRequestFunction import *

createEnrollmenturl = "https://uat-api.ssg-wsg.sg/tpg/enrolments"

#Manual Deletion
cancelPayload = "{\"enrolment\":{\"action\":\"Update\"}}"
cancelPayloadurl = "https://uat-api.ssg-wsg.sg/tpg/enrolments/details/"


def enrollmentInitialization():

    #Search 
    
    #Delete
    # cancelPayload = "{\"enrolment\":{\"action\":\"Update\"}}"
    # cancelPayloadurl = "https://uat-api.ssg-wsg.sg/tpg/enrolments/details/{refNumber}"
    # postHttpRequestJson(cancelPayloadurl, json=cancelPayload)
    

    #load config File
    configInfo = loadPayload("config.json")
    configInfoJson = json.loads(configInfo)

    #load Enrollment Json File
    enrollmentPayload = loadPayload("EnrolmentPayLoad.json")
    enrollmentPayloadJson = json.loads(enrollmentPayload)

    enrollmentPayloadJson["enrolment"]["course"]["run"]["id"] = configInfoJson["runId"]
    enrollmentPayloadJson["enrolment"]["course"]["referenceNumber"] = configInfoJson["CourseRefNum"]
    enrollmentPayloadJson["enrolment"]["trainingPartner"]["uen"] = configInfoJson["UEN"]

    saveJsonFormat(enrollmentPayloadJson, "EnrolmentPayLoad.json")


enrollmentInitialization()
enrollmentPayload = loadPayload("EnrollmentPayLoad.json")

ciptertext = doEncryption(enrollmentPayload.encode())
print(ciptertext)
response = requests.post(createEnrollmenturl, json = ciptertext.decode(), cert=certPath)
plainText = doDecryption(response.text)
pprintJsonFormat(plainText)

