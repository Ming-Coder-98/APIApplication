import json
from os import makedirs
from HttpRequestFunction import loadFile, saveJsonFormat
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import tkinter

##Variable used to store user's input
entries = []
certPemPath = ''
keyPemPath = ''
pathName = ''

#This method is used to saved the local file path for the certificate
def getCertPemFile(window):
    global pathName, certPemPath
    pathName = ''
    filePath=filedialog.askopenfilename()
    print('File path：',filePath)
    certPemPath = filePath
    label_2 = Label(window)
    pathName += "\n" + filePath + '\n'
    label_2["text"] += pathName
    label_2.grid(row = 0, column=1)


#This method is used to saved the local file path for the certificate
def getKeyPemFile(window):
    global pathName, keyPemPath
    filePath=filedialog.askopenfilename()
    print('File path：',filePath)
    keyPemPath = filePath
    pathName += "\n" + filePath
    label_2 = Label(window)
    label_2["text"] += pathName
    label_2.grid(row = 0, column=1)



# function to open a new window for Configuration
# on a button click
class setConfigWindow(Toplevel):
    global entries, pathName
    def __init__(self, master = None):       
        super().__init__(master = master)
        self.title("Configuration Window")
        self.geometry("600x250")
        self.resizable(False,False)

        frame = tk.Frame(self)
        frame.grid(row=0, column=0)
        for field in 'UEN', 'Encryption Key', 'Cert File', 'Key File':
            if field == 'Cert File':
                button = tk.Button(self,text="Browse", command=lambda:getCertPemFile(self))
                entries.append(LabelEntry(frame, field, button))
            elif field =='Key File':
                button = tk.Button(self,text="Browse", command=lambda:getKeyPemFile(self))
                entries.append(LabelEntry(frame, field, button))

            else:
                entries.append(LabelEntry(frame, field))
        
        saveButtonFrame(frame)
        


class saveButtonFrame(tkinter.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.pack(fill=tk.X)
        okButton = Button(self, text="OK", command=lambda:storeAndsave_all(self))
        okButton.pack(side=RIGHT,padx=5, pady=5)


class LabelEntry(tkinter.Frame):
    def __init__(self, parent, text, button=None):
        super().__init__(parent)
        self.pack(fill=tk.X)

        lbl = tk.Label(self, text=text, width=14, anchor='w')
        lbl.pack(side=tk.LEFT, padx=5, pady=5)
        if button:
            
            frame2 = tk.Frame(self)
            frame2.pack(side=tk.LEFT, expand=True)

            button.pack(in_=frame2, side=tk.LEFT, padx=5, pady=5)
        else:
            self.entry = tk.Entry(self)
            self.entry.pack(side=tk.LEFT, fill=tk.X, padx=5)


def storeAndsave_all(window):

    #load config File
    configInfo = loadFile("config.json")
    configInfoJson = json.loads(configInfo)

    configInfoJson["UEN"] = entries[0].entry.get()
    configInfoJson["key"] = entries[1].entry.get()
    configInfoJson["certPath"] = certPemPath
    configInfoJson["keyPath"] = keyPemPath
    #Save config File
    saveJsonFormat(configInfoJson, "config.json")

    

class showConfigWindow(Toplevel):
    def __init__(self, master = None):       
        super().__init__(master = master)
        self.title("Configuration Window")
        self.geometry("600x250")
        self.resizable(False,False)
        self.displayConfigInfo()

    def displayConfigInfo(frame):

        #Load Config Infomation
        configData = loadFile("config.json")
        configData = json.loads(configData)
        

        #Display Config Information
        Fact = "UEN: " + configData["UEN"] + "\nKey: " + configData["key"] + "\nCert Path: " + configData["certPath"] + "\nKey Path: " + configData["keyPath"]
        T = Text(frame, height = 7, width = 60)
        l = Label(frame, text = "Configuration Information")
        l.config(font =("Courier", 12))
        l.pack(pady=10)  
        T.pack()
        T.insert(tk.END, Fact)
        T.config(state=DISABLED)