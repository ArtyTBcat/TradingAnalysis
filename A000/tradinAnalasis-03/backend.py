import time
import tkinter as tk
from tkinter import messagebox
import pygubu
import os



class tkcommands():
    def __init__(self) -> None:
        self.callbacks = {
            'graphshort': tkcommands.on_button2_click
        }
        self.builder = builder = pygubu.Builder()
    def on_button1_click(): 
        messagebox.showinfo('Message', 'You clicked Button 1')
    def on_button2_click():
            messagebox.showinfo('Message', 'You clicked Button 2')
    # def on_button3_click():
    #     MyApplication().builder.get_variable('combox')
    def submit(self):
        print(self.builder.get_variable('combox'))


class MyApplication(pygubu.TkApplication):        
    def _create_ui(self):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, "Templates/pannel.ui")
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(file_path)
        self.mainwindow = builder.get_object('frame1', self.master)
        builder.connect_callbacks(tkcommands().callbacks)
        print(builder.get_variable('combox'))

        

root = tk.Tk()
app = MyApplication(root)
app.run()

