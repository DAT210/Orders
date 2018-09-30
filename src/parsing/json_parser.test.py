import json_parser as jp
import tkinter as tk
from tkinter import filedialog


if __name__ == "__main__":    
# prints out a table of (value name : value) pairs to test parsing

    root = tk.Tk()
    root.withdraw()

    filename = tk.filedialog.askopenfilename() # open dummy.json
    items = jp.json_to_dict(filename)
       
    for item in items:
        print("I am the", item["Name"])
        for value in item:
            print(value, " : " , item[value])
        print(" ")


    