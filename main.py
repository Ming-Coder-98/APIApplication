#Import course Run py Functions
from EnrolmentFunction import addEnrolment, enrollmentInitialization
from courseRunFunctions import *

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
    with open("config.json") as a:
        # Load the json file data into local variable "data"
        data1 = json.load(a)
        return data1

# Open the json file where the "enrolment info" is being stored
with open("EnrolmentPayLoad.json") as b:
    # Load the json file data into local variable "data"
    data2 = json.load(b)
# Store the list of data into local variable enrolmentinfo"
courseEnrolmentInfo = data2["enrolment"]
enrolmentCourseId = courseEnrolmentInfo["course"]["run"]["id"]
enrolmentRefNo = courseEnrolmentInfo["course"]["referenceNumber"]
enrolmentTpUen = courseEnrolmentInfo["trainingPartner"]["uen"]

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

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Starting Page (Press to start the Navigation/ Exit)
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

        button1 = tk.Button(self, text="Press to start the Navigation", bg="white", width=25, pady=5,
                            command=lambda: controller.show_frame(PageOne))  # go to Page One
        button1.place(relx=0.5, rely=0.65, anchor=CENTER)
        button2 = tk.Button(self, text="Exit", bg="white", width=25, pady=5,
                            command=quit_program)  # quit program
        button2.place(relx=0.5, rely=0.7, anchor=CENTER)


# Add course run into API
class PageOne(tk.Frame):

    def __init__(self, parent, controller):

        #load initialization method from courseRunFunctions.py  
        courseRunInitialization()      
        
        tk.Frame.__init__(self, parent)

        self.inner = tk.Frame(self)
        self.inner.place(relx=0.5, rely=0.2, anchor=CENTER)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label1 = tk.Label(self, text="You are about to add a Course Run to the course below: ")
        label1.place(relx=0.5, rely=0.15, anchor=CENTER)
        label2 = tk.Label(self, text="Course Reference Number: " + courseRefNumber)
        label2.place(relx=0.5, rely=0.2, anchor=CENTER)
        label3 = tk.Label(self, text="Training Provider UEN: " + courseTPUEN)
        label3.place(relx=0.5, rely=0.25, anchor=CENTER)
        label4 = tk.Label(self, text="Course Admin Email: " + courseAdminEmail)
        label4.place(relx=0.5, rely=0.3, anchor=CENTER)

        def AddCourse():  
            try:
                addCourserun()
                data1 = load_json_config()
                messagebox.showinfo("Successful", "Status Code: 200 \nAdded Course into API. The Course Run ID is " + str(data1["runId"]))
                print(str(data1["runId"]))
            except:
                data1 = load_json_config()
                messagebox.showerror("Invalid Response", "Status Code: 400 \nCourse Run already exist. The Course Run ID is " + str(data1["runId"]), )
                print(str(data1["runId"]))

        def DownloadFile():
            try:
                df = pd.read_json('/Users/Ming/Documents/APIApplication/CourseRunPayLoad.json')
                df.to_csv(filedialog.asksaveasfilename(defaultextension='.csv'))
                messagebox.showinfo("Successful", "CSV file has been downloaded")
            except:
                print("user didnt save.")

        def ViewCourseRunJsonFile():
            json_filename = 'CourseRunPayLoad.json'
            Interface = Tk()

            with open(json_filename, 'r') as inside:
                data = json.load(inside)

            text = Text(Interface, state='normal', height=20, width=50)
            text.place(x=20, y=40)
            text.insert('1.0', str(data))

            Interface.geometry("450x200")

            Interface.mainloop()

        # When button is pressed, function should be called
        AddButton = tk.Button(self, command=AddCourse, text='Add', width=10, pady=5, bg="white")
        AddButton.place(relx=0.5, rely=0.5, anchor=CENTER)
        BackButton = tk.Button(self, text="Back", width=10, pady=5, bg="white",
                               command=lambda: controller.show_frame(StartPage))
        BackButton.place(relx=0.3, rely=0.5, anchor=CENTER)
        NextButton = tk.Button(self, text="Next", width=10, pady=5, bg="white", command=lambda: controller.show_frame(PageTwo))
        NextButton.place(relx=0.7, rely=0.5, anchor=CENTER)
        ViewButton = tk.Button(self, text="Download course run in CSV", width=22, pady=5, bg="white",
                               command=DownloadFile)
        ViewButton.place(relx=0.5, rely=0.6, anchor=CENTER)
        ViewCourseRunJsonButton = tk.Button(self, text="View course run in json", width=18, pady=5, bg="white",
                               command=ViewCourseRunJsonFile)
        ViewCourseRunJsonButton.place(relx=0.5, rely=0.65, anchor=CENTER)


