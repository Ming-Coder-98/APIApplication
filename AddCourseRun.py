#Import course Run py Functions
import tkinter
from tkinter import scrolledtext

from requests.api import request
from configWindow import getCertPemFile, setConfigWindow, showConfigWindow
from AssessmentFunction import addAssessment
from EnrolmentFunction import addEnrolment, enrollmentInitialization
from AttendanceFunction import uploadAttendance
from courseRunFunctions import createCourserun, curlPostRequest, deleteCourserun, getCourseRun, getDeleteCourseRunPayLoad
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


class addCourseRunPageOptional(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Optional fields", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        label_1 = Label(self, text="Sessions", width=20, font=("bold", 15))
        label_1.place(x=137, y=100)

        label_14 = Label(self, text="Course Session Start Date:", width=20, font=("bold", 10))
        label_14.place(x=80, y=135)

        label_14_ttp = CreateToolTip(label_14,tooltipDescription["SessionStartDate"])

        entry_14 = Entry(self)
        entry_14.place(x=250, y=135)

        label_15 = Label(self, text="Course Session Start Time:", width=20, font=("bold", 10))
        label_15.place(x=80, y=160)

        label_15_ttp = CreateToolTip(label_15,tooltipDescription["SessionStartTime"])

        entry_15 = Entry(self)
        entry_15.place(x=250, y=160)

        label_16 = Label(self, text="Course Session End Date:", width=20, font=("bold", 10))
        label_16.place(x=80, y=185)

        label_16_ttp = CreateToolTip(label_16,tooltipDescription["SessionEndDate"])

        entry_16 = Entry(self)
        entry_16.place(x=250, y=185)

        label_17 = Label(self, text="Course Session End Time:", width=20, font=("bold", 10))
        label_17.place(x=80, y=210)

        label_17_ttp = CreateToolTip(label_17, tooltipDescription["SessionEndTime"])

        entry_17 = Entry(self)
        entry_17.place(x=250, y=210)

        label_18 = Label(self, text="Mode of Training:", width=20, font=("bold", 10))
        label_18.place(x=80, y=235)

        label_18_ttp = CreateToolTip(label_18,
                                    'Mode of Training is used as a parameter in the POST Request payload \n'
                                    'Example: 9')

        modeOfTraining = ttk.Combobox(self, width = 27,state="readonly")
        modeOfTraining['values'] = ["Select An Option",
                     "1. Classroom",
                     "2. Asynchronous eLearning",
                     "3. In-house",
                     "4. On-the-Job",
                     "5. Practical/Practicum",
                     "6. Supervised Field",
                     "7. Traineeship",
                     "8. Assessment",
                     "9. Synchronous eLearning"]
        modeOfTraining.current(0)
        modeOfTraining.place(x=250, y=235)

        def finalSelection18():
            entry_18 = modeOfTraining.get()[0]
            return entry_18

        label_19 = Label(self, text="Trainers", width=20, font=("bold", 15))
        label_19.place(x=137, y=270)

        label_20 = Label(self, text="Trainer name:", width=20, font=("bold", 10))
        label_20.place(x=80, y=305)

        label_20_ttp = CreateToolTip(label_20, tooltipDescription["TrainerName"])

        entry_20 = Entry(self)
        entry_20.place(x=250, y=305)

        label_21 = Label(self, text="Trainer Email:", width=20, font=("bold", 10))
        label_21.place(x=80, y=330)

        label_21_ttp = CreateToolTip(label_21,tooltipDescription["TrainerEmail"])

        entry_21 = Entry(self)
        entry_21.place(x=250, y=330)

        label_22 = Label(self, text="Trainer Code:", width=20, font=("bold", 10))
        label_22.place(x=80, y=355)

        label_22_ttp = CreateToolTip(label_22, tooltipDescription["TrainerCode"])

        entry_22 = Entry(self)
        entry_22.place(x=250, y=355)

        label_23 = Label(self, text="Trainer description:", width=20, font=("bold", 10))
        label_23.place(x=80, y=380)

        label_23_ttp = CreateToolTip(label_23, tooltipDescription["TrainerDescription"])

        entry_23 = Entry(self)
        entry_23.place(x=250, y=380)




        def typing(event):
            storeAndsave_all()

        entry_14.bind('<KeyRelease>', typing)
        entry_15.bind('<KeyRelease>', typing)
        entry_16.bind('<KeyRelease>', typing)
        entry_17.bind('<KeyRelease>', typing)
        entry_20.bind('<KeyRelease>', typing)
        entry_21.bind('<KeyRelease>', typing)
        entry_22.bind('<KeyRelease>', typing)
        entry_23.bind('<KeyRelease>', typing)

        def storeAndsave_all():

            page1 = json.loads(loadFile("CompletedCourseRunPayLoad.json"))
            page1["course"]["sessions"][0]["startDate"] = entry_14.get()
            page1["course"]["sessions"][0]["startTime"] = entry_15.get()
            page1["course"]["sessions"][0]["endDate"] = entry_16.get()
            page1["course"]["sessions"][0]["endTime"] = entry_17.get()
            page1["course"]["sessions"][0]["modeOfTraining"] = finalSelection18()
            page1["course"]["linkCourseRunTrainer"][0]["trainer"]["name"] = entry_20.get()
            page1["course"]["linkCourseRunTrainer"][0]["trainer"]["email"] = entry_21.get()
            page1["course"]["linkCourseRunTrainer"][0]["trainer"]["trainerType"]["code"] = entry_22.get()
            page1["course"]["linkCourseRunTrainer"][0]["trainer"]["trainerType"]["description"]= entry_23.get()
            saveJsonFormat(page1, "CompletedCourseRunPayload.json")


        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(addCourseRunPage1)
                               )
        backButton.place(relx=0.055, rely=0.021, anchor=CENTER)

        def callback():
            # print("test")
            # print(controller.frames[addCourseRunPageForm].curlText.get('1.0', tk.END))
            test=controller.frames[addCourseRunPageForm].curlText
            addCourseRunPageForm.refresh(test)
            controller.show_frame(addCourseRunPageForm)

        previewButton = tk.Button(self, text="Next", bg="white", width=25, pady=5, command=lambda: callback())
        previewButton.place(x=250, y=440, anchor=CENTER)



