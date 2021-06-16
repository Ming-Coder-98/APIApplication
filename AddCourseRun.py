#Import course Run py Functions
from configWindow import setConfigWindow, showConfigWindow
from AssessmentFunction import addAssessment
from EnrolmentFunction import addEnrolment, enrollmentInitialization
from AttendanceFunction import uploadAttendance
from courseRunFunctions import deleteCourserun, getdeleteCourseRunPayLoad, updateEmptyDeleteCourseRunPayLoad
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

class addCourseRunPageSelect(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Add Course Run (Select Option)", width=30, font=("bold", 20))
        label_0.place(x=5, y=53)

        nextButton = tk.Button(self, text="Next", bg="white", width=25, pady=5,
                               command =lambda: controller.show_frame(addCourseRunPage))
        nextButton.place(relx=0.5, rely=0.25, anchor=CENTER)


class addCourseRunPage(tk.Frame):

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

        label_1 = Label(self, text="Course Run Reference Number:", width=30, font=("bold", 10))
        label_1.place(x=25, y=130)

        entry_1 = Entry(self)
        entry_1.place(x=250, y=130)

        nextButton = tk.Button(self, text="Next", bg="white", width=25, pady=5,
                               command =lambda: controller.show_frame(addCourseRunPageTwo))
        nextButton.place(relx=0.5, rely=0.25, anchor=CENTER)


class addCourseRunPageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Add Course Run(2)", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        label_1 = Label(self, text="Sequence Number:", width=30, font=("bold", 10))
        label_1.place(x=25, y=105)

        entry_1 = Entry(self)
        entry_1.place(x=250, y=105)

        label_1 = Label(self, text="Course Admin Email:", width=30, font=("bold", 10))
        label_1.place(x=25, y=130)

        entry_1 = Entry(self)
        entry_1.place(x=250, y=130)

        label_2 = Label(self, text="Opening Registration Date:", width=30, font=("bold", 10))
        label_2.place(x=25, y=155)

        entry_2 = Entry(self)
        entry_2.place(x=250, y=155)

        label_3 = Label(self, text="Closing Registration Date:", width=30, font=("bold", 10))
        label_3.place(x=25, y=180)

        entry_3 = Entry(self)
        entry_3.place(x=250, y=180)

        label_4 = Label(self, text="Course Start Date:", width=30, font=("bold", 10))
        label_4.place(x=25, y=205)

        entry_4 = Entry(self)
        entry_4.place(x=250, y=205)

        label_5 = Label(self, text="Course End Date:", width=30, font=("bold", 10))
        label_5.place(x=25, y=230)

        entry_5 = Entry(self)
        entry_5.place(x=250, y=230)

        label_6 = Label(self, text="Course Code:", width=30, font=("bold", 10))
        label_6.place(x=25, y=255)

        entry_6 = Entry(self)
        entry_6.place(x=250, y=255)

        label_7 = Label(self, text="Course Description:", width=30, font=("bold", 10))
        label_7.place(x=25, y=280)

        entry_7 = Entry(self)
        entry_7.place(x=250, y=280)

        label_8 = Label(self, text="Course Description:", width=30, font=("bold", 10))
        label_8.place(x=25, y=280)

        entry_8 = Entry(self)
        entry_8.place(x=250, y=280)

        label_9 = Label(self, text="Mode of Training:", width=30, font=("bold", 10))
        label_9.place(x=25, y=305)

        entry_9 = Entry(self)
        entry_9.place(x=250, y=305)

        def storeAndsave_all():
            # load config File
            configInfo = loadFile("EmptyCourseRunPayLoad.json")
            configInfoJson = json.loads(configInfo)

            configInfoJson["course"]["runs"]["sequenceNumber"] = entry_1.get()
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

        nextButton = tk.Button(self, text="Next", bg="white", width=25, pady=5,
                               command =lambda: controller.show_frame(addCourseRunPageThree))
        nextButton.place(relx=0.5, rely=0.65, anchor=CENTER)

class addCourseRunPageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Add Course Run(3)", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)


        nextButton = tk.Button(self, text="Next", bg="white", width=25, pady=5,
                               command =lambda: controller.show_frame(addCourseRunPageFour))
        nextButton.place(relx=0.5, rely=0.25, anchor=CENTER)


class addCourseRunPageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Add Course Run(4)", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)


        createButton = tk.Button(self, text="Next", bg="white", width=25, pady=5,
                               command =lambda: controller.show_frame(addCourseRunPagePreview))
        createButton.place(relx=0.5, rely=0.25, anchor=CENTER)

class addCourseRunPagePreview(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Add Course Run(Preview)", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)


        nextButton = tk.Button(self, text="Next", bg="white", width=25, pady=5,
                               command =lambda: controller.show_frame(addCourseRunPageTwo))
        nextButton.place(relx=0.5, rely=0.25, anchor=CENTER)
