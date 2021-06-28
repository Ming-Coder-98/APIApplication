import json
import tkinter
import tkinter as tk
from tkinter import Button, Entry, IntVar, Label, Radiobutton, StringVar, filedialog, messagebox, scrolledtext, ttk
from tkinter.constants import CENTER, END, INSERT

import pandas as pd
from PIL import Image, ImageTk

from EnrolmentFunction import curlPostRequestUpdateEnrolmentFee, getUpdateEnrolmentFeePayLoad, updateEnrolmentFee, \
    curlRequestSearchEnrolment, searchEnrolment, displayPostRequestEnrolment
from courseRunFunctions import (createCourserun, curlPostRequest)
from HttpRequestFunction import loadFile
from tooltip import CreateToolTip

from tkinter import Button, Entry, IntVar, Label, Radiobutton, StringVar,scrolledtext,filedialog, ttk, messagebox
import tkinter as tk
from tkinter.constants import CENTER, DISABLED, END, INSERT
from tooltip import CreateToolTip
from PIL import ImageTk, Image
import json

#Load Tooltip Json object as ttDescription
with open("TooltipDescription.json") as f:
    tooltipDescription = json.load(f)

with open("config.json") as file:
    config = json.load(file)


# Frame for Page 1 - Add Course Run
class searchEnrolmentPage1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Search Enrolment", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        label_filterTitle = Label(self, text="Filter Details:", width=20, font=("bold", 15))
        label_filterTitle.place(x=137, y=100)

        label_updateFromDate = Label(self, text="Last Update Dates From*", width=20, font=("bold", 10))
        label_updateFromDate.place(x=80, y=135)

        #label_openRegDate_ttp = CreateToolTip(label_openRegDate, tooltipDescription["CourseRegistrationDateOpen"])

        entry_updateFromDate = Entry(self)
        entry_updateFromDate.place(x=250, y=135)

        label_updateToDate = Label(self, text="Last Update Dates To*", width=20, font=("bold", 10))
        label_updateToDate.place(x=80, y=160)

        #label_closeRegDate_ttp = CreateToolTip(label_closeRegDate, tooltipDescription["CourseRegistrationDateClose"])

        entry_updateToDate = Entry(self)
        entry_updateToDate.place(x=250, y=160)

        label_sortTitle = Label(self, text="Sort by Details:", width=20, font=("bold", 15))
        label_sortTitle.place(x=137, y=190)

        label_field = Label(self, text="Field", width=20, font=("bold", 10))
        label_field.place(x=80, y=225)

        #label_CourseModeOfTraining_ttp = CreateToolTip(label_CourseModeOfTraining, tooltipDescription["ModeOfTraining"])

        field = ttk.Combobox(self, width=27, state="readonly")
        field['values'] = ["Select an Option",
                           "updatedOn",
                           "createdOn"]
        field.current(0)
        field.place(x=250, y=225)

        label_order = Label(self, text="Order", width=20, font=("bold", 10))
        label_order.place(x=80, y=250)

        #label_CourseModeOfTraining_ttp = CreateToolTip(label_CourseModeOfTraining, tooltipDescription["ModeOfTraining"])

        order = ttk.Combobox(self, width=27, state="readonly")
        order['values'] = ["Select an Option",
                           "asc",
                           "desc"]
        order.current(0)
        order.place(x=250, y=250)

        label_sortTitle = Label(self, text="Enrolment Details:", width=20, font=("bold", 15))
        label_sortTitle.place(x=137, y=280)


        label_runId = Label(self, text="Course Run Id*", width=20, font=("bold", 10))
        label_runId.place(x=80, y=315)

        #label_runId_ttp = CreateToolTip(self.label_runId, tooltipDescription["CourseRunId"])

        entry_runId = Entry(self)
        entry_runId.place(x=250, y=315)

        label_CRN = Label(self, text="Course Reference Number*", width=20, font=("bold", 10))
        label_CRN.place(x=80, y=340)

        label_CRN_ttp = CreateToolTip(label_CRN, tooltipDescription["CourseReferenceNumber"])

        entry_CRN = Entry(self)
        entry_CRN.place(x=250, y=340)

        label_status = Label(self, text="Enrolment Status", width=20, font=("bold", 10))
        label_status.place(x=80, y=365)

        #label_CourseModeOfTraining_ttp = CreateToolTip(label_CourseModeOfTraining, tooltipDescription["ModeOfTraining"])

        status = ttk.Combobox(self, width=27, state="readonly")
        status['values'] = ["Select an Option",
                            "Confirmed",
                           "Cancelled"]
        status.current(0)
        status.place(x=250, y=365)

        label_traineeId = Label(self, text="Trainee Id", width=20, font=("bold", 10))
        label_traineeId.place(x=80, y=390)

        #label_runId_ttp = CreateToolTip(self.label_runId, tooltipDescription["CourseRunId"])

        entry_traineeId = Entry(self)
        entry_traineeId.place(x=250, y=390)


        label_statusCollection = Label(self, text="Fee Status Collection*", width=20, font=("bold", 10))
        label_statusCollection.place(x=80, y=415)

        # label_statusCollection_ttp = CreateToolTip(label_statusCollection, tooltipDescription["CourseVacCode"])

        statusCollection = ttk.Combobox(self, width=27, state="readonly")
        statusCollection['values'] = ["Select an Option",
                                      "Full Payment",
                                           "Pending Payment",
                                           "Partial Payment",
                                           "Cancelled"
                                           ]
        statusCollection.current(0)
        statusCollection.place(x=250, y=415)

        label_idType = Label(self, text="ID Type", width=20, font=("bold", 10))
        label_idType.place(x=80, y=440)

        #label_CourseModeOfTraining_ttp = CreateToolTip(label_CourseModeOfTraining, tooltipDescription["ModeOfTraining"])

        idType = ttk.Combobox(self, width=27, state="readonly")
        idType['values'] = ["Select an Option",
                            "NRIC",
                           "FIN",
                            "Others"]
        idType.current(0)
        idType.place(x=250, y=440)

        label_employerUEN = Label(self, text="Employer UEN", width=20, font=("bold", 10))
        label_employerUEN.place(x=80, y=465)

        #label_runId_ttp = CreateToolTip(self.label_runId, tooltipDescription["CourseRunId"])

        entry_employerUEN = Entry(self)
        entry_employerUEN.place(x=250, y=465)

        label_enrolmentDate = Label(self, text="Enrolment Date", width=20, font=("bold", 10))
        label_enrolmentDate.place(x=80, y=490)

        #label_closeRegDate_ttp = CreateToolTip(label_closeRegDate, tooltipDescription["CourseRegistrationDateClose"])

        entry_enrolmentDate = Entry(self)
        entry_enrolmentDate.place(x=250, y=490)


        label_sponsorshipType = Label(self, text="Sponsorship Type", width=20, font=("bold", 10))
        label_sponsorshipType.place(x=80, y=515)

        #label_CourseModeOfTraining_ttp = CreateToolTip(label_CourseModeOfTraining, tooltipDescription["ModeOfTraining"])

        sponsorshipType = ttk.Combobox(self, width=27, state="readonly")
        sponsorshipType['values'] = ["Select an Option",
                                     "EMPLOYER",
                                     "INDIVIDUAL"
                                     ]
        sponsorshipType.current(0)
        sponsorshipType.place(x=250, y=515)

        label_TpUEN = Label(self, text="Training Partner - UEN", width=20, font=("bold", 10))
        label_TpUEN.place(x=80, y=540)

        label_UEN_ttp = CreateToolTip(label_TpUEN, tooltipDescription["UEN"])
        uenReadOnly = StringVar()
        uenReadOnly.set(config["UEN"])
        entry_TpUEN = Entry(self, state=DISABLED, textvariable=uenReadOnly)
        entry_TpUEN.place(x=250, y=542)

        label_tpCode = Label(self, text="TP Code", width=20, font=("bold", 10))
        label_tpCode.place(x=80, y=565)

        #label_runId_ttp = CreateToolTip(self.label_runId, tooltipDescription["CourseRunId"])

        entry_tpCode = Entry(self)
        entry_tpCode.place(x=250, y=565)

        previewButton = tk.Button(self, text="Next", bg="white", width=25, pady=5,
                                  command= lambda: NextCallBack())
        previewButton.place(x=250, y=610, anchor=CENTER)

        def NextCallBack():
            searchEnrolmentPage2.payload = StoreAndSave()
            searchEnrolmentPage2.refresh(controller.frames[searchEnrolmentPage2].curlText)
            controller.show_frame(searchEnrolmentPage2)

        def StoreAndSave():
            try:
                payload = json.loads(searchEnrolmentPage2.payload)
            except:
                payload = {}

            if field.get()  != 'Select an Option' or order.get() != 'Select an Option':
                payload['sortBy'] = {}
                if field.get() != 'Select an Option':
                    payload['sortBy']['field']= field.get()
                if order.get() != 'Select an Option':
                    payload['sortBy']['order'] = (order.get())

            if entry_updateFromDate.get() != '' or entry_updateToDate.get() != '':
                payload['meta'] = {}
                if entry_updateFromDate.get() != '':
                    payload['meta']['lastUpdateDateFrom']= entry_updateFromDate.get()
                if entry_updateToDate.get() != '':
                    payload['meta']['lastUpdateDateTo'] = entry_updateToDate.get()

            if entry_CRN.get() or entry_runId.get() or entry_traineeId or entry_employerUEN or entry_enrolmentDate or entry_tpCode!= '':
                payload['enrolment'] = {}
                if entry_runId.get() != '':
                    payload['enrolment']['course'] = {}
                    payload['enrolment']['course']['run'] = {}
                    payload['enrolment']['course']['run']['id']= entry_runId.get()
                if entry_CRN.get() != '':
                    payload['enrolment']['course'] = {}
                    payload['enrolment']['course']['referenceNumber'] = entry_CRN.get()
                if entry_traineeId.get() != '':
                    payload['enrolment']['trainee'] = {}
                    payload['enrolment']['trainee']['id'] = entry_traineeId.get()
                if entry_employerUEN.get() != '':
                    payload['enrolment']['employer'] = {}
                    payload['enrolment']['employer']['uen'] = entry_employerUEN.get()
                if entry_enrolmentDate.get() != '':
                    payload['enrolment']['enrolmentDate'] = entry_enrolmentDate.get()
                if entry_TpUEN.get() != '':
                    payload['enrolment']['trainingPartner'] = {}
                    payload['enrolment']['trainingPartner']['uen'] = entry_TpUEN.get()
                if entry_tpCode.get() != '':
                    payload['enrolment']['trainingPartner']['code'] = entry_tpCode.get()
                if status.get() != 'Select an Option':
                    payload['enrolment']['status']= status.get()
                if statusCollection.get() != 'Select an Option':
                    payload['enrolment']['fee'] = {}
                    payload['enrolment']['fee']['feeCollectionStatus'] = statusCollection.get()
                if idType.get() != 'Select an Option':
                    payload['enrolment']['idType'] = {}
                    payload['enrolment']['idType']['type'] = idType.get()
                if sponsorshipType.get() != 'Select an Option':
                    payload['enrolment']['sponsorshipType'] = sponsorshipType.get()






            print(json.dumps(payload, indent=4))
            return str(json.dumps(payload, indent=4))

        # Initialies the file and object first in order to prevent clearing of data
        # addCourseRunPagePreview.payload = loadFile("EmptyaddCourseRunPayLoad.json")
        #addCourseRunPageForm.payload = "{}"

        #def previewCallBack():
            #addCourseRunPageForm.payload = storeAndsave_all()
            #print(addCourseRunPageForm.payload)
            #controller.show_frame(addCourseRunPage2)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Search Enrolment Page
