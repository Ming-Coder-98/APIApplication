#Import course Run py Functions
from tkinter import scrolledtext

from requests.api import request
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

        label_1 = Label(self, text="Course Reference Number:", width=20, font=("bold", 10))
        label_1.place(x=80, y=220)

        label_1_ttp = CreateToolTip(label_1, \
        'Internal Course Reference Number is used as a parameter in the POST Request payload \n'
        'Example of Course References Number: TGS-12345678')

        entry_1 = Entry(self)
        entry_1.place(x=250, y=220)

        label_2 = Label(self, text="Course Admin Email:", width=20, font=("bold", 10))
        label_2.place(x=80, y=245)

        label_2_ttp = CreateToolTip(label_2, \
        'Admin Email is used as a parameter in the POST Request payload \n'
        'Example of Admin Email: test@gmail.com')

        entry_2 = Entry(self)
        entry_2.place(x=250, y=245)

        label_3 = Label(self, text="Opening Registration Date:", width=20, font=("bold", 10))
        label_3.place(x=80, y=270)

        label_3_ttp = CreateToolTip(label_3, \
        'Opening Registration Date (YYYYMMDD) is used as a parameter in the POST Request payload \n'
        'Example: 20210617')

        entry_3 = Entry(self)
        entry_3.place(x=250, y=270)

        label_4 = Label(self, text="Closing Registration Date:", width=20, font=("bold", 10))
        label_4.place(x=80, y=295)

        label_4_ttp = CreateToolTip(label_4, \
        'Closing Registration Date (YYYYMMDD) is used as a parameter in the POST Request payload \n'
        'Example: 20210621')

        entry_4 = Entry(self)
        entry_4.place(x=250, y=295)

        label_5 = Label(self, text="Course Start Date:", width=20, font=("bold", 10))
        label_5.place(x=80, y=320)

        label_5_ttp = CreateToolTip(label_5, \
        'Course Start Date(YYYYMMDD) is used as a parameter in the POST Request payload \n'
        'Course Start Date should be later than Opening/Closing Registration Date \n'
        'Example: 20210628')

        entry_5 = Entry(self)
        entry_5.place(x=250, y=320)

        label_6 = Label(self, text="Course End Date:", width=20, font=("bold", 10))
        label_6.place(x=80, y=345)

        label_6_ttp = CreateToolTip(label_6, \
        'Course End Date(YYYYMMDD) is used as a parameter in the POST Request payload \n'
        'Course End Date should be later than Opening/Closing Registration and Course Start Date \n'
        'Example: 20210628')

        entry_6 = Entry(self)
        entry_6.place(x=250, y=345)

        label_7 = Label(self, text="Course Code:", width=20, font=("bold", 10))
        label_7.place(x=80, y=370)

        label_7_ttp = CreateToolTip(label_7, \
        'Course Code is used as a parameter in the POST Request payload \n'
        'Example: 01')

        entry_7 = Entry(self)
        entry_7.place(x=250, y=370)

        label_8 = Label(self, text="Course Description:", width=20, font=("bold", 10))
        label_8.place(x=80, y=395)

        label_8_ttp = CreateToolTip(label_8, \
        'Course Description is used as a parameter in the POST Request payload \n'
        'Example: Course is about...')

        entry_8 = Entry(self)
        entry_8.place(x=250, y=395)

        label_9 = Label(self, text="Mode of Training:", width=20, font=("bold", 10))
        label_9.place(x=80, y=420)

        label_9_ttp = CreateToolTip(label_9, \
        'Mode of Training (Integer) is used as a parameter in the POST Request payload \n'
        'Example: 9')

        entry_9 = Entry(self)
        entry_9.place(x=250, y=420)

        previewButton = tk.Button(self, text="Next", bg="white", width=25, pady=5, command=lambda: controller.show_frame(updateCourseRunPageForm) if self.var.get() == 2 else controller.show_frame(updateCourseRunPageFormFileUpload) )
        previewButton.place(x=250, y=540, anchor=CENTER)

        backButton = tk.Button(self, text="Back", bg="white", width=25, pady=5)
        backButton.place(x=250, y=580, anchor=CENTER)

        def storeAndsave_all():
            # load config File
            configInfo = loadFile("EmptyCourseRunPayLoad.json")
            configInfoJson = json.loads(configInfo)

            configInfoJson["course"]["courseReferenceNumber"] = entry_1.get()
            configInfoJson["course"]["runs"]["courseAdminEmail"] = entry_2.get()
            configInfoJson["course"]["runs"]["registrationDates"]["opening"] = entry_3.get()
            configInfoJson["course"]["runs"]["registrationDates"]["closing"] = entry_4.get()
            configInfoJson["course"]["runs"]["courseDates"]["start"] = entry_5.get()
            configInfoJson["course"]["runs"]["courseDates"]["end"] = entry_6.get()
            configInfoJson["course"]["runs"]["courseVacancy"]["code"] = entry_7.get()
            configInfoJson["course"]["runs"]["courseVacancy"]["description"] = entry_8.get()
            configInfoJson["course"]["runs"]["modeOfTraining"] = entry_9.get()
            # Save config File
            saveJsonFormat(configInfoJson, "EmptyCourseRunPayLoad.json")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  

class updateCourseRunPageForm(tk.Frame):

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
        label_0.place(x=90, y=85)

        # Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        # Configuration for Notebook layout
        tabControl = ttk.Notebook(self)

        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)

        # Adding of tabs
        tabControl.add(tab1, text='Request - Payload')
        tabControl.add(tab2, text='Curl')
        tabControl.add(tab3, text='Reponse')
        tabControl.place(width=440, height=460, x=30, y=222)

        payloadText = scrolledtext.ScrolledText(tab1, width=70, height=30)
        payloadText.insert(tk.END, str(getDeleteCourseRunPayLoad("")))
        payloadText.place(height=405, width=440, y=20)
        payloadText.bind("<Key>", lambda e: "break")

        curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        curlText.place(height=405, width=440, y=20)
        curlText.bind("<Key>", lambda e: "break")

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        responseText.bind("<Key>", lambda e: "break")

        createButton = tk.Button(self, text="Create", bg="white", width=25, pady=5,
                                )
        createButton.place(relx=0.5, rely=0.22, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(updateCourseRunPageSelect)
                               )
        backButton.place(relx=0.055, rely=0.021, anchor=CENTER)
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

        butt_request = Button(tab1, text='Find', command=lambda: find("payload"), highlightthickness=0, bd=0,
                              background="gray")
        butt_request.place(x=380, y=0, height=21, width=60)
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
            elif method == "payload":
                textw = payloadText
            else:
                textw = curlText
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
            filetext = str(payloadText.get("1.0", END)) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")

        # This method activates two other methods.
        # 1) this method calls the delete method in courseRunFunction and return the response
        # 2) Based on the response, if a status 200 is received, it will display the response
        def deleteCallBack(runId):
            resp = deleteCourserun(runId)
            if (resp.status_code < 400):
                messagebox.showinfo("Successful", "Successfully Delete Course Run: " + runId)
            responseText.delete("1.0", "end")
            responseText.insert(tk.END, resp.text)


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
        label_1_ttp = CreateToolTip(label_runId, \
        'The Course Run Id is used to create URL for POST Request Call\n'
        'Example: https://api.ssg-wsg.sg/courses/runs/{runId}')

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