#Import course Run py Functions
from configWindow import setConfigWindow, showConfigWindow
from AssessmentFunction import addAssessment
from EnrolmentFunction import addEnrolment, enrollmentInitialization
from AttendanceFunction import uploadAttendance
from courseRunFunctions import *

from HttpRequestFunction import loadFile, saveJsonFormat
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
        for F in (StartPage, viewCourseRunPage, deleteCourseRunPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        #Menubar
        menubar = Menu(self, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')  
        
        config = Menu(menubar, tearoff=0)  
        config.add_command(label="Set Configuration", command=lambda:setConfigWindow(self))
        config.add_command(label="Show Configuration", command=lambda:showConfigWindow(self))
        menubar.add_cascade(label="Setting", menu=config)

        courseMenu = Menu(menubar, tearoff=0)  
        courseMenu.add_command(label="View Course Run",command=lambda: self.show_frame(viewCourseRunPage))
        courseMenu.add_command(label="Add Course Run")  
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

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Starting Page (Press to start the Navigation/ Exit)
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

        entry_1 = Entry(self)
        entry_1.place(x=240, y=130)

        def courseRunViewer():
            courseRunID = entry_1.get()
            if (courseRunID != ""):
                # Call a Get HTTP to see if runId exists
                print("Searching Course Run Id: " + str(courseRunID))
                resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(courseRunID))
                print(resp.status_code)
                # Deletion
                if (resp.status_code < 400):
                    print(resp.json)
                else:
                    print("Run ID Does not exist ")

        submitButton = tk.Button(self, text="Submit", bg="white", width=25, pady=5,
                            command=lambda: courseRunViewer())
        submitButton.place(relx=0.5, rely=0.25, anchor=CENTER)
        exportButton = tk.Button(self, text="Export as JSON File", bg="white", width=25, pady=5,
                            command=lambda: controller.show_frame(StartPage))
        exportButton.place(relx=0.5, rely=0.3, anchor=CENTER)


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

        label_0 = Label(self, text="Delete Course Run", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        label_1 = Label(self, text="Course Run ID", width=20, font=("bold", 10))
        label_1.place(x=80, y=130)

        entry_1 = Entry(self)
        entry_1.place(x=240, y=130)

        tabControl = ttk.Notebook(self)
  
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        #500 x 747
        tabControl.add(tab1, text ='Payload')
        tabControl.add(tab2, text ='Reponse')
        tabControl.place(width= 400, height= 450, x = 50, y = 222)
        
        ttk.Label(tab1, 
                text ="Welcome to \
                GeeksForGeeks").grid(column = 0, 
                                    row = 0,
                                    padx = 30,
                                    pady = 30)  
        ttk.Label(tab2,
                text ="Lets dive into the\
                world of computers").grid(column = 0,
                                            row = 0, 
                                            padx = 30,
                                            pady = 30)

        submitButton = tk.Button(self, text="Delete", bg="white", width=25, pady=5)
        submitButton.place(relx=0.5, rely=0.25, anchor=CENTER)
        exportButton = tk.Button(self, text="Export as JSON File", bg="white", width=25, pady=5, command=controller.show_frame(StartPage))
        exportButton.place(relx=0.5, rely=0.95, anchor=CENTER)

        def show_frame(self, new_frame_class):
            if self.current_frame:
                self.current_frame.destroy()

            self.current_frame = new_frame_class(self.container, controller=self)
            self.current_frame.pack(fill="both", expand=True)


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