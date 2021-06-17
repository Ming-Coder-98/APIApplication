#Import course Run py Functions
from tooltip import CreateToolTip
from configWindow import setConfigWindow, showConfigWindow
from AssessmentFunction import addAssessment
from EnrolmentFunction import addEnrolment, enrollmentInitialization
from AttendanceFunction import uploadAttendance
from courseRunFunctions import curlGetRequest, curlPostRequest, deleteCourserun, getCourseRun, updateEmptyDeleteCourseRunPayLoad
from AddCourseRun import addCourseRunPageSelect

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
import pyjsonviewer
from tkinter import scrolledtext

# Open the json file where the "courserun info" is being stored
with open("CourseRunPayLoad.json") as f:
    # Load the json file data into local variable "data"
    data = json.load(f)
# Store the list of data into local variable "courseTPinfo & courseRuninfo"
courseTPinfo = data["course"]
courseRuninfo = data["course"]["runs"]
courseTPUEN = courseTPinfo["trainingProvider"]["uen"]
courseRefNumber = courseTPinfo["courseReferenceNumber"]
courseAdminEmail = courseRuninfo[0]["courseAdminEmail"]

def load_json_config():
    # Open the json file where the "config info" is being stored
    with open("config.json") as f:
        # Load the json file data into local variable "data"
        data = json.load(f)
        return data
    
def load_json_demoConfig():
    # Open the json file where the "config info" is being stored
    with open("demoConfig.json") as f:
        # Load the json file data into local variable "data"
        data = json.load(f)
        return data

# Open the json file where the "enrolment info" is being stored
with open("EnrolmentPayLoad.json") as f:
    # Load the json file data into local variable "data"
    data2 = json.load(f)
# Store the list of data into local variable enrolmentinfo"
courseEnrolmentInfo = data2["enrolment"]
enrolmentCourseId = courseEnrolmentInfo["course"]["run"]["id"]
enrolmentRefNo = courseEnrolmentInfo["course"]["referenceNumber"]
enrolmentTpUen = courseEnrolmentInfo["trainingPartner"]["uen"]

# Open the json file where the "attendance info" is being stored
with open("AttendancePayLoad.json") as f:
    # Load the json file data into local variable "data"
    attendanceData = json.load(f)
# Store the list of data into local variable enrolmentinfo"
attendanceSessionId = attendanceData["course"]["sessionID"]
attendanceRefNo = attendanceData["course"]["referenceNumber"]
attendanceTpUen = attendanceData["uen"]

# Open the json file where the "Assessment info" is being stored
with open("AssessmentPayLoad.json") as f:
    # Load the json file data into local variable "data"
    assessmentData = json.load(f)
# Store the list of data into local variable enrolmentinfo"
assessmentRunId = assessmentData["assessment"]["course"]["run"]["id"]
assessmentRefNo = assessmentData["assessment"]["course"]["referenceNumber"]
assessmentTpUen = assessmentData["assessment"]["trainingPartner"]["uen"]


# Quit Program
def quit_program():
    quit()



