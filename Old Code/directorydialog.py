#!/usr/local/bin/python3.6
import tkinter as tk
from tkinter import *
from tkinter import filedialog
#import tkinter, tkconstants, tkFileDialog
root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
print (root.filename)