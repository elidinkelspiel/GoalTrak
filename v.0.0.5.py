#####GoalTrak version v. 0.0.5 (alpha version 5)#####

###April 12th, 2014###

#By Eli Dinkelspiel#

#This version's functionality:# (note: not all inclusive, just big stuff)
#1) Can add names to a list database of students, which is saved in a text document bundled with the program
#2) Recognizes if name is already in list
#3) Refreshes listbox upon alterations to Student List
#4) Remove names from list
#5) Quit button
#6) About button
#7) Data persistence (so far limited, but structure is set and more should come)

#Changes from last version:#
#Improved file loading: if location doesn't exist, prints the relevant error message (which is rather long, yet helpful) and loads the program rather than crashing the entire program. May still have bugs.
#More documentation


#Known Bugs#
#Making new user attributes is now broken. HELP!
    #FIXED
#WORKING ON IMPLEMENTING A WINDOW IN A CANVAS WIDGET TO DISPLAY TEXT


#Goals for this version#
#Allow teachers to assign goals
#Transition to notebook functionality
    #Should have student info display and goal setting
#Documentation


from Tkinter import *
import pickle
import tkMessageBox
from ttk import Notebook, PanedWindow
'''from os from path import exists
from os import makedirs
newpath = r'C:\Program Files\arbitrary' 
if not os.path.exists(newpath): os.makedirs(newpath)'''
#from time import strftime

def item_from_list_deleter(item, list):
    x = 0
    end = len(list)
    while x < end:
        if list[x] == item:
            del list[x]
            end -= 1
        else:
            x += 1
    return list


def char_stripper_exclude(string, exclude):
    result = []
    for char in list(string):
        if char not in exclude:
            result.append(char)
    return ''.join(result)


def file_saver(data, location):
    file = open(location, 'w')
    pickle.dump(data, file)
    file.close()
    
def file_loader(location): 
    try:
        with open(location, 'rb') as mydoc:
            result = pickle.load(mydoc) 
        mydoc.close()
        return result
    except (IOError):
        print "No such file or directory: " + "\"" + location + "\""
        
        """If you're seeing this error and your name is not Eli Dinkelspiel, \
        please contact Eli to sort out your loading issues. Most likely, you moved or altered relevant storage data. \
        Actually, that's exactly what you did, but I wanted to sugarcoat it. Sorry, mate. If this program is somehow in use in an actual classroom context, \
        sorry for the rudeness of this message. I started GoalTrak as a school project. If you really need my help, don't hesitate to email me at edinkelspiel@gmail.com, or \
        call me at 415-407-3601. If you're at Urban, Parisa or Bethany will probably be able to help you out. And if you're really computer illiterate, \
        you may be intimidated by this window, which looks like the bowels of the computer. Don't worry, go ahead and quit the terminal. It won't do anything. Bye!"""

class User(object):
    def __init__(self, name, usrClass): #, grades, goals, goalHist, notes):
        self.name = name
        self.usrClass = usrClass
        #self.notes = notes
        #self.grades = grades
        #self.goals = goals
        #self.goalHist = goalHist
    
Albert_Einstein = User('Albert Einstein', 'Physics') #Test student

#Loading Section#

student_list = file_loader('GoalTrak/StudentList')

student_list.append('Albert Einstein')

student_information = {}

for student in student_list:
    #Do not put file_loader in here! I need my own try/except
    try:
        with open('GoalTrak/StudentInformation' + student, 'rb') as mydoc:
            student_information[student] = pickle.load(mydoc) 
        mydoc.close()
    except (IOError):
        student_information[student] = User(student, 'Enter student\'s class here')
    
###The Big Cheese###

