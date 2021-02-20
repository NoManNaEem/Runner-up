
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: PUT YOUR STUDENT NUMBER HERE
#    Student name: PUT YOUR NAME HERE
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Runners-Up
#
#  In this assignment you will combine your knowledge of HTMl
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application that allows the user to access online data.  See the
#  instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these functions
# only.  You can import other functions provided they are standard
# ones that come with the default Python/IDLE implementation and NOT
# functions from modules that need to be downloaded and installed
# separately.  Note that not all of the imported functions below are
# needed to successfully complete this assignment.

# The function for accessing a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup   
# The function for displaying a web document in the host
# operating system's default web browser.  We have given
# the function a distinct name to distinguish it from the
# built-in "open" function for opening local files.
# (You WILL need to use this function in your solution.)
from webbrowser import open as urldisplay

# Import some standard Tkinter functions. (You WILL need to use
# some of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to download and save a web document. If the
# attempted download fails, an error message is written to
# the shell window and the special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * lying - If True the Python function will try to hide its
#      identity from the web server. This can sometimes be used
#      to prevent the server from blocking access to Python
#      programs. However we do NOT encourage using this option
#      as it is both unreliable and unethical!
# * got_the_message - Set this to True once you've absorbed the
#      message above about Internet ethics.
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             lying = False,
             got_the_message = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to open a local HTML file in your operating
