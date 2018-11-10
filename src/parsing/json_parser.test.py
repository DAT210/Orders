import json_parser as jp
import tkinter as tk
from tkinter import filedialog


if __name__ == "__main__":    
# prints out a table of (value name : value) pairs to test parsing

    root = tk.Tk()
    root.withdraw()

    filename = tk.filedialog.askopenfilename() # open any json
    items, _ = jp.json_to_dict(filename)
    print(type(items))
      
    for item in items:        
        for value in item:
            print(value, " : " , item[value])
        print(" ")

# dumps all the parsed info into testdump.json
# every value with "password" key will be salted in the file
# case-insensitive

    testfile = "testdump.json"

    jp.whatever_to_json(items, "Items", testfile)

    