class addCourseRunPageForm(tk.Frame):
    def refresh(text):
        text.delete("1.0","end")
        text.insert(tk.END, addCourseRunPageForm.payload)

    def __init__(self, parent, controller):

        self.payload = {}
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        label_0 = Label(self, text="Add Course Run", width=20, font=("bold", 20))
        label_0.place(x=90, y=85)

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

        self.curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        self.curlText.insert(tk.END, str(curlPostRequest("", "")))
        self.curlText.place(height=405, width=440, y=20)
        self.curlText.bind("<Key>", lambda e: "break")

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        # responseText.bind("<Key>", lambda e: "break")

        def submitCallBack():
            responseText.delete("1.0","end")
            resp = createCourserun(addCourseRunPageForm.payload)
            print(addCourseRunPageForm.payload)
            print(resp.status_code)
            textPayload = StringVar(self, value = resp.text) 
            responseText.insert(INSERT, textPayload.get())
            
        submitButton = tk.Button(self, text="Create", bg="white", width=25, pady=5, command=lambda: submitCallBack())
        submitButton.place(relx=0.5, rely=0.25, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(addCourseRunPage1),
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



'''
      def downloadFile(method):
            files = [('JSON', '*.json'),
                     ('Text Document', '*.txt')]
            file = filedialog.asksaveasfile(filetypes=files, defaultextension='.json')
            filetext = str(payloadText.get("1.0", END)) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")
         '''


class addCourseRunPageFormFileUpload(tk.Frame):
    global fileUploadEntry

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Add Course Run", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)
        fileuploadframe = tk.Frame(self)
        fileuploadframe.place(x=90, y=120)

        fileUploadEntry = tk.Entry(fileuploadframe, width=45)
        fileUploadEntry.pack(side=tk.LEFT, fill=tk.X )
        createButton = tk.Button(self,text="Browse", command=lambda:getCertPemFile(self))       
        createButton.pack(in_=fileuploadframe, side=tk.LEFT)

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

        submitButton = tk.Button(self, text="Create", bg="white", width=25, pady=5, command=lambda: submitCallBack())
        submitButton.place(relx=0.5, rely=0.25, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(addCourseRunPage1)
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

            curlText.insert(tk.END, curlPostRequest("",contentInfo))
                

        def submitCallBack():
            responseText.delete("1.0","end")
            payload = contentInfo
            # payload = json.loads(payload)
            # print(payload)
            resp = createCourserun(payload)
            textPayload = StringVar(self, value = resp.text) 
            responseText.insert(INSERT,textPayload.get())


# Frame for Page 1 - Add Course Run
class addCourseRunPage1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Add Course Run", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        self.var = IntVar()
        Radiobutton(self, text="Upload a Course Run JSON File", variable=self.var, value=1).place(x=158, y=100)
        Radiobutton(self, text="Fill in the basic mandate form", variable=self.var, value=2).place(x=158, y=130)
        self.var.set(2)

        label_0 = Label(self, text="Basic Mandate Form", width=20, font=("bold", 15))
        label_0.place(x=137, y=185)

        label_CRN = Label(self, text="Course Reference Number*", width=20, font=("bold", 10))
        label_CRN.place(x=80, y=230)

        label_CRN_ttp = CreateToolTip(label_CRN, tooltipDescription["CourseReferenceNumber"])

        entry_CRN = Entry(self)
        entry_CRN.place(x=250, y=230)

        label_runTitle = Label(self, text="Run", width=20, font=("bold", 15))
        label_runTitle.place(x=137, y=270)

        label_openRegDate = Label(self, text="Opening Registration Dates*", width=20, font=("bold", 10))
        label_openRegDate.place(x=80, y=310)

        label_openRegDate_ttp = CreateToolTip(label_openRegDate, tooltipDescription["CourseRegistrationDateOpen"])

        entry_openRegDate = Entry(self)
        entry_openRegDate.place(x=250, y=310)

        label_closeRegDate = Label(self, text="Closing Registration Dates*", width=20, font=("bold", 10))
        label_closeRegDate.place(x=80, y=335)

        label_closeRegDate_ttp = CreateToolTip(label_closeRegDate, tooltipDescription["CourseRegistrationDateClose"])

        entry_closeRegDate = Entry(self)
        entry_closeRegDate.place(x=250, y=335)

        label_CourseStartDate = Label(self, text="Course Start Date*", width=20, font=("bold", 10))
        label_CourseStartDate.place(x=80, y=360)

        label_CourseStartDate_ttp = CreateToolTip(label_CourseStartDate, tooltipDescription["CourseStartDate"])

        entry_CourseStartDate = Entry(self)
        entry_CourseStartDate.place(x=250, y=360)

        label_CourseEndDate = Label(self, text="Course End Date*", width=20, font=("bold", 10))
        label_CourseEndDate.place(x=80, y=385)

        label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_CourseEndDate = Entry(self)
        entry_CourseEndDate.place(x=250, y=385)

        label_scheduleInfoType = Label(self, text="InfoType*", width=20, font=("bold", 10))
        label_scheduleInfoType.place(x=80, y=410)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_scheduleInfoType = Entry(self)
        entry_scheduleInfoType.place(x=250, y=410)

        label_scheduleInfoTypeDescription = Label(self, text="InfoType Description", width=20, font=("bold", 10))
        label_scheduleInfoTypeDescription.place(x=80, y=435)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_scheduleInfoTypeDescription = Entry(self)
        entry_scheduleInfoTypeDescription.place(x=250, y=435)

        label_CourseModeOfTraining = Label(self, text="Mode Of Training", width=20, font=("bold", 10))
        label_CourseModeOfTraining.place(x=80, y=460)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])
        modeOfTraining = ttk.Combobox(self, width=27, state="readonly")
        modeOfTraining['values'] = ["Select An Option",
                                    "1. Classroom",
                                    "2. Asynchronous eLearning",
                                    "3. In-house",
                                    "4. On-the-Job",
                                    "5. Practical/Practicum",
                                    "6. Supervised Field",
                                    "7. Traineeship",
                                    "8. Assessment",
                                    "9. Synchronous eLearning"]
        modeOfTraining.current(0)
        modeOfTraining.place(x=250, y=460)
        # entry_CourseModeOfTraining = Entry(self)
        # entry_CourseModeOfTraining.place(x=250, y=435)

        label_adminEmail = Label(self, text="Course Admin Email", width=20, font=("bold", 10))
        label_adminEmail.place(x=80, y=485)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_adminEmail = Entry(self)
        entry_adminEmail.place(x=250, y=485)

        label_threshold = Label(self, text="Threshold", width=20, font=("bold", 10))
        label_threshold.place(x=80, y=510)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_threshold = Entry(self)
        entry_threshold.place(x=250, y=510)

        label_intakeSize = Label(self, text="Intake Size", width=20, font=("bold", 10))
        label_intakeSize.place(x=80, y=535)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_intakeSize = Entry(self)
        entry_intakeSize.place(x=250, y=535)

        label_RegUserCount = Label(self, text="Registered User Count", width=20, font=("bold", 10))
        label_RegUserCount.place(x=80, y=560)

        # label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_RegUserCount = Entry(self)
        entry_RegUserCount.place(x=250, y=560)

        previewButton = tk.Button(self, text="Next", bg="white", width=25, pady=5,
                                  command=lambda: previewCallBack() if self.var.get() == 2 else controller.show_frame(
                                      addCourseRunPageFormFileUpload))
        previewButton.place(x=250, y=650, anchor=CENTER)

        # Initialies the file and object first in order to prevent clearing of data
        # addCourseRunPagePreview.payload = loadFile("EmptyaddCourseRunPayLoad.json")
        addCourseRunPageForm.payload = "{}"

        def storeAndsave_all():
            # load config File
            uen_Info = loadFile("config.json")
            config_uenJson = json.loads(uen_Info)
            uen_number = config_uenJson["UEN"]
            # self.courseRunInfoPythonObject["course"]["trainingProvider"]["uen"] = uen_number
            self.payload = json.loads(addCourseRunPageForm.payload)

            # Create the required field
            self.payload["course"] = {}
            self.payload["course"]["trainingProvider"] = {}
            self.payload["course"]["runs"] = [{}]
            self.payload["course"]["runs"][0] = {}
            self.payload["course"]["runs"][0]["registrationDates"] = {}
            self.payload["course"]["runs"][0]["courseDates"] = {}
            self.payload["course"]["runs"][0]["scheduleInfoType"] = {}

            self.payload["course"]["trainingProvider"]["uen"] = uen_number
            self.payload["course"]["courseReferenceNumber"] = entry_CRN.get()
            self.payload["course"]["runs"][0]["registrationDates"]["opening"] = entry_openRegDate.get()
            self.payload["course"]["runs"][0]["registrationDates"]["closing"] = entry_closeRegDate.get()
            self.payload["course"]["runs"][0]["courseDates"]["start"] = entry_CourseStartDate.get()
            self.payload["course"]["runs"][0]["courseDates"]["end"] = entry_CourseEndDate.get()
            self.payload["course"]["runs"][0]["scheduleInfoType"]["code"] = entry_scheduleInfoType.get()

            if entry_scheduleInfoTypeDescription.get() != '':
                self.payload["course"]["runs"][0]["scheduleInfoType"][
                    "description"] = entry_scheduleInfoTypeDescription.get()
            if modeOfTraining.get() != 'Select An Option':
                self.payload["course"]["runs"][0]["modeOfTraining"] = modeOfTraining.get()[0]
            if entry_adminEmail.get() != '':
                self.payload["course"]["runs"][0]["courseAdminEmail"] = entry_adminEmail.get()
            if entry_threshold.get() != '':
                self.payload["course"]["runs"][0]["threshold"] = entry_threshold.get()
            if entry_intakeSize.get() != '':
                self.payload["course"]["runs"][0]["intakeSize"] = entry_intakeSize.get()
            if entry_RegUserCount.get() != '':
                self.payload["course"]["runs"][0]["registeredUserCount"] = entry_RegUserCount.get()

            return str(json.dumps(self.payload, indent=4))

        def previewCallBack():
            addCourseRunPageForm.payload = storeAndsave_all()
            print(addCourseRunPageForm.payload)
            controller.show_frame(addCourseRunPage2)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Page 2 for Add Course Run  
