#Import course Run py Functions
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
        initialization()      
        
        tk.Frame.__init__(self, parent)

        self.inner = tk.Frame(self)
        self.inner.place(relx=0.5, rely=0.2, anchor=CENTER)

        load = Image.open("SKFBGPage.JPG")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label2 = tk.Label(self, text="You are about to add a course run")
        label2.place(relx=0.5, rely=0.15, anchor=CENTER)

        def AddCourse():  
            try:
                response = postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs", loadPayload("CourseRunPayLoad.json"))
                saveContent(response,  "config.json")
                messagebox.showinfo("Successful", "Added Course into API \n Status Code: 200")
            except:
                messagebox.showerror("Invalid Response", "Unable to add as Course Run has already been added. \n Status Code: 400 ", )

        def DownloadFile():
            try:
                df = pd.read_json('/Users/Ming/Documents/APIApplication/CourseRunPayLoad.json')
                df.to_csv(filedialog.asksaveasfilename(defaultextension='.csv'))
                messagebox.showinfo("Successful", "CSV file has been downloaded")
            except:
                print("user didnt save.")

        def ViewJsonFile():
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
        ViewJsonButton = tk.Button(self, text="View course run in json", width=18, pady=5, bg="white",
                               command=ViewJsonFile)
        ViewJsonButton.place(relx=0.5, rely=0.65, anchor=CENTER)


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

        label2 = tk.Label(self, text="You are about to add an enrollment")
        label2.place(relx=0.5, rely=0.15, anchor=CENTER)

        def AddEnrollment():
            messagebox.showinfo("Successful", "Added Enrollment into API")

        def DownloadFile():
            global read_file

            export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
            read_file.to_csv(export_file_path, index=None, header=True)
            messagebox.showinfo("Successful", "CSV file has been downloaded")

        # When button is pressed, function is called
        AddButton = tk.Button(self, command=AddEnrollment, text='Add', width=10, pady=5, bg="white")
        AddButton.place(relx=0.5, rely=0.5, anchor=CENTER)
        BackButton = tk.Button(self, text="Back", width=10, pady=5, bg="white",
                               command=lambda: controller.show_frame(StartPage))
        BackButton.place(relx=0.3, rely=0.5, anchor=CENTER)
        NextButton = tk.Button(self, text="Next", width=10, pady=5, bg="white", command=lambda: controller.show_frame(PageThree))
        NextButton.place(relx=0.7, rely=0.5, anchor=CENTER)
        ViewButton = tk.Button(self, text="View enrollment in CSV", width=18, pady=5, bg="white",
                               command=DownloadFile)
        ViewButton.place(relx=0.5, rely=0.6, anchor=CENTER)


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