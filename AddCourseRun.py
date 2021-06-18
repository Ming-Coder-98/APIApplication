#Import course Run py Functions
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

        label_2 = Label(self, text="Course Session Start Date:", width=20, font=("bold", 10))
        label_2.place(x=80, y=135)

        label_2_ttp = CreateToolTip(label_2,
        'Start Date (YYYYMMDD) can be used as a parameter in the POST Request payload \n'
        'Example: 20210616')

        entry_2 = Entry(self)
        entry_2.place(x=250, y=135)

        label_3 = Label(self, text="Course Session Start Time:", width=20, font=("bold", 10))
        label_3.place(x=80, y=160)

        label_3_ttp = CreateToolTip(label_3,'Start time (HH:MM) can be used as a parameter in the POST Request payload \n'
                                    'Example: 17:30')

        entry_3 = Entry(self)
        entry_3.place(x=250, y=160)

        label_4 = Label(self, text="Course Session End Date:", width=20, font=("bold", 10))
        label_4.place(x=80, y=185)

        label_4_ttp = CreateToolTip(label_4,'End Date (YYYYMMDD) can be used as a parameter in the POST Request payload \n'
                                    'Example: 20210621')

        entry_4 = Entry(self)
        entry_4.place(x=250, y=185)

        label_5 = Label(self, text="Course Session End Time:", width=20, font=("bold", 10))
        label_5.place(x=80, y=210)

        label_5_ttp = CreateToolTip(label_5, \
                                    'End time (HH:MM) can be used as a parameter in the POST Request payload \n'
                                    'Example: 18:30')

        entry_5 = Entry(self)
        entry_5.place(x=250, y=210)

        label_6 = Label(self, text="Mode of Training:", width=20, font=("bold", 10))
        label_6.place(x=80, y=235)

        label_6_ttp = CreateToolTip(label_6,
                                    'Mode of Training is used as a parameter in the POST Request payload \n'
                                    'Example: 9')

        entry_6 = Entry(self)
        entry_6.place(x=250, y=235)

        label_7 = Label(self, text="Trainers", width=20, font=("bold", 15))
        label_7.place(x=137, y=270)

        label_8 = Label(self, text="Trainer name:", width=20, font=("bold", 10))
        label_8.place(x=80, y=305)

        label_8_ttp = CreateToolTip(label_8, \
                                    'Name of the trainer can be used as a parameter in the POST Request payload \n'
                                    'Example: John')

        entry_8 = Entry(self)
        entry_8.place(x=250, y=305)

        label_9 = Label(self, text="Trainer Email:", width=20, font=("bold", 10))
        label_9.place(x=80, y=330)

        label_9_ttp = CreateToolTip(label_9, \
                                    'Email of trainner canbe used as a parameter in the POST Request payload \n'
                                  'Example: tester@gmail.com')

        entry_9 = Entry(self)
        entry_9.place(x=250, y=330)

        label_10 = Label(self, text="Trainer Code:", width=20, font=("bold", 10))
        label_10.place(x=80, y=355)

        label_10_ttp = CreateToolTip(label_10, \
                                     'Code of Trainer can be used as a parameter in the POST Request payload \n'
                                     '1 - Existing, 2 - New \n'
                                     'Example: 1')

        entry_10 = Entry(self)
        entry_10.place(x=250, y=355)

        label_11 = Label(self, text="Trainer description:", width=20, font=("bold", 10))
        label_11.place(x=80, y=380)

        label_11_ttp = CreateToolTip(label_11, \
                                     'Simple description of trainer can be used as a parameter in the POST Request payload \n'
                                     'Example: New Trainer')

        entry_11 = Entry(self)
        entry_11.place(x=250, y=380)

        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(addCourseRunPageSelect)
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