class addCourseRunPage2(tk.Frame):
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

        self.courseVacCode = ttk.Combobox(self, width=27, state="readonly")
        self.courseVacCode['values'] = ["Select An Option",
                                    "A - Available",
                                   "L - Limited",
                                   "F - Full"]
        self.courseVacCode.current(0)
        self.courseVacCode.place(x=250, y=140)

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

        self.entry_venueRoom = Entry(self)
        self.entry_venueRoom.place(x=250, y=215)

        label_venueUnit = Label(self, text="Venue - Unit*", width=20, font=("bold", 10))
        label_venueUnit.place(x=80, y=240)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_venueUnit = Entry(self)
        self.entry_venueUnit.place(x=250, y=240)

        label_venueFloor = Label(self, text="Venue - Floor*", width=20, font=("bold", 10))
        label_venueFloor.place(x=80, y=265)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_venueFloor = Entry(self)
        self.entry_venueFloor.place(x=250, y=265)

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

        self.entry_venuePostalCode = Entry(self)
        self.entry_venuePostalCode.place(x=250, y=365)

        label_venueWheelchair = Label(self, text="Venue - Wheelchair Access", width=20, font=("bold", 10))
        label_venueWheelchair.place(x=80, y=390)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        options_Wheelchair = ttk.Combobox(self, width=27, state="readonly")
        options_Wheelchair['values'] = ["Select An Option",
                                        "True",
                                        "False"]
        options_Wheelchair.current(0)
        options_Wheelchair.place(x=250, y=390)

        def storeAndsave_all():

            payloadToEdit = addCourseRunPageForm.payload
            payloadToEdit = json.loads(payloadToEdit)

            payloadToEdit['course']['runs'][0]['courseVacancy'] = {}
            payloadToEdit['course']['runs'][0]['venue'] = {}

            payloadToEdit['course']['runs'][0]['sequenceNumber'] = 0



            payloadToEdit['course']['runs'][0]['venue']['floor'] = self.entry_venueFloor.get()
            payloadToEdit['course']['runs'][0]['venue']['unit'] = self.entry_venueUnit.get()
            payloadToEdit['course']['runs'][0]['venue']['room'] = self.entry_venueRoom.get()
            payloadToEdit['course']['runs'][0]['venue']['postalCode'] = self.entry_venuePostalCode.get()


            if entry_courseVacDescription.get() != '':
                payloadToEdit['course']['runs'][0]['courseVacancy']['description'] = entry_courseVacDescription.get()
            if entry_scheduleInfo.get() != '':
                payloadToEdit['course']['runs'][0]['scheduleInfo'] = entry_scheduleInfo.get()
            if entry_venueBuilding.get() != '':
                payloadToEdit['course']['runs'][0]['venue']['building'] = entry_venueBuilding.get()
            if entry_venueBlock.get() != '':
                payloadToEdit['course']['runs'][0]['venue']['block'] = entry_venueBlock.get()
            if entry_venueStreet.get() != '':
                payloadToEdit['course']['runs'][0]['venue']['street'] = entry_venueStreet.get()
            if options_Wheelchair.get() != 'Select An Option':
                payloadToEdit['course']['runs'][0]['venue'][
                    'wheelChairAccess'] = True if options_Wheelchair.get() == 'True' else False
            if self.courseVacCode.get() != 'Select An Option':
                payloadToEdit["course"]["runs"][0]['courseVacancy'][
                    'code'] = self.courseVacCode.get()[0]

            # print(payloadToEdit)
            return str(json.dumps(payloadToEdit, indent=4))


        backButton = tk.Button(self, text="Back", bg="white", width=10, pady= 5,
                               command=lambda: controller.show_frame(addCourseRunPage1)
                               )
        backButton.place(relx=0.055, rely=0.021, anchor=CENTER)

        def callback():
            addCourseRunPageForm.payload = storeAndsave_all()
            print(addCourseRunPageForm.payload)
            controller.show_frame(addCourseRunPage3)

        previewButton = tk.Button(self, text="Next", bg="white", width=25, pady=5, command=lambda: callback())
        previewButton.place(x=250, y=640, anchor=CENTER)


