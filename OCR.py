'''#################Extracting Important text from image#################'''
#Importing Libraries for Text conversion
from PIL import Image
import pytesseract
import cv2
import re
import os

#Collecting Useful data from the Converted Text take from the Image
def get_useful_info(words, j):
    store_name = words[0]
    store_address = "".join(words[1:4])
    date_keywords = ["Date","Purchase Date","Time"]
    invoice_keywords = ["Bill No","Invoice:","Invoice :","Invoice No:","Invoice No :","Invoice No", "ill No"]
    invoice_num,amount,date,time = "","","",""
    amount_keywords = ["total","Grand Total","SubTotal","Sub Total","Final Amount","Net Payable","otal"]
    item_keywords = ["hsn","Item","Items","Qty","hsh"]
    item_flag = 0
    items = []
    date_regex = r'(\d{1,2}/\d{1,2}/\d{1,2})'
    for i in range(4,len(words)):
        string = words[i]
        
        if any(x in string for x in item_keywords):
            item_flag = 1
            continue
        
        for ext in invoice_keywords:
              if ext in string and invoice_num == "":
                  invoice_num = string.replace(ext,"").strip()
                  
        if any(ext1 in string for ext1 in amount_keywords) and amount == "":
            for i in string.lower():
                if i.isdigit() or i==".":
                    amount += i
                elif i == " ":
                    amount = ""

        else:
            for ext2 in date_keywords: 
                if ext2 in string and date == "":
                    date = string.replace(ext2,"").strip()
                
            if date == "":
                try:
                    date = re.search(date_regex, string).group()
                except AttributeError:
                    try:
                        date = re.search(r'\d{2,4}-\[a-zA-Z]{3}-\d{2,4}', string).group()
                    except AttributeError:
                        date = ""
                    
                try:
                    time = re.search(r'\d{1,2}:\d{1,2}:\d{1,2}', string).group()
                except AttributeError:
                    time = ""
    
            if amount=="" and item_flag == 1:
                string = string.split()
                for i in string:
                    if i.isdigit() == False:
                        items.append(" ".join(string))
                        break
            if amount != "":
                item_flag = 0
                
    #Cleaning Items
    data = [store_name,store_address,date + " " + time,invoice_num,amount,items]
    from prettytable import PrettyTable
    headers = ['store_name', 'Store Address',"Date & Time","Invoice No.","Total","Items"]
    t = PrettyTable(headers)
    t.add_row(data)     #Loop this part to add more data to table
    if not os.path.exists('../Data/'):
        os.makedirs('../Data/')
    fp = open('../Data/opt' + str(j) + '.txt', 'w')
    fp.write(str(t))
    fp.close()

#Function to convert image to text
def func(filePath, j):
    image = cv2.imread(filePath)
    #cv2.imshow("Original", image)
    
    blurred = cv2.blur(image, (1,1))
    #cv2.imshow("Blurred_image", blurred)
    img = Image.fromarray(blurred)
    text = pytesseract.image_to_string(img, lang='eng')
    words = text.split("\n")
    #cv2.waitKey(0)
    #Writing the converted text to file
    if not os.path.exists('../OCR/'):
        os.makedirs('../OCR/')
    f = open("../OCR/result" + str(j) + ".txt", "w")
    for k in words:
        f.write(k + "\n")
    f.close()
    get_useful_info(words, j)

#Importing libraries for GUI
import os
from tkinter import filedialog
import tkinter as tk

#Function to get the folder of the dataset
def browse_button():
    filename = filedialog.askdirectory()
    j = 0
    #Checking all files present in the selected directory
    for i in os.listdir(filename):
        func(filename + "/" + i, j)
        j += 1
    root.destroy()  #Destroy's the GUI once execution has completed

#Creating GUI
root = tk.Tk()
#Button to select folder
buttonbrowse = tk.Button(root, text="Browse", command = browse_button).grid(row=0, column=3)

root.mainloop()