class addCourseRunPageSelect(tk.Frame):
    def __init__(self, parent, controller):
        print("addCourseRun Init")
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
        'Mode of Training is used as a parameter in the POST Request payload \n'
        'Example: 9')

        entry_9 = Entry(self)
        entry_9.place(x=250, y=420)

        label_10 = Label(self, text="Course Run Room:", width=20, font=("bold", 10))
        label_10.place(x=80, y=445)

        label_10_ttp = CreateToolTip(label_10, \
        'Course Run Room Number  is used as a parameter in the POST Request payload \n'
        'Example: 9')

        entry_10 = Entry(self)
        entry_10.place(x=250, y=445)

        label_11 = Label(self, text="Course Run Room Floor:", width=20, font=("bold", 10))
        label_11.place(x=80, y=470)

        label_11_ttp = CreateToolTip(label_11, \
        'The level of the Course Run room is used as a parameter in the POST Request payload \n'
        'Example: 9')

        entry_11 = Entry(self)
        entry_11.place(x=250, y=470)

        label_12 = Label(self, text="Course run Room Unit:", width=20, font=("bold", 10))
        label_12.place(x=80, y=495)

        label_12_ttp = CreateToolTip(label_12, \
        'The unit of the Course Run room is used as a parameter in the POST Request payload \n'
        'Example: 12')

        entry_12 = Entry(self)
        entry_12.place(x=250, y=495)

        label_13 = Label(self, text="Course run Postal Code:", width=20, font=("bold", 10))
        label_13.place(x=80, y=495)

        label_13_ttp = CreateToolTip(label_13, \
        'The postal code of the Course Run Venue is used as a parameter in the POST Request payload \n'
        'Example: 12345')

        entry_13 = Entry(self)
        entry_13.place(x=250, y=495)

        previewButton = tk.Button(self, text="Next", bg="white", width=25, pady=5, command=lambda: controller.show_frame(addCourseRunPageOptional) if self.var.get() == 2 else controller.show_frame(addCourseRunPageFormFileUpload) )
        previewButton.place(x=250, y=540, anchor=CENTER)

        # This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value

        def typing(event):
            storeAndsave_all()

        entry_1.bind('<KeyRelease>', typing)
        entry_2.bind('<KeyRelease>', typing)
        entry_3.bind('<KeyRelease>', typing)
        entry_4.bind('<KeyRelease>', typing)
        entry_5.bind('<KeyRelease>', typing)
        entry_6.bind('<KeyRelease>', typing)
        entry_7.bind('<KeyRelease>', typing)
        entry_8.bind('<KeyRelease>', typing)
        entry_9.bind('<KeyRelease>', typing)

        def storeAndsave_all():
            # load config File
            configInfo = loadFile("EmptyCourseRunPayLoad.json")
            configInfoJson = json.loads(configInfo)

            configInfoJson["course"]["courseReferenceNumber"] = entry_1.get()
            configInfoJson["course"]["runs"][0]["courseAdminEmail"] = entry_2.get()
            configInfoJson["course"]["runs"][0]["registrationDates"]["opening"] = int(entry_3.get()) if entry_3.get()!="" else 0
            configInfoJson["course"]["runs"][0]["registrationDates"]["closing"] = int(entry_4.get()) if entry_4.get()!="" else 0
            configInfoJson["course"]["runs"][0]["courseDates"]["start"] = int(entry_5.get()) if entry_5.get()!="" else 0
            configInfoJson["course"]["runs"][0]["courseDates"]["end"] = int(entry_6.get()) if entry_6.get()!="" else 0
            configInfoJson["course"]["runs"][0]["courseVacancy"]["code"] = entry_7.get()
            configInfoJson["course"]["runs"][0]["courseVacancy"]["description"] = entry_8.get()
            configInfoJson["course"]["runs"][0]["modeOfTraining"] = entry_9.get()
            configInfoJson["course"]["runs"][0]["venue"]["room"] = entry_10.get()
            configInfoJson["course"]["runs"][0]["venue"]["floor"] = entry_11.get()
            configInfoJson["course"]["runs"][0]["venue"]["unit"] = entry_12.get()
            configInfoJson["course"]["runs"][0]["venue"]["postalCode"] = entry_13.get()

            saveJsonFormat(configInfoJson,"CompletedCourseRunPayload.json")



    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  

class addCourseRunPageForm(tk.Frame):
    def refresh(text):
        configInfo = loadFile("CompletedCourseRunPayLoad.json")
        text.delete("1.0","end")
        text.insert(tk.END, configInfo)

    def __init__(self, parent, controller):

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

        configInfo = loadFile("CompletedCourseRunPayLoad.json")
        self.curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        self.curlText.insert(tk.END, str(curlPostRequest("", str(configInfo))))
        self.curlText.place(height=405, width=440, y=20)
        self.curlText.bind("<Key>", lambda e: "break")

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        # responseText.bind("<Key>", lambda e: "break")

        def submitCallBack():
            responseText.delete("1.0","end") 
            configInfo = loadFile("CompletedCourseRunPayLoad.json")
            resp = createCourserun(configInfo)
            print(resp.status_code)
            textPayload = StringVar(self, value = resp.text) 
            responseText.insert(INSERT, textPayload.get())
            
        submitButton = tk.Button(self, text="Create", bg="white", width=25, pady=5, command=lambda: submitCallBack())
        submitButton.place(relx=0.5, rely=0.25, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(addCourseRunPageSelect),
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
                               command=lambda: controller.show_frame(addCourseRunPageSelect)
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
            
