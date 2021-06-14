import tkinter as tk
from tkinter import *
from tkinter import filedialog
import tkinter
#This method is used to saved the local file path for the certificate
def getLocalFile():
    filePath=filedialog.askopenfilename()

    print('File path：',filePath)
    return filePath

# function to open a new window for Configuration
# on a button click
class setConfigWindow(Toplevel):
      
    def __init__(self, master = None):       
        super().__init__(master = master)
        self.title("Configuration Window")
        self.geometry("400x250")
        label = Label(self, text ="Setting")
        label.pack()

        self.resizable(False,False)
        entries = []
        for field in 'UEN', 'Encryption Key', 'Cert File', 'Key File':
            if field == 'CSV File' or field == 'Key File':
                button = tk.Button(text="Browse")
                entries.append(LabelEntry(self, field, button))
            else:
                entries.append(LabelEntry(self, field))
class LabelEntry(tkinter.Frame):
    def __init__(self, parent, text, button=None):
        super().__init__(parent)
        self.pack(fill=tk.X)

        lbl = tk.Label(self, text=text, width=14, anchor='w')
        lbl.pack(side=tk.LEFT, padx=5, pady=5)
        if button:
            frame2 = tk.Frame(self)
            frame2.pack(side=tk.LEFT, expand=True)

            entry = tk.Entry(frame2)
            entry.pack(side=tk.LEFT, fill=tk.X, padx=5)

            button.pack(in_=frame2, side=tk.LEFT, padx=5, pady=5)
        else:
            entry = tk.Entry(self)
            entry.pack(side=tk.LEFT, fill=tk.X, padx=5)