#Import course Run py Functions
from CourseSession import getCourseSessionPage
from UpdateCourseRun import updateCourseRunPageFormFileUpload, updateCourseRunPagePage2, updateCourseRunPagePage3, updateCourseRunPagePage4, updateCourseRunPagePreview, updateCourseRunPageSelect
from tooltip import CreateToolTip
from configWindow import setConfigWindow, showConfigWindow
from AssessmentFunction import addAssessment
from EnrolmentFunction import addEnrolment, enrollmentInitialization
from AttendanceFunction import uploadAttendance
from courseRunFunctions import curlGetRequestViewCourseRun, curlPostRequest, deleteCourserun, getCourseRun, getDeleteCourseRunPayLoad
from AddCourseRun import addCourseRunPageForm, addCourseRunPageFormFileUpload, addCourseRunPage1, addCourseRunPage2, addCourseRunPage3, addCourseRunPage4

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



#Load Tooltip Json object as ttDescription
with open("TooltipDescription.json") as f:
    ttDescription = json.load(f)


# Quit Program
def quit_program():
    quit()



class APIProject(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, *kwargs)
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        

        self.frames = {}
        for F in (getCourseSessionPage, updateCourseRunPagePreview,updateCourseRunPagePage2,updateCourseRunPagePage3,updateCourseRunPagePage4,updateCourseRunPageFormFileUpload, updateCourseRunPageSelect, addCourseRunPageFormFileUpload,addCourseRunPageForm,addCourseRunPage4,addCourseRunPage3,addCourseRunPage2, addCourseRunPage1, viewCourseRunPage, deleteCourseRunPage, StartPage):
            frame = F(self.container, self)

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
        courseMenu.add_command(label="Add Course Run",command=lambda:self.show_frame(addCourseRunPage1))
        courseMenu.add_command(label="Delete Course Run",command=lambda: self.show_frame(deleteCourseRunPage)) 
        courseMenu.add_command(label="Update Course Run",command=lambda: self.show_frame(updateCourseRunPageSelect))  
        courseMenu.add_command(label="Course Session",command=lambda: self.show_frame(getCourseSessionPage))   
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

        def recreateFrame(classObject):
            frame = classObject(self.container, self)
            self.frames[classObject] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        def reInitialiseFrame(FrameName):
            recreateFrame(FrameName)
            self.show_frame(FrameName)
            

    
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

        label_1 = Label(self, text="Course Run ID", width=20, font=("bold", 10), anchor='w')
        label_1.place(x=105, y=130)
        label_1_ttp = CreateToolTip(label_1, ttDescription["CourseRunId"])
        entry_1 = Entry(self)
        entry_1.place(x=275, y=130)
        #This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing(event):
            value = curlGetRequestViewCourseRun(entry_1.get())
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

        tabControl.add(curlFrame, text ='Request')
        tabControl.add(responseFrame, text ='Reponse')

        tabControl.place(width= 440, height= 460, x = 30, y = 222)

        #Textbox for response Frame
        responseText = scrolledtext.ScrolledText(responseFrame,width=70,height=30)
        responseText.place(height = 405, width = 440,y=20)
        responseText.bind("<Key>", lambda e: "break")

        #Textbox for Curl Frame
        curlText = scrolledtext.ScrolledText(curlFrame,width=70,height=30)
        curlText.insert(tk.END, str(curlGetRequestViewCourseRun("")))
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

        
        # This call back method activates two other methods.
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
        label_1 = Label(self, text="Course Run ID ", width=20, font=("bold", 10), anchor='w')
        label_1.place(x=105, y=100)

        entry_1 = Entry(self)
        entry_1.place(x=275, y=100)
        label_1_ttp = CreateToolTip(label_1, ttDescription["CourseRunId"])

        #Course Ref Number
        label_CRN = Label(self, text="Course Reference Number", width=20, font=("bold", 10), anchor='w')
        label_CRN.place(x=105, y=130)

        entry_CRN = Entry(self)
        entry_CRN.place(x=275, y=130)

        label_CRN_ttp = CreateToolTip(label_CRN, ttDescription["CourseReferenceNumber"])

        #This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing():
            value = curlPostRequest(entry_1.get(),getDeleteCourseRunPayLoad(entry_CRN.get()))
            curlText.delete("1.0","end")
            curlText.insert(tk.END, value)
            
        entry_CRN.bind('<KeyRelease>', lambda a:typing())
        entry_1.bind('<KeyRelease>', lambda b:typing())

        #Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        #Configuration for Notebook layout
        tabControl = ttk.Notebook(self)
  
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        
        #Adding of tabs
        tabControl.add(tab2, text ='Request')
        tabControl.add(tab3, text ='Reponse')
        tabControl.place(width= 440, height= 460, x = 30, y = 222)

        curlText = scrolledtext.ScrolledText(tab2,width=70,height=30)
        curlText.insert(tk.END, str(curlPostRequest("",getDeleteCourseRunPayLoad(entry_CRN.get()))))
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

        def downloadFile(method):
            files = [('JSON', '*.json'), 
                     ('Text Document', '*.txt')]
            file = filedialog.asksaveasfile(filetypes = files, defaultextension='.json')
            filetext = str(getDeleteCourseRunPayLoad(entry_CRN.get())) if method == "payload" else str(responseText.get("1.0",END))
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

app = APIProject()
app.geometry("500x747")
app.resizable(0,0)
app.mainloop()