# Page 3 for add Course Run - Sessions
class addCourseRunPage3(tk.Frame):

    def addFrame(self, addFrame):
        # self.addFrame(addFrame)        
        self.label_sessionId = Label(addFrame, text="Session Id*", width=20, font=("bold", 10))
        self.label_sessionId.place(x=0, y=0)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_sessionIdadd = Entry(addFrame)
        self.entry_sessionIdadd.place(x=170, y=0)

    def addFrame(self, AddFrame):

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(AddFrame, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_ModeOfTraining = Label(AddFrame, text="Mode of Training*", width=20, font=("bold", 10))
        label_ModeOfTraining.place(x=0, y=0)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.modeOfTraining = ttk.Combobox(self, width = 27,state="readonly")
        self.modeOfTraining['values'] = ["Select An Option",
                     "1. Classroom",
                     "2. Asynchronous eLearning",
                     "3. In-house",
                     "4. On-the-Job",
                     "5. Practical/Practicum",
                     "6. Supervised Field",
                     "7. Traineeship",
                     "8. Assessment",
                     "9. Synchronous eLearning"]
        self.modeOfTraining.current(0)
        self.modeOfTraining.place(x=270, y=170)


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

        self.label_SessionVenueUnit = Label(AddFrame, text="Venue Unit*", width=20, font=("bold", 10))
        self.label_SessionVenueUnit.place(x=0, y=150)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenueUnit = Entry(AddFrame)
        self.entry_SessionVenueUnit.place(x=170, y=150)

        self.label_SessionVenueFloor = Label(AddFrame, text="Venue Floor*", width=20, font=("bold", 10))
        self.label_SessionVenueFloor.place(x=0, y=175)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenueFloor = Entry(AddFrame)
        self.entry_SessionVenueFloor.place(x=170, y=175)

        self.label_SessionVenueBuilding = Label(AddFrame, text="Venue Building", width=20, font=("bold", 10))
        self.label_SessionVenueBuilding.place(x=0, y=200)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenueBuilding = Entry(AddFrame)
        self.entry_SessionVenueBuilding.place(x=170, y=200)

        self.label_SessionVenueBlock = Label(AddFrame, text="Venue Block", width=20, font=("bold", 10))
        self.label_SessionVenueBlock.place(x=0, y=225)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenueBlock = Entry(AddFrame)
        self.entry_SessionVenueBlock.place(x=170, y=225)

        self.label_SessionVenueStreet = Label(AddFrame, text="Venue Street", width=20, font=("bold", 10))
        self.label_SessionVenueStreet.place(x=0, y=250)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenueStreet = Entry(AddFrame)
        self.entry_SessionVenueStreet.place(x=170, y=250)

        self.label_SessionVenuePostalCode = Label(AddFrame, text="Venue Postal Code*", width=20, font=("bold", 10))
        self.label_SessionVenuePostalCode.place(x=0, y=275)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.entry_SessionVenuePostalCode = Entry(AddFrame)
        self.entry_SessionVenuePostalCode.place(x=170, y=275)

        self.tkvar_Wheelchair = StringVar(self)
        self.tkvar_PriVenue = StringVar(self)
        choices = {'False', 'True'}
        self.tkvar_Wheelchair.set("Select an Option")
        self.tkvar_PriVenue.set("Select an Option")

        self.label_SessionVenuePostalCode = Label(AddFrame, text="Venue Primary Venue", width=20, font=("bold", 10))
        self.label_SessionVenuePostalCode.place(x=0, y=300)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.options_PrimaryVenue = ttk.Combobox(AddFrame, width=17, state="readonly")
        self.options_PrimaryVenue['values'] = ["Select an Option",
                                               "True",
                                               "False"]
        self.options_PrimaryVenue.current(0)
        self.options_PrimaryVenue.place(x=170, y=300)

        self.label_SessionVenuePostalCode = Label(AddFrame, text="Venue Wheelchair Access", width=20, font=("bold", 10))
        self.label_SessionVenuePostalCode.place(x=0, y=325)
        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])
        self.options_Wheelchair = ttk.Combobox(AddFrame, width=17, state="readonly")
        self.options_Wheelchair['values'] = ["Select an Option",
                                             "True",
                                             "False"]
        self.options_Wheelchair.current(0)
        self.options_Wheelchair.place(x=170, y=325)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        addFrame = tk.Frame(self)
        addFrame.place(width=300, height=400, x=100, y=170)
        self.addFrame(addFrame)

        label_1 = Label(self, text="Optional Fields", width=20, font=("bold", 20))
        label_1.place(x=80, y=55)

        label_2 = Label(self, text="Sessions", width=20, font=("bold", 15))
        label_2.place(x=137, y=100)

        def callback():
            print(addCourseRunPageForm.payload)
            # addCourseRunPagePreview.refresh(controller.frames[addCourseRunPagePreview].curlText)
            controller.show_frame(addCourseRunPage4)

        def addCallback():
            payloadToEdit = addCourseRunPageForm.payload
            payloadToEdit = json.loads(payloadToEdit)

            priVenue = self.options_PrimaryVenue.get() if self.options_PrimaryVenue.get() != 'Select an Option' else ''
            wheelChair = self.options_Wheelchair.get() if self.options_Wheelchair.get() != 'Select an Option' else ''
            try:
                sessionList = payloadToEdit["course"]["run"]["sessions"]
            except:
                sessionList = []

            sessionObjectTemplate = {
                "startTime": self.entry_SessionStartDate.get(),
                "endTime": self.entry_SessionEndTime.get(),
                "startDate": self.entry_SessionStartDate.get(),
                "startTime": self.entry_SessionStartTime.get(),
                "modeOfTraining": self.modeOfTraining.get()[0],
                "venue": {
                    "room": self.entry_SessionVenueRoom.get(),
                    "floor": self.entry_SessionVenueFloor.get(),
                    "unit": self.entry_SessionVenueUnit.get(),
                    "postalCode": self.entry_SessionVenuePostalCode.get()
                }
            }
            if self.entry_SessionVenueBlock.get() != '':
                sessionObjectTemplate["venue"]["block"] = self.entry_SessionVenueBlock.get()
            if self.entry_SessionVenueStreet.get() != '':
                sessionObjectTemplate["venue"]["street"] = self.entry_SessionVenueStreet.get()
            if self.entry_SessionVenueBuilding.get() != '':
                sessionObjectTemplate["venue"]["building"] = self.entry_SessionVenueBuilding.get()
            if priVenue != '':
                sessionObjectTemplate["venue"]["primaryVenue"] = True if priVenue == 'True' else False
            if wheelChair != '':
                sessionObjectTemplate["venue"]["wheelChairAccess"] = True if wheelChair == 'True' else False

                # print(payloadToEdit['course']['run']['sessions'])
            sessionList.append(sessionObjectTemplate)
            payloadToEdit['course']['runs'][0]['sessions'] = sessionList
            addCourseRunPageForm.payload = json.dumps(payloadToEdit, indent=4)
            print(addCourseRunPageForm.payload)
            tkinter.messagebox.showinfo(title="Success", message="Session successfully added")
            clearSessionEntryBox()


        def clearSessionEntryBox():
            self.entry_SessionEndDate.delete(0, 'end')
            self.entry_SessionEndTime.delete(0, 'end')
            self.entry_SessionStartDate.delete(0, 'end')
            self.entry_SessionStartTime.delete(0, 'end')
            self.entry_SessionVenueBlock.delete(0, 'end')
            self.entry_SessionVenueBuilding.delete(0, 'end')
            self.entry_SessionVenueFloor.delete(0, 'end')
            self.entry_SessionVenuePostalCode.delete(0, 'end')
            self.entry_SessionVenueRoom.delete(0, 'end')
            self.entry_SessionVenueStreet.delete(0, 'end')
            self.entry_SessionVenueUnit.delete(0, 'end')
            self.modeOfTraining.current(0)
            self.options_Wheelchair.current(0)
            self.options_PrimaryVenue.current(0)

        def backcallback():
            controller.show_frame(addCourseRunPage2)

        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: backcallback()
                               )
        backButton.place(relx=0.055, rely=0.021, anchor=CENTER)
        addButton = tk.Button(self, text="Add", bg="white", width=15, pady=5, command=lambda: addCallback())
        addButton.place(relx=0.3, rely=0.85, anchor=CENTER)
        previewButton = tk.Button(self, text="Next", bg="white", width=15, pady=5, command=lambda: callback())
        previewButton.place(relx=0.7, rely=0.85, anchor=CENTER)