class searchEnrolmentPage2(tk.Frame):

    def refresh(controllerCurlText):
        controllerCurlText.delete("1.0","end")
        controllerCurlText.insert(tk.END, str(curlRequestSearchEnrolment(searchEnrolmentPage2.payload)))

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        #Variable
        self.payload = '{}'
        self.textPayload = ''
        self.contentInfo = ''

        # Title
        label_0 = Label(self, text="Search Enrolment", width=20, font=("bold", 20))
        label_0.place(x=90, y=50)

        label_page = Label(self, text="Number of Pages", width=20, font=("bold", 10))
        label_page.place(x=100, y=95)

        #label_runId_ttp = CreateToolTip(self.label_runId, tooltipDescription["CourseRunId"])

        entry_page = Entry(self)
        entry_page.place(x=250, y=95)

        label_pageSize = Label(self, text="Page Sizes", width=20, font=("bold", 10))
        label_pageSize.place(x=100, y=120)

        #label_runId_ttp = CreateToolTip(self.label_runId, tooltipDescription["CourseRunId"])

        entry_pageSize = Entry(self)
        entry_pageSize.place(x=250, y=120)


        # This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing():
            searchEnrolmentPage2.payload = storeAndSave()
            value = curlRequestSearchEnrolment(searchEnrolmentPage2.payload)
            self.curlText.delete("1.0", "end")
            self.curlText.insert(tk.END, value)

        entry_page.bind('<KeyRelease>', lambda a: typing())
        entry_pageSize.bind('<KeyRelease>', lambda a: typing())

        def storeAndSave():
            temp = searchEnrolmentPage2.payload
            print(temp)
            temp = json.loads(temp)
            if entry_page.get()!= '' or entry_pageSize.get() != '':
                temp['parameters'] = {}
                temp['parameters']['page'] = entry_page.get()
                temp['parameters']['pageSize'] = entry_pageSize.get()

            print(json.dumps(temp, indent=4))
            return str(json.dumps(temp, indent=4))




        # Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        # Configuration for Notebook layout
        tabControl = ttk.Notebook(self)

        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)

        # Adding of tabs
        tabControl.add(tab2, text='Request')
        tabControl.add(tab3, text='Response')
        tabControl.place(width=440, height=460, x=30, y=222)

        self.curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        self.curlText.insert(tk.END,
                        str(curlRequestSearchEnrolment("")))
        self.curlText.place(height=405, width=440, y=20)
        self.curlText.bind("<Key>", lambda e: "break")

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        responseText.bind("<Key>", lambda e: "break")

        submitButton = tk.Button(self, text="Search", bg="white", width=25, pady=5,
                                 command=lambda: searchEnrolmentCallBack(searchEnrolmentPage2.payload))
        submitButton.place(relx=0.5, rely=0.22, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=25, pady=5,
                                 command=lambda:controller.show_frame(searchEnrolmentPage1))
        backButton.place(relx=0.5, rely=0.27, anchor=CENTER)
        exportButton1 = tk.Button(self, text="Export Payload", bg="white", width=15, pady=5,
                                  command=lambda: downloadFile("payload"))
        exportButton1.place(relx=0.3, rely=0.95, anchor=CENTER)
        exportButton2 = tk.Button(self, text="Export Response", bg="white", width=15, pady=5,
                                  command=lambda: downloadFile("response"))
        exportButton2.place(relx=0.7, rely=0.95, anchor=CENTER)

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

        def downloadFile(method):
            files = [('JSON', '*.json'),
                     ('Text Document', '*.txt')]
            file = filedialog.asksaveasfile(filetypes=files, defaultextension='.json')
            filetext = str(searchEnrolmentPage2.payload) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")

        # This method activates two other methods.
        # 1) this method calls the delete method in courseRunFunction and return the response
        # 2) Based on the response, if a status 200 is received, it will display the response
        def searchEnrolmentCallBack(searchEnrolmentPayload):
            resp = searchEnrolment(searchEnrolmentPayload)
            responseText.delete("1.0", "end")
            responseText.insert(tk.END, resp)
            tabControl.select(tab3)