class GoalTrak(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        
        self.entryVariable = StringVar() #Entry Box
        self.entry = Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=1,sticky='EW')
        self.entry.bind("<Return>", self.onPressEnter)
        self.entryVariable.set(u"Enter new student here")
        
        #Simple buttons#
        
        self.quitButton = Button(self,text=u"Quit", command=self.onQuitClick) #Quit button
        self.quitButton.grid(row = 14, sticky='SE')
        
        self.removeButton = Button(self, text=u"Remove student", command=self.onRemoveClick) #Remove student button
        self.removeButton.grid(column=0,row=6, sticky = 'W')
        
        self.optionMenu = Button(self, text=u"About", command=self.onAboutClick) #About button
        self.optionMenu.grid(row = 13, sticky='SE')
        
        self.infoUpdate = Button(self, text=u"Update Student Info", command=self.onInfoUpdateClick) #Info updater
        self.infoUpdate.grid(column=0, row=4, sticky = 'W')
        
        self.showInformation = Button(self, text = u"Show Information", command=self.onShowInformationClick)
        self.showInformation.grid(column=0, row=5, sticky = 'W')
        
        self.labelVariable = StringVar() #Banner
        self.labelVariable.set(u"Welcome to GoalTrak")
        label = Label(self,textvariable=self.labelVariable, \
        anchor="w",fg="white",bg="navy")
        label.grid(column=0,row=0,sticky='EW')
        
        self.StudentListDisplay = Listbox(self) #Student List
        self.StudentListDisplay.grid(row=2,column=0,columnspan=2,sticky='W')
        for student in student_list:
            self.StudentListDisplay.insert(END, student)
        
        self.tab = Notebook(width=200, height=200) #Notebook
        self.tab.pressed_index = None
        
        self.studentClassLabelVar = StringVar()
        self.studentClassLabelVar.set('')
        self.studentNameLabelVar = StringVar()
        self.studentNameLabelVar.set('Click "show information"')
        self.studentInfoDisplayFrame = Frame(self.tab)
        studentNameLabel = Label(self.studentInfoDisplayFrame, textvariable=self.studentNameLabelVar, fg='black', bg='white')
        studentNameLabel.grid(column=0,row=0,sticky='N')
        studentClassLabel = Label(self.studentInfoDisplayFrame, textvariable=self.studentClassLabelVar, fg='black', bg='white')
        studentClassLabel.grid(column=0,row=1,sticky='W')
        otherWidget = Canvas(self.tab, width=300, height=300)
        
        #studentNameDisplayWindow = self.studentInfoDisplayCanvas.create_window(100,10,window=studentNameLabel)
        #studentClassDisplayWindow = self.studentInfoDisplayCanvas.create_window(100,100,window=studentClassLabel)
        self.tab.add(self.studentInfoDisplayFrame, text='Student Info')
        self.tab.add(otherWidget, text='Other Widget')
        self.tab.grid(column = 0, row = 7, rowspan = 5, sticky = 'EW')


        self.grid_columnconfigure(0,weight=1) #This makes it so the window is resizable
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, END)
        
        
    def onAboutClick(self):
        tkMessageBox.showinfo(title=u'About', message=u'GoalTrak v. Alpha V by Eli Dinkelspiel')
    
        
    def student_list_updater(self, studentlist):
        self.StudentListDisplay.delete(0, END)
        for student in studentlist:
            self.StudentListDisplay.insert(END, student)
    
    def onQuitClick(self):
        result = tkMessageBox.askokcancel(title='GoalTrak', message='Are you sure you want to quit GoalTrak?')
        if result == True:
            GoalTrak.destroy(self)
            
        
    def onRemoveClick(self):
        index = self.StudentListDisplay.curselection()
        index = int(index[0])
        result = tkMessageBox.askokcancel(title='Are you sure?', \
        message='Are you sure you want to remove %s? This cannot be undone and will remove all associated data.' \
        % (student_list[index]))
        if result == True:
            del student_list[index]
            self.student_list_updater(student_list)
            file_saver(student_list, 'GoalTrak/StudentList')
                
        
    def onPressEnter(self, event): #Enters students into save file
        hold = self.entryVariable.get()
        hold = str(hold)
        with open('GoalTrak/StudentList', 'rb') as file: #This appends students to the already existing document of students
            if (hold) not in student_list:
                student_list.append(hold)
                file_saver(student_list, 'GoalTrak/StudentList')
                self.labelVariable.set(self.entryVariable.get() + " added" )
                self.student_list_updater(student_list)
            else: #If student is already in list, aborts
                self.labelVariable.set( self.entryVariable.get() + " is already in list" )
            file.close()
        self.entry.focus_set()
        self.entry.selection_range(0, END)
        
    def onShowInformationClick(self):
        studentNameVar = student_list[int(self.StudentListDisplay.curselection()[0])]
        self.studentNameLabelVar.set(studentNameVar)
        try:
            current_student = file_loader('GoalTrak/StudentInformation' + studentNameVar)
            self.studentClassLabelVar.set(current_student.usrClass)
        except (AttributeError):
            self.studentClassLabelVar.set(u'No set class')
        
        


    def onInfoUpdateClick(self):
        index = self.StudentListDisplay.curselection()
        index = int(index[0])
        student_name = student_list[index]
        
        def onSaveQuitClick():
            hold = self.UserInformationUpdater.classEntry.get()
            hold = str(hold)
            current_student = file_loader('GoalTrak/StudentInformation' + student_name)
            for student in student_information: #I probably want to get rid of this for loop but I'm afraid to tinker with my code :(
                if student == student_name:
                    try:
                        current_student.usrClass = hold
                        file_saver(current_student, 'GoalTrak/StudentInformation' + student_name)
                    except (AttributeError):
                        print 'New file being created'
                        file_saver(User(student_name, hold), 'GoalTrak/StudentInformation' + student_name)
                        current_student = file_loader('GoalTrak/StudentInformation' + student_name)
            self.UserInformationUpdater.destroy()
        try:
            if student_name == 'Albert Einstein':
                current_student = Albert_Einstein
            else:
                current_student = file_loader('GoalTrak/StudentInformation' + student_name)
        except (IOError):
            file_saver('GoalTrak/StudentInformation' + student_name) 
                
        
        self.UserInformationUpdater = Toplevel()
        self.UserInformationUpdater.grid()
        
        self.UserInformationUpdater.title("Update Information - %s" % (student_name)) #student_list[index]
        
        self.UserInformationUpdater.labelVar = StringVar() #Banner
        self.UserInformationUpdater.infolabel = Label(self.UserInformationUpdater, \
        textvariable=self.UserInformationUpdater.labelVar, anchor="w", fg="white", bg="navy")
        self.UserInformationUpdater.infolabel.grid(column=0,row=0,columnspan=2,sticky='EW')
        self.UserInformationUpdater.labelVar.set(u"User Information")
        
        self.UserInformationUpdater.classEntryInit = StringVar() #Entry Box
        self.UserInformationUpdater.classEntry = Entry(self.UserInformationUpdater, textvariable=self.UserInformationUpdater.classEntryInit)
        self.UserInformationUpdater.classEntry.grid(column=0,row=1,sticky='EW')
        try:
            self.UserInformationUpdater.classEntryInit.set(str(current_student.usrClass))
        except (AttributeError):
            self.UserInformationUpdater.classEntryInit.set(u"Enter student's class here")
            
        
        self.UIU_quitButton = Button(self.UserInformationUpdater, text=u"Save and Quit", command=onSaveQuitClick) #You think this section needs a note? Figure it out on your own, hotstuff!
        self.UIU_quitButton.grid(column=1, row=2)
        
        self.UserInformationUpdater.grid_columnconfigure(0,weight=1) #This makes it so the window is resizable
        self.UserInformationUpdater.resizable(True,True)
        self.UserInformationUpdater.update()
        self.UserInformationUpdater.geometry(self.UserInformationUpdater.geometry())
        

        
        
if __name__ == "__main__": #Looper: Starring app.mainloop
    app = GoalTrak(None)
    app.title('GoalTrak v. 0.0.5')
    app.mainloop()