# Page 4 for Add Course Run - Trainers
class addCourseRunPage4(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_1 = Label(self, text="Optional Fields", width=20, font=("bold", 20))
        label_1.place(x=80, y=55)

        label_1 = Label(self, text="Trainers", width=20, font=("bold", 15))
        label_1.place(x=137, y=100)

        self.label_trainerTypeCode = Label(self, text="Trainer Type Code*", width=20, font=("bold", 10))
        self.label_trainerTypeCode.place(x=80, y=140)

        self.index = 0
        self.ssecList = []

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_trainerTypeCode = Entry(self)
        self.entry_trainerTypeCode.place(x=250, y=140)

        self.label_trainerTypeDescription = Label(self, text="Trainer Type Description*", width=20, font=("bold", 10))
        self.label_trainerTypeDescription.place(x=80, y=165)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_trainerTypeDescription = Entry(self)
        self.entry_trainerTypeDescription.place(x=250, y=165)

        self.label_trainerId = Label(self, text="Trainer Id*", width=20, font=("bold", 10))
        self.label_trainerId.place(x=80, y=190)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_trainerId = Entry(self)
        self.entry_trainerId.place(x=250, y=190)

        self.label_trainerName = Label(self, text="Trainer Name", width=20, font=("bold", 10))
        self.label_trainerName.place(x=80, y=215)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_trainerName = Entry(self)
        self.entry_trainerName.place(x=250, y=215)

        self.label_trainerEmail = Label(self, text="Trainer Email", width=20, font=("bold", 10))
        self.label_trainerEmail.place(x=80, y=240)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_trainerEmail = Entry(self)
        self.entry_trainerEmail.place(x=250, y=240)

        self.label_trainerExperience = Label(self, text="Trainer Experience", width=20, font=("bold", 10))
        self.label_trainerExperience.place(x=80, y=265)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_trainerExperience = Entry(self)
        self.entry_trainerExperience.place(x=250, y=265)

        self.label_trainerlinkedInUrl = Label(self, text="Trainer linkedInUrl", width=20, font=("bold", 10))
        self.label_trainerlinkedInUrl.place(x=80, y=290)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_trainerlinkedInUrl = Entry(self)
        self.entry_trainerlinkedInUrl.place(x=250, y=290)

        self.label_trainersalutationId = Label(self, text="Trainer salutationId", width=20, font=("bold", 10))
        self.label_trainersalutationId.place(x=80, y=315)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_trainersalutationId = Entry(self)
        self.entry_trainersalutationId.place(x=250, y=315)

        self.label_trainerdomainAreaOfPractice = Label(self, text="Trainer AreaOfPractice", width=20, font=("bold", 10))
        self.label_trainerdomainAreaOfPractice.place(x=80, y=340)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_trainerdomainAreaOfPractice = Entry(self)
        self.entry_trainerdomainAreaOfPractice.place(x=250, y=340)

        self.label_trainerinTrainingProviderProfile = Label(self, text="inTrainingProviderProfile", width=20,
                                                            font=("bold", 10))
        self.label_trainerinTrainingProviderProfile.place(x=80, y=365)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])


        inTrainingProviderProfile = ttk.Combobox(self, width = 27, state ="readonly")
        inTrainingProviderProfile['values'] = ["Select an Option",
                                               "True",
                                               "False"
                                               ]
        inTrainingProviderProfile.current(0)
        inTrainingProviderProfile.place(x=250, y=365)

        label_1 = Label(self, text="Trainers - SsecEQAs", width=20, font=("bold", 15))
        label_1.place(x=137, y=410)

        self.label_trainerssecEQA = Label(self, text="Trainer ssecEQA", width=20, font=("bold", 10))
        self.label_trainerssecEQA.place(x=80, y=450)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_trainerssecEQA = Entry(self)
        self.entry_trainerssecEQA.place(x=250, y=450)

        self.label_trainerssecEQAdescription = Label(self, text="Trainer description", width=20, font=("bold", 10))
        self.label_trainerssecEQAdescription.place(x=80, y=475)

        # label_CRN_ttp = CreateToolTip(label_courseVac, tooltipDescription["CourseReferenceNumber"])

        self.entry_trainerssecEQAdescription = Entry(self)
        self.entry_trainerssecEQAdescription.place(x=250, y=475)

        addssecEqasButton = tk.Button(self, text="add ssecEQA", bg="white", width=10, pady=5,
                                      command=lambda: addssecCallback()
                                      )
        addssecEqasButton.place(relx=0.5, rely=0.70, anchor=CENTER)

        def addssecCallback():
            payloadToEdit = addCourseRunPageForm.payload
            payloadToEdit = json.loads(payloadToEdit)
            ssecEQAtemplate = {
                "code": self.entry_trainerssecEQA.get(),
                "description": self.entry_trainerssecEQAdescription.get()
            }

            self.ssecList.append(ssecEQAtemplate)
            addCourseRunPageForm.payload = json.dumps(payloadToEdit, indent=4)
            self.entry_trainerssecEQA.delete(0, 'end')
            self.entry_trainerssecEQAdescription.delete(0, 'end')
            print(self.ssecList)

        def callback():
            addCourseRunPageForm.refresh(controller.frames[addCourseRunPageForm].curlText)
            controller.show_frame(addCourseRunPageForm)

        def addCallback():
            payloadToEdit = addCourseRunPageForm.payload
            payloadToEdit = json.loads(payloadToEdit)
            if inTrainingProviderProfile.get() == 'Select an Option':
                result = ''
            else:
                result = inTrainingProviderProfile.get()

            try:
                trainerList = payloadToEdit["course"]['runs'][0]["linkCourseRunTrainer"]
            except:
                trainerList = []

            trainerObjectTemplate = {
                "trainer": {
                    "name": self.entry_trainerName.get(),
                    "email": self.entry_trainerEmail.get(),
                    "indexNumber": self.index,
                    "trainerType": {
                        "code": self.entry_trainerTypeCode.get(),
                        "description": self.entry_trainerTypeDescription.get()
                    }
                }
            }

            if (self.entry_trainerId.get() != ''):
                trainerObjectTemplate["trainer"]["id"] = self.entry_trainerId.get()
            if (self.entry_trainerExperience.get() != ''):
                trainerObjectTemplate["trainer"]["experience"] = self.entry_trainerExperience.get()
            if (self.entry_trainerlinkedInUrl.get() != ''):
                trainerObjectTemplate["trainer"]["linkedInURL"] = self.entry_trainerlinkedInUrl.get()
            if (self.entry_trainerdomainAreaOfPractice.get() != ''):
                trainerObjectTemplate["trainer"]["domainAreaOfPractice"] = self.entry_trainerdomainAreaOfPractice.get()
            if (self.entry_trainersalutationId.get() != ''):
                trainerObjectTemplate["trainer"]["salutationId"] = self.entry_trainersalutationId.get()
            if (result != ''):
                trainerObjectTemplate["trainer"]["inTrainingProviderProfile"] = result
            if (self.ssecList != []):
                trainerObjectTemplate["trainer"]["linkedSsecEQAs"] = self.ssecList

            # print(trainerObjectTemplate)
            trainerList.append(trainerObjectTemplate)
            payloadToEdit['course']['runs'][0]['linkCourseRunTrainer'] = trainerList
            addCourseRunPageForm.payload = json.dumps(payloadToEdit, indent=4)
            print(addCourseRunPageForm.payload)
            tkinter.messagebox.showinfo(title="Success", message="Trainer successfully added")
            self.ssecList = []
            self.index = self.index + 1

        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(addCourseRunPage3)
                               )
        backButton.place(relx=0.055, rely=0.021, anchor=CENTER)
        addButton = tk.Button(self, text="Add", bg="white", width=15, pady=5, command=lambda: addCallback())
        addButton.place(relx=0.3, rely=0.85, anchor=CENTER)
        previewButton = tk.Button(self, text="Next", bg="white", width=15, pady=5, command=lambda: callback())
        previewButton.place(relx=0.7, rely=0.85, anchor=CENTER)