class APIProject(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, *kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        

        self.frames = {}
        for F in (addCourseRunPageSelect, viewCourseRunPage, deleteCourseRunPage, StartPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        #Menubar
        menubar = Menu(self, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')  
        
        config = Menu(menubar, tearoff=0)  
        config.add_command(label="Set Configuration", command=lambda:setConfigCallback())
        config.add_command(label="Show Configuration", command=lambda:showConfigWindow(self))
        menubar.add_cascade(label="Setting", menu=config)

        courseMenu = Menu(menubar, tearoff=0)  
        courseMenu.add_command(label="View Course Run",command=lambda: self.show_frame(viewCourseRunPage))
        courseMenu.add_command(label="Add Course Run",command=lambda:self.show_frame(addCourseRunPageSelect))
        courseMenu.add_command(label="Delete Course Run",command=lambda: self.show_frame(deleteCourseRunPage)) 
        courseMenu.add_command(label="Update Course Run")  
        menubar.add_cascade(label="Course", menu=courseMenu)  

        
        enrolmentMenu = Menu(menubar, tearoff=0)  
        enrolmentMenu.add_command(label="Create Enrolment")
        enrolmentMenu.add_command(label="Update/Cancel Enrolment")  
        enrolmentMenu.add_command(label="Search Enrolment")  
        enrolmentMenu.add_command(label="View Enrolment")  
        enrolmentMenu.add_command(label="Update Enrolment Fee Collection")  
        menubar.add_cascade(label="Enrolment", menu=enrolmentMenu)  

        
        attendanceMenu = Menu(menubar, tearoff=0)  
        attendanceMenu.add_command(label="Course Session Attendance")
        attendanceMenu.add_command(label="Upload Course Session Attendance")   
        menubar.add_cascade(label="Attendance", menu=attendanceMenu)  

        
        assessmentMenu = Menu(menubar, tearoff=0)  
        assessmentMenu.add_command(label="Create Assessment")
        assessmentMenu.add_command(label="Update/Void Assessment")  
        assessmentMenu.add_command(label="Search Assessment")  
        assessmentMenu.add_command(label="View Assessment")  
        menubar.add_cascade(label="Assessment", menu=assessmentMenu)  
            
        self.config(menu=menubar)

        #This method "blank" out the menubar to prevent duplicate opening of window for Setting 
        def setConfigCallback():
            top2 = setConfigWindow(self)
            top2.transient(self)
            top2.grab_set()
            self.wait_window(top2)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()   

# ViewCourseRun Page
# 2 options for the user to choose from

class viewCourseRunPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="View Course Run", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        label_1 = Label(self, text="Course Run ID", width=20, font=("bold", 10))
        label_1.place(x=80, y=130)
        label_1_ttp = CreateToolTip(label_1, \
        'The Course Run Id is used as a URL for GET Request Call\n'
        'Example: https://api.ssg-wsg.sg/courses/runs/{runId}')
        entry_1 = Entry(self)
        entry_1.place(x=240, y=130)
        #This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing(event):
            value = curlGetRequest(entry_1.get())
            curlText.delete("1.0","end")
            curlText.insert(tk.END, value)

        entry_1.bind('<KeyRelease>',typing)

        #Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        #Configuration for Notebook layout
        tabControl = ttk.Notebook(self)
  
        responseFrame = ttk.Frame(tabControl)
        curlFrame = ttk.Frame(tabControl)

        tabControl.add(curlFrame, text ='Curl')
        tabControl.add(responseFrame, text ='Reponse')

        tabControl.place(width= 440, height= 460, x = 30, y = 222)

        #Textbox for response Frame
        responseText = scrolledtext.ScrolledText(responseFrame,width=70,height=30)
        responseText.place(height = 405, width = 440,y=20)
        responseText.bind("<Key>", lambda e: "break")

        #Textbox for Curl Frame
        curlText = scrolledtext.ScrolledText(curlFrame,width=70,height=30)
        curlText.insert(tk.END, str(curlGetRequest("")))
        curlText.place(height = 405, width = 440, y=20)
        curlText.bind("<Key>", lambda e: "break")

        #adding of single line text box
        edit = Entry(self, background="light gray") 

        #positioning of text box
        edit.place(x = 285, height= 21, y=244) 

        #setting focus
        edit.focus_set()

        butt = Button(responseFrame, text='Find', command=lambda:find("resp"), highlightthickness = 0, bd = 0, background="gray")  
        butt.place(x = 380, y=0, height=21, width=60) 
        butt_curl = Button(curlFrame, text='Find', command=lambda:find("curl"), highlightthickness = 0, bd = 0, background="gray")  
        butt_curl.place(x = 380, y=0, height=21, width=60) 
        


        submitButton = tk.Button(self, text="Submit", bg="white", width=25, pady=5,
                            command=lambda: submitCallBack())
        submitButton.place(relx=0.5, rely=0.25, anchor=CENTER)
        exportButton = tk.Button(self, text="Export Response", bg="white", width=25, pady=5, command = lambda: downloadFile())
        exportButton.place(relx=0.5, rely=0.95, anchor=CENTER)

        
        # This method activates two other methods.
        # 1) this method calls the get method in courseRunFunction and return the response
        # 2) Based on the response, if a status 200 is received, it will display the response    
        def submitCallBack():
            responseText.delete("1.0","end") 
            courseRunID = entry_1.get()
            resp = getCourseRun(courseRunID)
            print(resp.status_code)
            textPayload = StringVar(self, value = resp.text) 
            responseText.insert(INSERT, textPayload.get())
        def downloadFile():
            files = [('JSON', '*.json'), 
                     ('Text Document', '*.txt')]
            file = filedialog.asksaveasfile(filetypes = files, defaultextension='.json')
            filetext = str(responseText.get("1.0",END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")

        #This method is used to search the response text and highlight the searched word in red
        def find(method):
            if method == "resp":
                textw = responseText
            else:
                textw = curlText
            #remove tag 'found' from index 1 to END
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

    def show_frame(self, new_frame_class):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = new_frame_class(self.container, controller=self)
        self.current_frame.pack(fill="both", expand=True)

#Delete Course Run Page
class deleteCourseRunPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        
        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)
        
        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)
        
        #Title
        label_0 = Label(self, text="Delete Course Run", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        #Course Run Id
        label_1 = Label(self, text="Course Run ID: ", width=20, font=("bold", 10), anchor='w')
        label_1.place(x=80, y=100)

        entry_1 = Entry(self)
        entry_1.place(x=240, y=100)
        label_1_ttp = CreateToolTip(label_1, \
        'The Course Run Id is used to create URL for POST Request Call\n'
        'Example: https://api.ssg-wsg.sg/courses/runs/{runId}')

        #Course Ref Number
        label_CRN = Label(self, text="Course Reference Number", width=20, font=("bold", 10), anchor='w')
        label_CRN.place(x=80, y=130)

        entry_CRN = Entry(self)
        entry_CRN.place(x=240, y=130)

        label_CRN_ttp = CreateToolTip(label_CRN, \
        'Internal Course Reference Number is used as a parameter in the POST Request payload \n'
        'Example of Course References Number: TGS-12345678')

        #This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing(type):
            if type == "CRN":
                value = updateEmptyDeleteCourseRunPayLoad(entry_CRN.get())
                payloadText.delete("1.0","end")
                payloadText.insert(tk.END, value)

            value = curlPostRequest(entry_1.get(),entry_CRN.get())
            curlText.delete("1.0","end")
            curlText.insert(tk.END, value)
            
        entry_CRN.bind('<KeyRelease>', lambda a:typing("CRN"))
        entry_1.bind('<KeyRelease>', lambda b:typing("runId"))

        #Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        #Configuration for Notebook layout
        tabControl = ttk.Notebook(self)
  
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        
        #Adding of tabs
        tabControl.add(tab1, text ='Request - Payload')
        tabControl.add(tab2, text ='Curl')
        tabControl.add(tab3, text ='Reponse')
        tabControl.place(width= 440, height= 460, x = 30, y = 222)

        payloadText = scrolledtext.ScrolledText(tab1,width=70,height=30)
        payloadText.insert(tk.END, str(updateEmptyDeleteCourseRunPayLoad("")))
        payloadText.place(height = 405, width = 440, y=20)
        payloadText.bind("<Key>", lambda e: "break")

        curlText = scrolledtext.ScrolledText(tab2,width=70,height=30)
        curlText.insert(tk.END, str(curlPostRequest("","")))
        curlText.place(height = 405, width = 440, y=20)
        curlText.bind("<Key>", lambda e: "break")
        
        responseText = scrolledtext.ScrolledText(tab3,width=70,height=30)
        responseText.place(height = 405, width = 440, y=20)
        responseText.bind("<Key>", lambda e: "break")

        submitButton = tk.Button(self, text="Delete", bg="white", width=25, pady=5, command=lambda: deleteCallBack(entry_1.get()))
        submitButton.place(relx=0.5, rely=0.25, anchor=CENTER)
        exportButton1 = tk.Button(self, text="Export Payload", bg="white", width=15, pady=5, command = lambda: downloadFile("payload"))
        exportButton1.place(relx=0.3, rely=0.95, anchor=CENTER)
        exportButton2 = tk.Button(self, text="Export Response", bg="white", width=15, pady=5,command = lambda: downloadFile("response"))
        exportButton2.place(relx=0.7, rely=0.95, anchor=CENTER)
        
        #adding of single line text box
        edit = Entry(self, background="light gray") 

        #positioning of text box
        edit.place(x = 285, height= 21, y=244) 

        #setting focus
        edit.focus_set()

        butt_request = Button(tab1, text='Find', command=lambda:find("payload"), highlightthickness = 0, bd = 0, background="gray")  
        butt_request.place(x = 380, y=0, height=21, width=60) 
        butt_resp = Button(tab2, text='Find', command=lambda:find("curl"), highlightthickness = 0, bd = 0, background="gray")  
        butt_resp.place(x = 380, y=0, height=21, width=60) 
        butt_resp = Button(tab3, text='Find', command=lambda:find("resp"), highlightthickness = 0, bd = 0, background="gray")  
        butt_resp.place(x = 380, y=0, height=21, width=60) 

        #This method is used to search the response text and highlight the searched word in red
        def find(method):
            if method == "resp":
                textw = responseText
            elif method == "payload":
                textw = payloadText
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

        def downloadFile(method):
            files = [('JSON', '*.json'), 
                     ('Text Document', '*.txt')]
            file = filedialog.asksaveasfile(filetypes = files, defaultextension='.json')
            filetext = str(payloadText.get("1.0",END)) if method == "payload" else str(responseText.get("1.0",END))
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
            responseText.delete("1.0","end")
            responseText.insert(tk.END, resp.text)
                

# Starting Page (Welcome Page)
# 2 options for the user to choose from
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFMenuPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        # button1 = tk.Button(self, text="Press to start the Navigation", bg="white", width=25, pady=5,
        #                     command=lambda: controller.show_frame(PageOne))  # go to Page One
        # button1.place(relx=0.5, rely=0.65, anchor=CENTER)
        button2 = tk.Button(self, text="Exit", bg="white", width=25, pady=5,
                            command=quit_program)  # quit program
        button2.place(relx=0.5, rely=0.7, anchor=CENTER)

    def show_frame(self, new_frame_class):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = new_frame_class(self.container, controller=self)
        self.current_frame.pack(fill="both", expand=True)


# 

app = APIProject()
app.geometry("500x747")
app.resizable(0,0)
app.mainloop()

# Add course run into API
# class PageOne(tk.Frame):

#     def __init__(self, parent, controller):

#         #load initialization method from courseRunFunctions.py  
#         courseRunInitialization()      
        
#         tk.Frame.__init__(self, parent)

#         self.inner = tk.Frame(self)
#         self.inner.place(relx=0.5, rely=0.2, anchor=CENTER)

#         load = Image.open("SKFCoursePage.JPG")
#         render = ImageTk.PhotoImage(load)

#         # labels can be text or images
#         img2 = Label(self, image=render)
#         img2.image = render
#         img2.place(x=0, y=0, relwidth=1, relheight=1)

#         label1 = tk.Label(self, text="You are about to add a Course Run to the course below: ")
#         label1.place(relx=0.5, rely=0.15, anchor=CENTER)
#         label2 = tk.Label(self, text="Course Reference Number: " + courseRefNumber)
#         label2.place(relx=0.5, rely=0.2, anchor=CENTER)
#         label3 = tk.Label(self, text="Training Provider UEN: " + courseTPUEN)
#         label3.place(relx=0.5, rely=0.25, anchor=CENTER)
#         label4 = tk.Label(self, text="Course Admin Email: " + courseAdminEmail)
#         label4.place(relx=0.5, rely=0.3, anchor=CENTER)

#         def AddCourse():  
#             try:
#                 addCourserun()
#                 data = load_json_config()
#                 messagebox.showinfo("Successful", "Status Code: 200 \nAdded Course into API. The Course Run ID is " + str(data["runId"]))
#                 print(str(data["runId"]))
#             except:
#                 data = load_json_config()
#                 messagebox.showerror("Invalid Response", "Status Code: 400 \nCourse Run already exist. The Course Run ID is " + str(data["runId"]), )
#                 print(str(data["runId"]))

#         def DownloadFile():
#             try:
#                 df = pd.read_json('C:/Users/User/Desktop/application/APIApplication/CourseRunPayLoad.json')
#                 df.to_csv(filedialog.asksaveasfilename(defaultextension='.csv'))
#                 messagebox.showinfo("Successful", "CSV file has been downloaded")
#             except:
#                 print("user didnt save.")

#         def ViewCourseRunJsonFile():
#                 pyjsonviewer.view_data(json_file="C:/Users/User/Desktop/application/APIApplication/CourseRunPayLoad.json")

#         # When button is pressed, function should be called
#         AddButton = tk.Button(self, command=AddCourse, text='Add', width=10, pady=5, bg="white")
#         AddButton.place(relx=0.5, rely=0.5, anchor=CENTER)
#         BackButton = tk.Button(self, text="Back", width=10, pady=5, bg="white",
#                                command=lambda: controller.show_frame(StartPage))
#         BackButton.place(relx=0.3, rely=0.5, anchor=CENTER)
#         NextButton = tk.Button(self, text="Next", width=10, pady=5, bg="white", command=lambda: controller.show_frame(PageTwo))
#         NextButton.place(relx=0.7, rely=0.5, anchor=CENTER)
#         ViewButton = tk.Button(self, text="Download course run in CSV", width=22, pady=5, bg="white",
#                                command=DownloadFile)
#         ViewButton.place(relx=0.5, rely=0.6, anchor=CENTER)
#         ViewCourseRunJsonButton = tk.Button(self, text="View course run in json", width=18, pady=5, bg="white",
#                                command=ViewCourseRunJsonFile)
#         ViewCourseRunJsonButton.place(relx=0.5, rely=0.65, anchor=CENTER)


# # Add enrollment into API
# class PageTwo(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

#         self.inner = tk.Frame(self)
#         self.inner.place(relx=0.5, rely=0.2, anchor=CENTER)

#         load = Image.open("SKFEnrolmentPage.JPG")
#         render = ImageTk.PhotoImage(load)

#         # labels can be text or images
#         img2 = Label(self, image=render)
#         img2.image = render
#         img2.place(x=0, y=0, relwidth=1, relheight=1)

#         label1 = tk.Label(self, text="You are about to add an Enrolment")
#         label1.place(relx=0.5, rely=0.15, anchor=CENTER)
#         label2 = tk.Label(self, text="Enrolment Course Run ID: " + str(enrolmentCourseId))
#         label2.place(relx=0.5, rely=0.2, anchor=CENTER)
#         label3 = tk.Label(self, text="Enrolment Reference No: " + enrolmentRefNo)
#         label3.place(relx=0.5, rely=0.25, anchor=CENTER)
#         label4 = tk.Label(self, text="Enrolment TP UEN: " + enrolmentTpUen)
#         label4.place(relx=0.5, rely=0.3, anchor=CENTER)


#         def AddEnrollment():
#             try:
#                 addEnrolment()
#                 data = load_json_demoConfig()
#                 messagebox.showinfo("Successful", "Status Code: 200 \nAdded Enrolment into API Your Enrolment ID is " +
#                                     (data["enrollRefNum"]))
#                 print((data["enrollRefNum"]))
#             except:
#                 data = load_json_demoConfig()
#                 messagebox.showerror("Invalid Response",
#                                          "Status Code: 400 \nEnrolmentID already exist. The Enrolment ID is " +
#                                      (data["enrollRefNum"]))
#                 print((data["enrollRefNum"]))

           

#         def DownloadFile():
#             try:
#                 df = pd.read_json('C:/Users/User/Desktop/application/APIApplication/EnrolmentPayload.json')
#                 df.to_csv(filedialog.asksaveasfilename(defaultextension='.csv'))
#                 messagebox.showinfo("Successful", "CSV file has been downloaded")
#             except:
#                 print("user didnt save.")

#         def ViewEnrolmentJsonFile():
#             pyjsonviewer.view_data(json_file="C:/Users/User/Desktop/application/APIApplication/EnrolmentPayload.json")

#             # When button is pressed, function should be called

#         AddButton = tk.Button(self, command=AddEnrollment, text='Add', width=10, pady=5, bg="white")
#         AddButton.place(relx=0.5, rely=0.5, anchor=CENTER)
#         BackButton = tk.Button(self, text="Back", width=10, pady=5, bg="white",
#                                command=lambda: controller.show_frame(StartPage))
#         BackButton.place(relx=0.3, rely=0.5, anchor=CENTER)
#         NextButton = tk.Button(self, text="Next", width=10, pady=5, bg="white",
#                                command=lambda: controller.show_frame(PageThree))
#         NextButton.place(relx=0.7, rely=0.5, anchor=CENTER)
#         ViewButton = tk.Button(self, text="Download Enrolment in CSV", width=22, pady=5, bg="white",
#                                command=DownloadFile)
#         ViewButton.place(relx=0.5, rely=0.6, anchor=CENTER)
#         ViewEnrolmentJsonButton = tk.Button(self, text="View Enrolment in json", width=18, pady=5, bg="white",
#                                             command=ViewEnrolmentJsonFile)
#         ViewEnrolmentJsonButton.place(relx=0.5, rely=0.65, anchor=CENTER)


# # Add attendance into API
# class PageThree(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

#         self.inner = tk.Frame(self)
#         self.inner.place(relx=0.5, rely=0.2, anchor=CENTER)

#         load = Image.open("SKFAttendancePage.JPG")
#         render = ImageTk.PhotoImage(load)

#         # labels can be text or images
#         img2 = Label(self, image=render)
#         img2.image = render
#         img2.place(x=0, y=0, relwidth=1, relheight=1)

#         label1 = tk.Label(self, text="You are about to add an Attendance")
#         label1.place(relx=0.5, rely=0.15, anchor=CENTER)
#         label2 = tk.Label(self, text="Attendance Course Session ID: " + attendanceSessionId)
#         label2.place(relx=0.5, rely=0.2, anchor=CENTER)
#         label3 = tk.Label(self, text="Attendance Course Reference No: " + attendanceRefNo)
#         label3.place(relx=0.5, rely=0.25, anchor=CENTER)
#         label4 = tk.Label(self, text="Attendance TP UEN: " + attendanceTpUen)
#         label4.place(relx=0.5, rely=0.3, anchor=CENTER)

#         def AddAttendance():
#             try:
#                 uploadAttendance()
#                 messagebox.showinfo("Successful", "Status Code: 200 \nAdded Attendance into API")
#             except:
#                 messagebox.showerror("Invalid Response",
#                                          "Status Code: 400 \nAttendance already taken.")

#         def DownloadFile():
#             try:
#                 df = pd.read_json('C:/Users/User/Desktop/application/APIApplication/AttendancePayload.json')
#                 df.to_csv(filedialog.asksaveasfilename(defaultextension='.csv'))
#                 messagebox.showinfo("Successful", "CSV file has been downloaded")
#             except:
#                 print("user didnt save.")

#         def ViewAttendanceJsonFile():
#             pyjsonviewer.view_data(json_file="C:/Users/User/Desktop/application/APIApplication/AttendancePayload.json")

#             # When button is pressed, function should be called

#         AddButton = tk.Button(self, command=AddAttendance, text='Add', width=10, pady=5, bg="white")
#         AddButton.place(relx=0.5, rely=0.5, anchor=CENTER)
#         BackButton = tk.Button(self, text="Back", width=10, pady=5, bg="white",
#                                command=lambda: controller.show_frame(StartPage))
#         BackButton.place(relx=0.3, rely=0.5, anchor=CENTER)
#         NextButton = tk.Button(self, text="Next", width=10, pady=5, bg="white",
#                                command=lambda: controller.show_frame(PageFour))
#         NextButton.place(relx=0.7, rely=0.5, anchor=CENTER)
#         ViewButton = tk.Button(self, text="Download Attendance in CSV", width=22, pady=5, bg="white",
#                                command=DownloadFile)
#         ViewButton.place(relx=0.5, rely=0.6, anchor=CENTER)
#         ViewAttendanceJsonButton = tk.Button(self, text="View Attendance in json", width=18, pady=5, bg="white",
#                                             command=ViewAttendanceJsonFile)
#         ViewAttendanceJsonButton.place(relx=0.5, rely=0.65, anchor=CENTER)


# # Add assessment into API
# class PageFour(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

#         self.inner = tk.Frame(self)
#         self.inner.place(relx=0.5, rely=0.2, anchor=CENTER)

#         load = Image.open("SKFAssessmentPage.JPG")
#         render = ImageTk.PhotoImage(load)

#         # labels can be text or images
#         img2 = Label(self, image=render)
#         img2.image = render
#         img2.place(x=0, y=0, relwidth=1, relheight=1)

#         label1 = tk.Label(self, text="You are about to add an Assessment")
#         label1.place(relx=0.5, rely=0.15, anchor=CENTER)
#         label2 = tk.Label(self, text="Assessment Course Run ID: " + assessmentRunId)
#         label2.place(relx=0.5, rely=0.2, anchor=CENTER)
#         label3 = tk.Label(self, text="Assessment Course Reference No: " + assessmentRefNo)
#         label3.place(relx=0.5, rely=0.25, anchor=CENTER)
#         label4 = tk.Label(self, text="Assessment TP UEN: " + assessmentTpUen)
#         label4.place(relx=0.5, rely=0.3, anchor=CENTER)


#         def AddAssessment():
#             try:
#                 addAssessment()
#                 data = load_json_demoConfig()
#                 messagebox.showinfo("Successful", "Status Code: 200 \nAdded Assessment into API Your Assessment Reference Number is ")
#                 (data["AssessmentRefNum"])
#             except:
#                 data = load_json_demoConfig()
#                 messagebox.showerror("Invalid Response",
#                                          "Status Code: 400 \nAssessment already exist.")

#         def DownloadFile():
#             try:
#                 df = pd.read_json('C:/Users/User/Desktop/application/APIApplication/AssessmentPayload.json')
#                 df.to_csv(filedialog.asksaveasfilename(defaultextension='.csv'))
#                 messagebox.showinfo("Successful", "CSV file has been downloaded")
#             except:
#                 print("user didnt save.")

#         def ViewAssessmentJsonFile():
#             pyjsonviewer.view_data(json_file="C:/Users/User/Desktop/application/APIApplication/AssessmentPayload.json")

#             # When button is pressed, function should be called

#         AddButton = tk.Button(self, command=AddAssessment, text='Add', width=10, pady=5, bg="white")
#         AddButton.place(relx=0.5, rely=0.5, anchor=CENTER)
#         BackButton = tk.Button(self, text="Back", width=10, pady=5, bg="white",
#                                command=lambda: controller.show_frame(StartPage))
#         BackButton.place(relx=0.3, rely=0.5, anchor=CENTER)
#         NextButton = tk.Button(self, text="Next", width=10, pady=5, bg="white",
#                                command=lambda: controller.show_frame(FinalPage))
#         NextButton.place(relx=0.7, rely=0.5, anchor=CENTER)
#         ViewButton = tk.Button(self, text="Download Assessment in CSV", width=22, pady=5, bg="white",
#                                command=DownloadFile)
#         ViewButton.place(relx=0.5, rely=0.6, anchor=CENTER)
#         ViewAssessmentJsonButton = tk.Button(self, text="View Assessment in json", width=18, pady=5, bg="white",
#                                             command=ViewAssessmentJsonFile)
#         ViewAssessmentJsonButton.place(relx=0.5, rely=0.65, anchor=CENTER)

# class FinalPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

#         load = Image.open("SKFFinalPage.JPG")
#         render = ImageTk.PhotoImage(load)

#         # labels can be text or images
#         img2 = Label(self, image=render)
#         img2.image = render
#         img2.place(x=0, y=0, relwidth=1, relheight=1)

#         BackButton = tk.Button(self, text="Back", width=10, pady=5, bg="white",
#                                command=lambda: controller.show_frame(StartPage))
#         BackButton.place(relx=0.5, rely=0.55, anchor=CENTER)
#         button1 = tk.Button(self, text="Press to Exit App", bg="white", width=20, pady=5,
#                             command=quit_program)  # quit program
#         button1.place(relx=0.5, rely=0.6, anchor=CENTER)