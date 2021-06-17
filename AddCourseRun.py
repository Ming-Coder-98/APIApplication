#Import course Run py Functions
from configWindow import setConfigWindow, showConfigWindow
from AssessmentFunction import addAssessment
from EnrolmentFunction import addEnrolment, enrollmentInitialization
from AttendanceFunction import uploadAttendance
from courseRunFunctions import deleteCourserun, updateEmptyDeleteCourseRunPayLoad
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

from tooltip import CreateToolTip

class addCourseRunPageForm(tk.Frame):
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



class addCourseRunPageSelect(tk.Frame):
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
        Radiobutton(self, text="Upload a Course Run JSON File", variable=self.var, value="1",command=lambda: controller.show_frame(addCourseRunPageForm)).place(x=158,y=100)
        Radiobutton(self, text="Fill in the basic mandate form", variable=self.var, value="2").place(x=158,y=130)
        self.selection = tk.StringVar()
        self.selection.set("2")

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

        previewButton = tk.Button(self, text="Preview", bg="white", width=25, pady=5)
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