# Add enrollment into API
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.inner = tk.Frame(self)
        self.inner.place(relx=0.5, rely=0.2, anchor=CENTER)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label1 = tk.Label(self, text="You are about to add an Enrolment")
        label1.place(relx=0.5, rely=0.15, anchor=CENTER)
        label2 = tk.Label(self, text="Enrolment Course Run ID: " + str(enrolmentCourseId))
        label2.place(relx=0.5, rely=0.2, anchor=CENTER)
        label3 = tk.Label(self, text="Enrolment Reference No: " + enrolmentRefNo)
        label3.place(relx=0.5, rely=0.25, anchor=CENTER)
        label4 = tk.Label(self, text="Enrolment TP UEN: " + enrolmentTpUen)
        label4.place(relx=0.5, rely=0.3, anchor=CENTER)


        def AddEnrollment():
            try:
                addEnrolment()
                data1 = load_json_config()
                messagebox.showinfo("Successful", "Status Code: 200 \nAdded Enrolment into API Your Enrolment ID is " +
                                    (data1["enrollRefNum"]))
                print((data1["enrollRefNum"]))
            except:
                data1 = load_json_config()
                messagebox.showerror("Invalid Response",
                                         "Status Code: 400 \nEnrolmentID already exist. The Enrolment ID is " +
                                     (data1["enrollRefNum"]))
                print((data1["enrollRefNum"]))

           

        def DownloadFile():
            try:
                df = pd.read_json('/Users/Ming/Documents/APIApplication/EnrolmentPayload.json')
                df.to_csv(filedialog.asksaveasfilename(defaultextension='.csv'))
                messagebox.showinfo("Successful", "CSV file has been downloaded")
            except:
                print("user didnt save.")

        def ViewEnrolmentJsonFile():
            json_filename = 'EnrolmentPayLoad.json'
            Interface = Tk()

            with open(json_filename, 'r') as inside:
                data = json.load(inside)

            text = Text(Interface, state='normal', height=20, width=50)
            text.place(x=20, y=40)
            text.insert('1.0', str(data))

            Interface.geometry("450x200")

            Interface.mainloop()

            # When button is pressed, function should be called

        AddButton = tk.Button(self, command=AddEnrollment, text='Add', width=10, pady=5, bg="white")
        AddButton.place(relx=0.5, rely=0.5, anchor=CENTER)
        BackButton = tk.Button(self, text="Back", width=10, pady=5, bg="white",
                               command=lambda: controller.show_frame(StartPage))
        BackButton.place(relx=0.3, rely=0.5, anchor=CENTER)
        NextButton = tk.Button(self, text="Next", width=10, pady=5, bg="white",
                               command=lambda: controller.show_frame(PageThree))
        NextButton.place(relx=0.7, rely=0.5, anchor=CENTER)
        ViewButton = tk.Button(self, text="Download Enrolment in CSV", width=22, pady=5, bg="white",
                               command=DownloadFile)
        ViewButton.place(relx=0.5, rely=0.6, anchor=CENTER)
        ViewEnrolmentJsonButton = tk.Button(self, text="View Enrolment in json", width=18, pady=5, bg="white",
                                            command=ViewEnrolmentJsonFile)
        ViewEnrolmentJsonButton.place(relx=0.5, rely=0.65, anchor=CENTER)


# Add attendance into API
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.inner = tk.Frame(self)
        self.inner.place(relx=0.5, rely=0.2, anchor=CENTER)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label2 = tk.Label(self, text="You are about to add an attendance")
        label2.place(relx=0.5, rely=0.15, anchor=CENTER)

        def AddAttendance():
            messagebox.showinfo("Successful", "Added Attendance into API")

        def DownloadFile():
            messagebox.showinfo("Successful", "CSV file has been downloaded")

        # When button is pressed, function is called
        AddButton = tk.Button(self, command=AddAttendance, text='Add', width=10, pady=5, bg="white")
        AddButton.place(relx=0.5, rely=0.5, anchor=CENTER)
        BackButton = tk.Button(self, text="Back", width=10, pady=5, bg="white",
                               command=lambda: controller.show_frame(StartPage))
        BackButton.place(relx=0.3, rely=0.5, anchor=CENTER)
        NextButton = tk.Button(self, text="Next", width=10, pady=5, bg="white", command=lambda: controller.show_frame(PageFour))
        NextButton.place(relx=0.7, rely=0.5, anchor=CENTER)
        ViewButton = tk.Button(self, text="View attendance in CSV", width=18, pady=5, bg="white",
                               command=DownloadFile)
        ViewButton.place(relx=0.5, rely=0.6, anchor=CENTER)


# Add assessment into API
class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.inner = tk.Frame(self)
        self.inner.place(relx=0.5, rely=0.2, anchor=CENTER)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label2 = tk.Label(self, text="You are about to add an assessment")
        label2.place(relx=0.5, rely=0.15, anchor=CENTER)

        def AddAssessment():
            messagebox.showinfo("Successful", "Added Assessment into API")

        def DownloadFile():
            messagebox.showinfo("Successful", "CSV file has been downloaded")

        # When button is pressed, function is called
        AddButton = tk.Button(self, command=AddAssessment, text='Add', width=10, pady=5, bg="white")
        AddButton.place(relx=0.5, rely=0.5, anchor=CENTER)
        BackButton = tk.Button(self, text="Back", width=10, pady=5, bg="white",
                               command=lambda: controller.show_frame(StartPage))
        BackButton.place(relx=0.3, rely=0.5, anchor=CENTER)
        NextButton = tk.Button(self, text="Next", width=10, pady=5, bg="white", command=lambda: controller.show_frame(PageTwo))
        NextButton.place(relx=0.7, rely=0.5, anchor=CENTER)
        ViewButton = tk.Button(self, text="View assessment in CSV", width=18, pady=5, bg="white",
                               command=DownloadFile)
        ViewButton.place(relx=0.5, rely=0.6, anchor=CENTER)



app = APIProject()
app.geometry("500x747")
app.mainloop()