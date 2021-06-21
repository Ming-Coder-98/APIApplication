#Import course Run py Functions
from tkinter import scrolledtext
import tkinter

from requests.api import delete, request
from requests.sessions import session
from configWindow import getCertPemFile, setConfigWindow, showConfigWindow
from AssessmentFunction import addAssessment
from EnrolmentFunction import addEnrolment, enrollmentInitialization
from AttendanceFunction import uploadAttendance
from courseRunFunctions import createCourserun, curlPostRequest, deleteCourserun, getDeleteCourseRunPayLoad, updateCourserun
from HttpRequestFunction import getHttpRequest, loadFile, saveJsonFormat
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import json
import datetime
from PIL import ImageTk, Image
from tkinter import filedialog
import pandas as pd

from tooltip import CreateToolTip
#Load Tooltip Json object as ttDescription
with open("TooltipDescription.json") as f:
    tooltipDescription = json.load(f)

#Preview Page
class updateCourseRunPagePreview(tk.Frame):
    global contentInfo
    contentInfo = ''
    
    def refresh(controllerCurlText):
        controllerCurlText.delete("1.0","end")
        controllerCurlText.insert(tk.END, str(curlPostRequest("",updateCourseRunPagePreview.payload)))

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        label_0 = Label(self, text="Update Course Run", width=20, font=("bold", 20))
        label_0.place(x=90, y=43)

        #Course Run Id
        label_runId = Label(self, text="Course Run ID: ", width=20, font=("bold", 10), anchor='w')
        label_runId.place(x=90, y=100)

        entry_runId = Entry(self)
        entry_runId.place(x=250, y=100)
        label_1_ttp = CreateToolTip(label_runId, tooltipDescription["CourseRunId"])

        #This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing():
            contentInfo = updateCourseRunPagePreview.payload
            value = curlPostRequest(entry_runId.get(),contentInfo)
            self.curlText.delete("1.0","end")
            self.curlText.insert(tk.END, value)

        entry_runId.bind('<KeyRelease>', lambda b:typing())

        # Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        # Configuration for Notebook layout
        tabControl = ttk.Notebook(self)

        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)

        # Adding of tabs
        tabControl.add(tab2, text='Request')
        tabControl.add(tab3, text='Reponse')
        tabControl.place(width=440, height=460, x=30, y=222)

        self.payload = loadFile("EmptyUpdateCourseRunPayLoad.json")
        self.curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        self.curlText.insert(tk.END,  str(curlPostRequest("","")))
        self.curlText.place(height=405, width=440, y=20)
        self.curlText.bind("<Key>", lambda e: "break")

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        # responseText.bind("<Key>", lambda e: "break")

        def submitCallBack():
            print("Do Nothing")
            
        submitButton = tk.Button(self, text="Update", bg="white", width=25, pady=5, command=lambda: submitCallBack())
        submitButton.place(relx=0.5, rely=0.25, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(updateCourseRunPagePage3),
                               )
        backButton.place(relx=0.055, rely=0.021, anchor=CENTER)
        # exportButton1 = tk.Button(self, text="Export Payload", bg="white", width=15, pady=5, command = lambda: downloadFile("payload"))
        # exportButton1.place(relx=0.3, rely=0.95, anchor=CENTER)
        # exportButton2 = tk.Button(self, text="Export Response", bg="white", width=15, pady=5,command = lambda: downloadFile("response"))
        # exportButton2.place(relx=0.7, rely=0.95, anchor=CENTER)

        # adding of single line text box
        edit = Entry(self, background="light gray")

        # positioning of text box
        edit.place(x=285, height=21, y=244)

        # setting focus
        edit.focus_set()

        butt_resp = Button(tab2, text='Find', command=lambda: find("curl"), highlightthickness=0, bd=0,
                           background="gray")
        butt_resp.place(x=380, y=0, height=21, width=60)
        butt_resp = Button(tab3, text='Find', command=lambda: find("resp"), highlightthickness=0, bd=0,
                           background="gray")
        butt_resp.place(x=380, y=0, height=21, width=60)

        # This method is used to search the response text and highlight the searched word in red
        def find(method):
            if method == "resp":
                textw = responseText
            else:
                textw = self.curlText
            textw.tag_remove('found', '1.0', END)

            # returns to widget currently in focus
            s = edit.get()
            if s:
                idx = '1.0'
                while 1:
                    # searches for desried string from index 1
                    idx = textw.search(s, idx, nocase=1,
                                       stopindex=END)
                    if not idx: break

                    # last index sum of current index and
                    # length of text
                    lastidx = '%s+%dc' % (idx, len(s))

                    # overwrite 'Found' at idx
                    textw.tag_add('found', idx, lastidx)
                    idx = lastidx
                    # textw.see(idx)  # Once found, the scrollbar automatically scrolls to the text

                # mark located string as red
                textw.tag_config('found', foreground='red')

        edit.focus_set()




    '''   def downloadFile(method):
            files = [('JSON', '*.json'),
                     ('Text Document', '*.txt')]
            file = filedialog.asksaveasfile(filetypes=files, defaultextension='.json')
            filetext = str(payloadText.get("1.0", END)) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")
            '''