# system's default web browser.  (Note that Python's "webbrowser"
# module does not guarantee to open local files, even if you use a
# 'file://..." address).  The file to be opened must be in the same
# folder as this module.
#
# Since this code is platform-dependent we do NOT guarantee that it
# will work on all systems.
#
def open_html_file(file_name):
    
    # Import operating system functions
    from os import system
    from os.path import isfile
    
    # Remove any platform-specific path prefixes from the
    # filename
    local_file = file_name[file_name.rfind('/') + 1:] # Unix
    local_file = local_file[local_file.rfind('\\') + 1:] # DOS
    
    # Confirm that the file name has an HTML extension
    if not local_file.endswith('.html'):
        raise Exception("Unable to open file " + local_file + \
                        " in web browser - Only '.html' files allowed")
    
    # Confirm that the file is in the same directory (folder) as
    # this program
    if not isfile(local_file):
        raise Exception("Cannot find file " + local_file + \
                        " in the same folder as this program")
    
    # Collect all the exit codes for each attempt
    exit_codes = []
    
    # Microsoft Windows: Attempt to "start" the web browser
    code = system('start ' + local_file)
    if code != 0:
        exit_codes.append(code)
    else:
        return 0
    
    # Apple macOS: Attempt to "open" the web browser
    code = system("open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Linux: Attempt to "xdg-open" the local file in the
    # web browser
    code = system("xdg-open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Give up!
    raise Exception('Unable to open file ' + local_file + \
                    ' in web browser - Exit codes: ' + \
                    str(exit_codes))

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

##### DEVELOP YOUR SOLUTION HERE #####




# Gui


window = Tk()

window.title("What's on Second")
# set window size
window.geometry("800x800")
#photo

img = PhotoImage(file=("download.png"))
panel = Label(window, image = img,bg="white").pack(fill="x")


#set window color
window.configure(bg='white')
#radiobutton

Radiobutton_value = IntVar()


Radiobutton1 = Radiobutton(window, text="MUSIC (Top 10 music)",bg="white",fg="green",variable=Radiobutton_value,value=1,font =( 'Verdana', 10))
Radiobutton2 = Radiobutton(window, text="WORLD FASTEST ANIMAL (Top 10)",bg="white",fg="red",variable=Radiobutton_value,value=2,font =( 'Verdana', 10))
Radiobutton3 = Radiobutton(window, text="WORLD SMALLEST ANIMAL (Top 10)",bg="white",fg="orange",variable=Radiobutton_value,value=3,font =( 'Verdana', 10))
Radiobutton4 = Radiobutton(window, text="WORLD FASTEST FISHES (Top 10)",bg="white",fg="blue",variable=Radiobutton_value,value=4,font =( 'Verdana', 10))
Radiobutton1.pack()
Radiobutton2.pack()
Radiobutton3.pack()
previous=Label(window,text="Previous#").pack()
Radiobutton4.pack()

# #button function defination


def update_button():
    if Radiobutton_value.get()==1:
        music()
    if Radiobutton_value.get()==2:
        Fastest_animails()    
    if Radiobutton_value.get()==3:
        Smallest_animals() 
    if Radiobutton_value.get()==4:
        Static()      
def Source_button():
    if Radiobutton_value.get()==1:
        music_source()
    if Radiobutton_value.get()==2:
        Fastest_Animal_source()    
    if Radiobutton_value.get()==3:
        Smallest_Animal_source() 
    if Radiobutton_value.get()==4:
        Static_source()      
# createing Button
Button1=Button(window,text="Update",command=update_button).pack()
Button2=Button(window,text="Source",command=Source_button).pack()
#Runnerup label
runnerup_label=Label(window,text="Runner UP", bg="white",fg="black",font =( 'Verdana', 15))
runnerup_label.pack()

# listbox
listbox1 = Listbox(window , width=50, height=2)
listbox1.pack()
listbox2 = Listbox(window,width=50)
listbox2.pack()
# function
def music():
    str1=download("https://www.officialcharts.com/charts/",save_file=False)
    patt=re.compile('''(alt=")([A-Z ']+)(")''')
    matches= patt.finditer(str1)
    list1=[]
# for i in matches:
#     print(i)
#the commented for loop it for to find the index where the our requird string you may remove it 
    
    list1.append(str1[39178+5: 39188-1])
    list1.append(str1[42518+5: 42527-1])
    list1.append(str1[49301+5: 49321-1])
    list1.append(str1[52694+5: 52708-1])
    list1.append(str1[56079+5: 56096-1])
    list1.append(str1[59457+5: 59475-1])
    list1.append(str1[62790+5: 62812-1])
    list1.append(str1[66146+5: 66170-1])
    list1.append(str1[69503+5: 69513-1]) 
    list1.append(str1[73280+5: 73295-1])
    j=0
    for i in list1:
      
        if(j==1):
            listbox1.insert(1,list1[1])
            
        listbox2.insert(j,i)
        j=j+1


def Fastest_animails():
    str1=download("https://themysteriousworld.com/fastest-land-animals/",save_file=False)
    patt=re.compile('''(<\/span>) ([A-Z 0-9 a-z-&#;]+)(<\/h3>)''')
    matches= patt.finditer(str1)
    list1=[]
    # for i in matches:
    #     print(i)

    list1.append(str1[59288:59321])
    list1.append(str1[52269:52304])
    list1.append(str1[48910:48945])
    list1.append(str1[45593:45634])
    list1.append(str1[42215:42250])
    list1.append(str1[39014:39044])    
    list1.append(str1[35905:35940])
    list1.append(str1[32757:32793])
    list1.append(str1[28195:28242-5])
    list1.append(str1[24384:24418])
    j=0
    for i in list1:
      
        if(j==1):
            listbox1.insert(1,list1[1])
            
        listbox2.insert(j,i)
        j=j+1
def Smallest_animals():
    str1=download("https://bestlifeonline.com/smallest-animals-on-planet/?nab=0&utm_referrer=https%3A%2F%2Fwww.google.com%2F",save_file=False)
    patt=re.compile(''' <div class="title ">([A-Z a-z-]+)<\/div>''')
    matches= patt.finditer(str1)
    list1=[]
    # for i in matches:
    #     print(i)
    
    list1.append(str1[44546+21:44596-6])#10
    list1.append(str1[47136+21:47184-6])#9
    list1.append(str1[50631+21:50673-6])#8
    list1.append(str1[56976+21:57010-6])#7
    list1.append(str1[59970+21:60019-6])#6
    list1.append(str1[62869+21:62912-6])#5    
    list1.append(str1[65002+21:65046-6])#4
    list1.append(str1[68493+21:68546-6])#3
    list1.append(str1[73176+21:73221-6])#2
    list1.append(str1[75914+21:75954-6])#1 
    j=0    
    for i in list1:
      
        if(j==1):
            listbox1.insert(1,list1[1])
            
        listbox2.insert(j,i)
        j=j+1   
def Static():
    import codecs

    path="Static.html" 
    file=codecs.open(path,"rb")
    file1=file.read()
    str1=str(file1)
    patt=re.compile(''' <h3 class="listicle__title heading-3">([a-z A-Z]+)</h3>''')
    matches= patt.finditer(str1)
    list1=[]
 
    list1.append(str1[102504+39:102560-5])#10
    list1.append(str1[107326+39:107378-5])#9
    list1.append(str1[111729+39:111787-5])#8
    list1.append(str1[116402+39:116451-5])#7
    list1.append(str1[120800+39:120854-5])#6
    list1.append(str1[125258+39:125323-5])#5    
    list1.append(str1[129750+39:129804-5])#4
    list1.append(str1[134204+39:134256-5])#3
    list1.append(str1[138642+39:138695-5])#2
    list1.append(str1[143087+39:143151-5])#1
    j=0    
    for i in list1:
      
        if(j==1):
            listbox1.insert(1,list1[1])
            
        listbox2.insert(j,i)
        j=j+1   
def music_source():
    str1=download("https://soundcloud.com/charts/top",save_file=False)        
    j=0
    for i in range(100):
         
        listbox2.insert(j,str1)
        if str1=="\n":
            j=j+1
def Fastest_Animal_source():
    str1=download("https://themysteriousworld.com/fastest-land-animals/",save_file=False)        
    j=0
    for i in range(100):
         
        listbox2.insert(j,str1)
        if str1=="\n":
            j=j+1          
def Smallest_Animal_source():
    str1=download("https://bestlifeonline.com/smallest-animals-on-planet/?nab=0&utm_referrer=https%3A%2F%2Fwww.google.com%2F",save_file=False)        
    j=0
    for i in range(100):
         
        listbox2.insert(j,str1)
        if str1=="\n":
            j=j+1                        
def Static_source():
    import codecs

    path="Static.html" 
    file=codecs.open(path,"rb")
    file1=file.read()
    str1=str(file1)
    j=0
    for i in range(100):
         
        listbox2.insert(j,str1)
        if str1=="\n":
            j=j+1     


window.mainloop()