#Frame for Page 1 - update Course Run
class updateCourseRunPageSelect(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Update Course Run", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        self.var = IntVar()
        Radiobutton(self, text="Upload a Course Run JSON File", variable=self.var, value=1).place(x=158,y=100)
        Radiobutton(self, text="Fill in the basic mandate form", variable=self.var, value=2).place(x=158,y=130)
        self.var.set(2)

        label_0 = Label(self, text="Basic Mandate Form", width=20, font=("bold", 15))
        label_0.place(x=137, y=185)

        label_CRN = Label(self, text="Course Reference Number*", width=20, font=("bold", 10))
        label_CRN.place(x=80, y=220)

        label_CRN_ttp = CreateToolTip(label_CRN, tooltipDescription["CourseReferenceNumber"])

        entry_CRN = Entry(self)
        entry_CRN.place(x=250, y=220)


        label_runTitle = Label(self, text="Run", width=20, font=("bold", 15))
        label_runTitle.place(x=137, y=250)

        label_openRegDate = Label(self, text="Opening Registration Dates*", width=20, font=("bold", 10))
        label_openRegDate.place(x=80, y=285)

        label_openRegDate_ttp = CreateToolTip(label_openRegDate, tooltipDescription["CourseRegistrationDateOpen"])

        entry_openRegDate = Entry(self)
        entry_openRegDate.place(x=250, y=285)

        label_closeRegDate = Label(self, text="Closing Registration Dates*", width=20, font=("bold", 10))
        label_closeRegDate.place(x=80, y=310)

        label_closeRegDate_ttp = CreateToolTip(label_closeRegDate, tooltipDescription["CourseRegistrationDateClose"])

        entry_closeRegDate = Entry(self)
        entry_closeRegDate.place(x=250, y=310)

        label_CourseStartDate = Label(self, text="Course Start Date*", width=20, font=("bold", 10))
        label_CourseStartDate.place(x=80, y=335)

        label_CourseStartDate_ttp = CreateToolTip(label_CourseStartDate, tooltipDescription["CourseStartDate"])

        entry_CourseStartDate = Entry(self)
        entry_CourseStartDate.place(x=250, y=335)

        label_CourseEndDate = Label(self, text="Course End Date*", width=20, font=("bold", 10))
        label_CourseEndDate.place(x=80, y=360)

        label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_CourseEndDate = Entry(self)
        entry_CourseEndDate.place(x=250, y=360)
        
        label_scheduleInfoType = Label(self, text="InfoType*", width=20, font=("bold", 10))
        label_scheduleInfoType.place(x=80, y=385)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_scheduleInfoType = Entry(self)
        entry_scheduleInfoType.place(x=250, y=385)

        label_scheduleInfoTypeDescription = Label(self, text="InfoType Description", width=20, font=("bold", 10))
        label_scheduleInfoTypeDescription.place(x=80, y=410)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_scheduleInfoTypeDescription = Entry(self)
        entry_scheduleInfoTypeDescription.place(x=250, y=410)

        label_CourseModeOfTraining = Label(self, text="Mode Of Training", width=20, font=("bold", 10))
        label_CourseModeOfTraining.place(x=80, y=435)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_CourseModeOfTraining = Entry(self)
        entry_CourseModeOfTraining.place(x=250, y=435)

        label_adminEmail = Label(self, text="Course Admin Email", width=20, font=("bold", 10))
        label_adminEmail.place(x=80, y=460)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_adminEmail = Entry(self)
        entry_adminEmail.place(x=250, y=460)

        label_threshold = Label(self, text="Threshold", width=20, font=("bold", 10))
        label_threshold.place(x=80, y=485)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_threshold = Entry(self)
        entry_threshold.place(x=250, y=485)

        label_intakeSize = Label(self, text="Intake Size", width=20, font=("bold", 10))
        label_intakeSize.place(x=80, y=510)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_intakeSize = Entry(self)
        entry_intakeSize.place(x=250, y=510)

        label_RegUserCount = Label(self, text="Registered User Count", width=20, font=("bold", 10))
        label_RegUserCount.place(x=80, y=535)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_RegUserCount = Entry(self)
        entry_RegUserCount.place(x=250, y=535)


        previewButton = tk.Button(self, text="Next", bg="white", width=25, pady=5, command=lambda: previewCallBack() if self.var.get() == 2 else controller.show_frame(updateCourseRunPageFormFileUpload) )
        previewButton.place(x=250, y=640, anchor=CENTER)


        #Initialies the file and object first in order to prevent clearing of data
        updateCourseRunPagePreview.payload = loadFile("EmptyUpdateCourseRunPayLoad.json")

        def storeAndsave_all():
            self.courseRunInfoPythonObject= json.loads(updateCourseRunPagePreview.payload)
            # load config File
            uen_Info = loadFile("config.json")
            config_uenJson = json.loads(uen_Info)
            uen_number = config_uenJson["UEN"]
            self.courseRunInfoPythonObject["course"]["trainingProvider"]["uen"] = uen_number

            self.courseRunInfoPythonObject["course"]["courseReferenceNumber"] = entry_CRN.get()
            self.courseRunInfoPythonObject["course"]["run"]["registrationDates"]["opening"] = entry_openRegDate.get()
            self.courseRunInfoPythonObject["course"]["run"]["registrationDates"]["closing"] = entry_closeRegDate.get()
            self.courseRunInfoPythonObject["course"]["run"]["courseDates"]["start"] = entry_CourseStartDate.get()
            self.courseRunInfoPythonObject["course"]["run"]["courseDates"]["end"] = entry_CourseEndDate.get()
            self.courseRunInfoPythonObject["course"]["run"]["scheduleInfoType"]["code"] = entry_scheduleInfoType.get()
            self.courseRunInfoPythonObject["course"]["run"]["scheduleInfoType"]["description"] = entry_scheduleInfoTypeDescription.get()
            self.courseRunInfoPythonObject["course"]["run"]["modeOfTraining"] = entry_CourseModeOfTraining.get()
            self.courseRunInfoPythonObject["course"]["run"]["courseAdminEmail"] = entry_adminEmail.get()
            self.courseRunInfoPythonObject["course"]["run"]["threshold"] = entry_threshold.get()
            self.courseRunInfoPythonObject["course"]["run"]["intakeSize"] = entry_intakeSize.get()
            self.courseRunInfoPythonObject["course"]["run"]["registeredUserCount"] = entry_RegUserCount.get()

            return str(json.dumps(self.courseRunInfoPythonObject,indent=4))
        def previewCallBack():
            updateCourseRunPagePreview.payload = storeAndsave_all()
            controller.show_frame(updateCourseRunPagePage2)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#Page 2 for Update Course Run  
class updateCourseRunPagePage2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_1 = Label(self, text="Run", width=20, font=("bold", 15))
        label_1.place(x=137, y=100)

        label_courseVacCode = Label(self, text="Course Vacancy Code*", width=20, font=("bold", 10))
        label_courseVacCode.place(x=80, y=140)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        entry_courseVacCode = Entry(self)
        entry_courseVacCode.place(x=250, y=140)

        label_courseVacDescription = Label(self, text="Course Vacancy Description", width=20, font=("bold", 10))
        label_courseVacDescription.place(x=80, y=165)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        entry_courseVacDescription = Entry(self)
        entry_courseVacDescription.place(x=250, y=165)

        label_scheduleInfo = Label(self, text="Schedule Info", width=20, font=("bold", 10))
        label_scheduleInfo.place(x=80, y=190)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        entry_scheduleInfo = Entry(self)
        entry_scheduleInfo.place(x=250, y=190)

        label_venueRoom = Label(self, text="Venue - Room*", width=20, font=("bold", 10))
        label_venueRoom.place(x=80, y=215)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        entry_venueRoom = Entry(self)
        entry_venueRoom.place(x=250, y=215)

        label_venueUnit = Label(self, text="Venue - Unit*", width=20, font=("bold", 10))
        label_venueUnit.place(x=80, y=240)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        entry_venueUnit = Entry(self)
        entry_venueUnit.place(x=250, y=240)

        label_venueFloor = Label(self, text="Venue - Floor*", width=20, font=("bold", 10))
        label_venueFloor.place(x=80, y=265)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        entry_venueFloor = Entry(self)
        entry_venueFloor.place(x=250, y=265)

        label_venueBlock = Label(self, text="Venue - Block", width=20, font=("bold", 10))
        label_venueBlock.place(x=80, y=290)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        entry_venueBlock = Entry(self)
        entry_venueBlock.place(x=250, y=290)

        label_venueStreet = Label(self, text="Venue - Street", width=20, font=("bold", 10))
        label_venueStreet.place(x=80, y=315)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        entry_venueStreet = Entry(self)
        entry_venueStreet.place(x=250, y=315)

        label_venueBuilding = Label(self, text="Venue - Building", width=20, font=("bold", 10))
        label_venueBuilding.place(x=80, y=340)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        entry_venueBuilding = Entry(self)
        entry_venueBuilding.place(x=250, y=340)

        label_venuePostalCode = Label(self, text="Venue - Postal Code", width=20, font=("bold", 10))
        label_venuePostalCode.place(x=80, y=365)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        entry_venuePostalCode = Entry(self)
        entry_venuePostalCode.place(x=250, y=365)

        label_venueWheelchair = Label(self, text="Venue - Wheelchair Access", width=20, font=("bold", 10))
        label_venueWheelchair.place(x=80, y=390)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        tkvar = StringVar(self)
        choices = { 'False','True'}
        tkvar.set("Select an Option")
        options_Wheelchair = OptionMenu(self, tkvar, *choices)
        options_Wheelchair.place(x=250, y=390, width=125)


        def storeAndsave_all():
            print("store and save")
            payloadToEdit = updateCourseRunPagePreview.payload
            payloadToEdit= json.loads(payloadToEdit)
            payloadToEdit['course']['run']['courseVacancy']['code'] = entry_courseVacCode.get()
            payloadToEdit['course']['run']['courseVacancy']['description'] = entry_courseVacDescription.get()
            payloadToEdit['course']['run']['scheduleInfo'] = entry_scheduleInfo.get()
            payloadToEdit['course']['run']['venue']['floor'] = entry_venueFloor.get()
            payloadToEdit['course']['run']['venue']['unit'] = entry_venueUnit.get()
            payloadToEdit['course']['run']['venue']['room'] = entry_venueRoom.get()
            payloadToEdit['course']['run']['venue']['building'] = entry_venueBuilding.get()
            payloadToEdit['course']['run']['venue']['block'] = entry_venueBlock.get()
            payloadToEdit['course']['run']['venue']['postalCode'] = entry_venuePostalCode.get()
            payloadToEdit['course']['run']['venue']['street'] = entry_venueStreet.get()
            payloadToEdit['course']['run']['venue']['wheelChairAccess'] = tkvar.get() if tkvar.get() != 'Select an Option' else ''

            # print(payloadToEdit)
            return str(json.dumps(payloadToEdit,indent=4))

        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(updateCourseRunPageSelect)
                               )
        backButton.place(relx=0.055, rely=0.021, anchor=CENTER)

        def callback():

            updateCourseRunPagePreview.payload = storeAndsave_all()
            # updateCourseRunPageSelect.updateCourseRunInfo = storeAndsave_all()
            # updateCourseRunPagePreview.refresh(controller.frames[updateCourseRunPagePreview].curlText)
            controller.show_frame(updateCourseRunPagePage3)

        previewButton = tk.Button(self, text="Next", bg="white", width=25, pady=5, command=lambda: callback())
        previewButton.place(x=250, y=640, anchor=CENTER)

#Page 3 for Update Course Run - Sessions
class updateCourseRunPagePage3(tk.Frame):
    def deleteFrameInit(self, deleteFrame):

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(deleteFrame, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        self.label_sessionId = Label(deleteFrame, text="Session Id*", width=20, font=("bold", 10))
        self.label_sessionId.place(x=0, y=0)

        self.entry_sessionId = Entry(deleteFrame)
        self.entry_sessionId.place(x=170, y=0)

    def updateFrame(self,updateFrame):
        self.addFrame(updateFrame)        
        self.label_sessionId= Label(updateFrame, text="Session Id*", width=20, font=("bold", 10))
        self.label_sessionId.place(x=0, y=350)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_sessionId = Entry(updateFrame)
        self.entry_sessionId.place(x=170, y=350)


    def addFrame(self,AddFrame):

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(AddFrame, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_ModeOfTraining = Label(AddFrame, text="Mode of Training*", width=20, font=("bold", 10))
        label_ModeOfTraining.place(x=0, y=0)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_ModeOfTraining = Entry(AddFrame)
        self.entry_ModeOfTraining.place(x=170, y=0)


        self.label_SessionStartDate = Label(AddFrame, text="Session Start Date*", width=20, font=("bold", 10))
        self.label_SessionStartDate.place(x=0, y=25)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionStartDate = Entry(AddFrame)
        self.entry_SessionStartDate.place(x=170, y=25)

        self.label_SessionEndDate = Label(AddFrame, text="Session End Date*", width=20, font=("bold", 10))
        self.label_SessionEndDate.place(x=0, y=50)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionEndDate = Entry(AddFrame)
        self.entry_SessionEndDate.place(x=170, y=50)

        self.label_SessionStartTime = Label(AddFrame, text="Session Start Time*", width=20, font=("bold", 10))
        self.label_SessionStartTime.place(x=0, y=75)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionStartTime = Entry(AddFrame)
        self.entry_SessionStartTime.place(x=170, y=75)

        self.label_SessionEndTime = Label(AddFrame, text="Session End Time*", width=20, font=("bold", 10))
        self.label_SessionEndTime.place(x=0, y=100)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionEndTime = Entry(AddFrame)
        self.entry_SessionEndTime.place(x=170, y=100)

        self.label_SessionVenueRoom = Label(AddFrame, text="Venue Room*", width=20, font=("bold", 10))
        self.label_SessionVenueRoom.place(x=0, y=125)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenueRoom = Entry(AddFrame)
        self.entry_SessionVenueRoom.place(x=170, y=125)

        self.label_SessionVenueUnit= Label(AddFrame, text="Venue Unit*", width=20, font=("bold", 10))
        self.label_SessionVenueUnit.place(x=0, y=150)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenueUnit = Entry(AddFrame)
        self.entry_SessionVenueUnit.place(x=170, y=150)

        self.label_SessionVenueFloor= Label(AddFrame, text="Venue Floor*", width=20, font=("bold", 10))
        self.label_SessionVenueFloor.place(x=0, y=175)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenueFloor = Entry(AddFrame)
        self.entry_SessionVenueFloor.place(x=170, y=175)

        self.label_SessionVenueBuilding= Label(AddFrame, text="Venue Building", width=20, font=("bold", 10))
        self.label_SessionVenueBuilding.place(x=0, y=200)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenueBuilding = Entry(AddFrame)
        self.entry_SessionVenueBuilding.place(x=170, y=200)

        self.label_SessionVenueBlock= Label(AddFrame, text="Venue Block", width=20, font=("bold", 10))
        self.label_SessionVenueBlock.place(x=0, y=225)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenueBlock = Entry(AddFrame)
        self.entry_SessionVenueBlock.place(x=170, y=225)

        self.label_SessionVenueStreet= Label(AddFrame, text="Venue Street", width=20, font=("bold", 10))
        self.label_SessionVenueStreet.place(x=0, y=250)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenueStreet = Entry(AddFrame)
        self.entry_SessionVenueStreet.place(x=170, y=250)

        self.label_SessionVenuePostalCode= Label(AddFrame, text="Venue Postal Code*", width=20, font=("bold", 10))
        self.label_SessionVenuePostalCode.place(x=0, y=275)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenuePostalCode = Entry(AddFrame)
        self.entry_SessionVenuePostalCode.place(x=170, y=275)

        self.tkvar_Wheelchair = StringVar(self)
        self.tkvar_PriVenue = StringVar(self)
        choices = { 'False','True'}
        self.tkvar_Wheelchair.set("Select an Option")
        self.tkvar_PriVenue.set("Select an Option")

        self.label_SessionVenuePostalCode= Label(AddFrame, text="Venue Primary Venue", width=20, font=("bold", 10))
        self.label_SessionVenuePostalCode.place(x=0, y=300)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        options_PrimaryVenue = OptionMenu(AddFrame, self.tkvar_PriVenue, *choices)
        options_PrimaryVenue.place(x=170, y=300, width=125)

        self.label_SessionVenuePostalCode= Label(AddFrame, text="Venue Wheelchair Access", width=20, font=("bold", 10))
        self.label_SessionVenuePostalCode.place(x=0, y=325)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        options_Wheelchair = OptionMenu(AddFrame, self.tkvar_Wheelchair, *choices)
        options_Wheelchair.place(x=170, y=325, width=125)


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        #Setting of frame based on Choice for "action"
        def hide(choice):
            if choice == 'Delete':
                print('delete')
                deleteFrame.place(width = 300, height = 300, x = 80, y = 200)
                addFrame.place_forget()
                updateFrame.place_forget()
            elif choice == 'Add':
                print('Add')
                deleteFrame.place_forget()
                addFrame.place(width = 300, height = 400, x = 80, y = 200)
                updateFrame.place_forget()
            elif choice == 'All':
                updateFrame.place_forget()
                deleteFrame.place_forget()
                addFrame.place_forget()
            else:
                updateFrame.place(width = 300, height = 400, x = 80, y = 200)
                deleteFrame.place_forget()
                addFrame.place_forget()

        addFrame = tk.Frame()
        deleteFrame = tk.Frame()
        updateFrame = tk.Frame()

        self.addFrame(addFrame)
        self.updateFrame(updateFrame)
        self.deleteFrameInit(deleteFrame)
        self.tkvar = StringVar(self)
        choices = {'Add','Delete', 'Update'}
        self.tkvar.set("Select an Option")
        options_Session_Action= OptionMenu(self, self.tkvar, *choices, command=lambda x: hide(self.tkvar.get()))
        options_Session_Action.place(x=250, y=140, width=125)

        label_1 = Label(self, text="Sessions", width=20, font=("bold", 15))
        label_1.place(x=137, y=100)

        label_courseVacCode = Label(self, text="Action*", width=20, font=("bold", 10))
        label_courseVacCode.place(x=80, y=140)

        def callback():
            hide('All')
            
            updateCourseRunPagePreview.refresh(controller.frames[updateCourseRunPagePreview].curlText)
            controller.show_frame(updateCourseRunPagePreview)
        
        def addCallback():
            payloadToEdit = updateCourseRunPagePreview.payload
            payloadToEdit= json.loads(payloadToEdit)
            priVenue = self.tkvar_PriVenue.get() if self.tkvar_PriVenue.get() != 'Select an Option' else ''
            wheelChair = self.tkvar_Wheelchair.get() if self.tkvar_PriVenue.get() != 'Select an Option' else ''

            sessionObjectTemplate = {
                "action":self.tkvar.get(),
                "endDate":self.entry_SessionEndDate.get(),
                "endTime":self.entry_SessionEndTime.get(),
                "sessionId":self.entry_sessionId.get(),
                "startDate":self.entry_SessionStartDate.get(),
                "startTime":self.entry_SessionStartTime.get(),
                "modeOfTraining":self.entry_ModeOfTraining.get(),
                "venue":{
                    "room":self.entry_SessionVenueRoom.get(),
                    "unit":self.entry_SessionVenueUnit.get(),
                    "block":self.entry_SessionVenueBlock.get(),
                    "floor":self.entry_SessionVenueFloor.get(),
                    "street":self.entry_SessionVenueStreet.get(),
                    "building":self.entry_SessionVenueBuilding.get(),
                    "postalCode":self.entry_SessionVenuePostalCode.get(),
                    "primaryVenue":priVenue,
                    "wheelChairAccess":wheelChair
                }
            }

            print(payloadToEdit['course']['run']['sessions'])
            payloadToEdit['course']['run']['sessions'].append(sessionObjectTemplate)
            updateCourseRunPagePreview.payload = json.dumps(payloadToEdit, indent = 4)
            print(updateCourseRunPagePreview.payload)
            tkinter.messagebox.showinfo(title="Success", message="Session successfully added")
            previewButton.place(relx=0.7, rely=0.95, anchor=CENTER)
            
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(updateCourseRunPagePage2)
                               )
        backButton.place(relx=0.055, rely=0.021, anchor=CENTER)
        addButton = tk.Button(self, text="Add", bg="white", width=15, pady=5, command=lambda: addCallback())
        addButton.place(relx=0.3, rely=0.95, anchor=CENTER)
        previewButton = tk.Button(self, text="Next", bg="white", width=15, pady=5, command=lambda: callback())
        




class updateCourseRunPageFormFileUpload(tk.Frame):
    global fileUploadEntry
    global contentInfo
    contentInfo = ''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Update Course Run", width=20, font=("bold", 20))
        label_0.place(x=90, y=43)

        
        #Course Run Id
        label_runId = Label(self, text="Course Run ID: ", width=20, font=("bold", 10), anchor='w')
        label_runId.place(x=90, y=100)

        entry_runId = Entry(self)
        entry_runId.place(x=250, y=100)
        label_1_ttp = CreateToolTip(label_runId, tooltipDescription["CourseRunId"])

        #This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing():

            value = curlPostRequest(entry_runId.get(),contentInfo)
            curlText.delete("1.0","end")
            curlText.insert(tk.END, value)

        entry_runId.bind('<KeyRelease>', lambda b:typing())

        fileuploadframe = tk.Frame(self)
        fileuploadframe.place(x=90, y=130)

        fileUploadEntry = tk.Entry(fileuploadframe, width=45)
        fileUploadEntry.pack(side=tk.LEFT, fill=tk.X )
        fileUploadButton = tk.Button(self,text="Browse", command=lambda:getCertPemFile(self))       
        fileUploadButton.pack(in_=fileuploadframe, side=tk.LEFT)

         #Configuration for Notebook layout
        tabControl = ttk.Notebook(self)
  
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        
        #Adding of tabs
        tabControl.add(tab2, text ='Request')
        tabControl.add(tab3, text ='Reponse')
        tabControl.place(width= 440, height= 460, x = 30, y = 222)

        curlText = scrolledtext.ScrolledText(tab2,width=70,height=30)
        curlText.insert(tk.END, str(curlPostRequest("","")))
        curlText.place(height = 405, width = 440, y=20)
        curlText.bind("<Key>", lambda e: "break")
        
        responseText = scrolledtext.ScrolledText(tab3,width=70,height=30)
        responseText.place(height = 405, width = 440, y=20)
        # responseText.bind("<Key>", lambda e: "break")

        updateButton = tk.Button(self, text="Update", bg="white", width=25, pady=5, command=lambda: updateCallBack(entry_runId.get()))
        updateButton.place(relx=0.5, rely=0.25, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(updateCourseRunPageSelect)
                               )
        backButton.place(relx=0.055, rely=0.021, anchor=CENTER)
        # exportButton1 = tk.Button(self, text="Export Payload", bg="white", width=15, pady=5, command = lambda: downloadFile("payload"))
        # exportButton1.place(relx=0.3, rely=0.95, anchor=CENTER)
        # exportButton2 = tk.Button(self, text="Export Response", bg="white", width=15, pady=5,command = lambda: downloadFile("response"))
        # exportButton2.place(relx=0.7, rely=0.95, anchor=CENTER)
        
        #adding of single line text box
        edit = Entry(self, background="light gray") 

        #positioning of text box
        edit.place(x = 285, height= 21, y=244) 

        #setting focus
        edit.focus_set()

        butt_resp = Button(tab2, text='Find', command=lambda:find("curl"), highlightthickness = 0, bd = 0, background="gray")  
        butt_resp.place(x = 380, y=0, height=21, width=60) 
        butt_resp = Button(tab3, text='Find', command=lambda:find("resp"), highlightthickness = 0, bd = 0, background="gray")  
        butt_resp.place(x = 380, y=0, height=21, width=60) 

        #This method is used to search the response text and highlight the searched word in red
        def find(method):
            if method == "resp":
                textw = responseText
            else:
                textw = curlText
            textw.tag_remove('found', '1.0', END) 
            
            #returns to widget currently in focus
            s = edit.get() 
            if s:
                idx = '1.0'
                while 1:
                    #searches for desried string from index 1
                    idx = textw.search(s, idx, nocase=1, 
                                    stopindex=END) 
                    if not idx: break
                    
                    #last index sum of current index and
                    #length of text
                    lastidx = '%s+%dc' % (idx, len(s)) 
                    
                    #overwrite 'Found' at idx
                    textw.tag_add('found', idx, lastidx) 
                    idx = lastidx
                    # textw.see(idx)  # Once found, the scrollbar automatically scrolls to the text
                
                #mark located string as red
                textw.tag_config('found', foreground='red') 
               
            edit.focus_set()

        def getCertPemFile(window):
            curlText.delete("1.0","end")
            filePath=filedialog.askopenfilename(filetypes=[('JSON', '*.json')])
            fileUploadEntry.delete(0, 'end')
            fileUploadEntry.insert(1, filePath)
            global contentInfo
            with open(filePath, 'r') as content:
                contentInfo = content.read()

            curlText.insert(tk.END, curlPostRequest(entry_runId.get(),contentInfo))
                

        def updateCallBack(runId):
            responseText.delete("1.0","end")
            payload = contentInfo
            # payload = json.loads(payload)
            # print(payload)
            resp = updateCourserun(runId,payload)
            textPayload = StringVar(self, value = resp.text) 
            responseText.insert(INSERT,textPayload.get())
            

# resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/224925/sessions?uen=199900650G&courseReferenceNumber=TGS-2020001831&sessionMonth=062021")
# print(resp.text)