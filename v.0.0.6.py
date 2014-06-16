#####GoalTrak version v. 0.0.6 (alpha version 6)#####

###May 21st, 2014###

#By Eli Dinkelspiel#

#This version's functionality:# (note: not all inclusive, just big stuff)
#1) Can add names to a list database of students, which is saved in a text document bundled with the program
#2) Recognizes if name is already in list
#3) Refreshes listbox upon alterations to Student List
#4) Remove names from list
#5) User information Updater stores usrClass and can set one goal
    #WHICH MEANS IT CAN SET GOALS!
#6) Quit button
#7) About button
#8) Data persistence
#9) Notebook functionality
    #Displays user information
#10) Can refresh user information manually (it's not a bug it's a feature)
#11) Stability
#12) Everything on GitHub

#Changes from last version:#
#Finished moving documentation to this wiki
#Changed goalHist and notes to one argument, dataPoint
#dataPoint is inherited. It's its own class.
#dataPoint has a function, compile()
#creates a dictionary with all possible data types. If data type isn't included passed NoneType. 
#Added functionality to my new text field and spinbox!



#Known Bugs/TODO#


#Goals for this version#
#Track goal values over time
#Store notes for each student
#BONUS: Sort users by class


#Goals for next version#


from Tkinter import *
import pickle
import tkMessageBox
from os import remove
from ttk import Notebook, PanedWindow
from datetime import datetime
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
        raise(IOError)
        """If you're seeing this error and your name is not Eli Dinkelspiel, \
        please contact Eli to sort out your loading issues. Most likely, you moved or altered relevant storage data. \
        Actually, that's exactly what you did, but I wanted to sugarcoat it. Sorry, mate. If this program is somehow in use in an actual classroom context, \
        sorry for the rudeness of this message. I started GoalTrak as a school project. If you really need my help, don't hesitate to email me at edinkelspiel@gmail.com, or \
        call me at 415-407-3601. If you're at Urban, Parisa or Bethany will probably be able to help you out. And if you're really computer illiterate, \
        you may be intimidated by this window, which looks like the bowels of the computer. Don't worry, go ahead and quit the terminal. It won't do anything. Bye!"""

def dataPointCompile(goal, goalVal, note):
        return {'timestamp':datetime.now(),
        'goal':goal, 
        'goalVal':goalVal,
        'note':note
        }
        
class User(object):
    def __init__(self, name, usrClass, goals, dataHist): #grades
        self.name = name
        self.usrClass = usrClass
        #self.grades = grades
        self.goals = goals
        self.dataHist = dataHist
    
current_student = None



#Loading Section#

student_list = file_loader('GoalTrak/StudentList')


student_information = {}

for student in student_list:
    #Do not put file_loader in here! I need my own try/except
    try:
        with open('GoalTrak/StudentInformation' + student, 'rb') as mydoc:
            student_information[student] = pickle.load(mydoc) 
        mydoc.close()
    except (IOError):
        student_information[student] = User(student, None, {}, [])
    
###The Big Cheese###

class GoalTrak(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        
        self.entryVariable = StringVar() #Student entry box
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
        
        self.tab = Notebook(width = 500, height = 300) #Notebook
        self.tab.pressed_index = None
        
        
        ###Notebook###
        
        self.studentInfoDisplayFrame = Frame(self.tab) ####Info display tab###
        
        self.studentNameLabelVar = StringVar() #Student name label
        self.studentNameLabelVar.set('Click "show information"')
        studentNameLabel = Label(self.studentInfoDisplayFrame, textvariable=self.studentNameLabelVar, fg='black', bg='white')
        studentNameLabel.grid(column=0,row=0,sticky='NW')
        
        self.studentClassLabelVar = StringVar() #Student class label
        self.studentClassLabelVar.set('')
        studentClassLabel = Label(self.studentInfoDisplayFrame, textvariable=self.studentClassLabelVar, fg='black', bg='white')
        studentClassLabel.grid(column=0,row=1,sticky='W')
        
        self.studentGoal1LabelVar = StringVar() #Student goal1 label
        self.studentGoal1LabelVar.set('')
        studentGoal1Label = Label(self.studentInfoDisplayFrame, textvariable=self.studentGoal1LabelVar, fg='black', bg='white')
        studentGoal1Label.grid(column=0,row=2,sticky='W')
        
        self.dataGenerationFrame = Frame(self.tab) ###Data entry frame###
        self.dataGenerationFrame.grid()
        
        self.listboxFrame = Frame(self.dataGenerationFrame) #LISTBOX
        self.listboxFrame.grid(column=0, row=0, columnspan=2, rowspan=2, padx=2, pady=2)
        self.goalSelection = Listbox(self.listboxFrame)
        self.goalSelection.pack()
        
        self.goalValEntryFrame = Frame(self.dataGenerationFrame) #SPINBOX
        self.goalValEntryFrame.grid(row= 0, column=4, padx=2, pady=2)
        self.goalValEntry = Spinbox(self.goalValEntryFrame, from_=0, to=10)
        self.goalValEntry.pack()
        
        self.noteEntryFrame = Frame(self.dataGenerationFrame) #TEXT
        self.noteEntryFrame.grid(column= 2, row=1, columnspan=3, rowspan=3, padx=2, pady=2)
        self.noteEntry = Text(self.noteEntryFrame, borderwidth=2, height = 15, width = 40, relief=SUNKEN)
        self.noteEntry.pack(anchor= 'w')
        
        self.buttonBox = Frame(self.dataGenerationFrame)
        self.buttonBox.grid(row= 4, column= 0, columnspan= 2, rowspan= 2, sticky= 'W')
        self.addDataButton = Button(self.buttonBox, text = 'Store Information', command=self.onStoreInformationClick)
        self.addDataButton.pack()
        
        self.tab.add(self.studentInfoDisplayFrame, text='Student Info') #Labels tabs
        self.tab.add(self.dataGenerationFrame, text='Enter Data')
        self.tab.grid(column = 0, row = 7, rowspan = 5, sticky = 'EW')

        self.grid_columnconfigure(0,weight=1) #This makes it so the window is resizable
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, END)
        
        
    def onAboutClick(self): #About message
        tkMessageBox.showinfo(title=u'About', message=u'GoalTrak v. Alpha VI by Eli Dinkelspiel')
    
        
    def student_list_updater(self, studentlist):
        self.StudentListDisplay.delete(0, END)
        for student in studentlist:
            self.StudentListDisplay.insert(END, student)#Refreshes student listbox
    
    def onQuitClick(self):
        result = tkMessageBox.askokcancel(title='GoalTrak', message='Are you sure you want to quit GoalTrak?')
        if result == True:
            GoalTrak.destroy(self) #Quit button
               
    def onRemoveClick(self):
        index = self.StudentListDisplay.curselection()
        index = int(index[0])
        result = tkMessageBox.askokcancel(title='Are you sure?', \
        message='Are you sure you want to remove %s? This cannot be undone and will remove all associated data.' \
        % (student_list[index]))
        if result == True:
            try:
                remove('GoalTrak/StudentInformation' +student_list[index])
            except (OSError):
                pass
            del student_list[index]
            self.student_list_updater(student_list)
            file_saver(student_list, 'GoalTrak/StudentList')#Remove student button
            
                     
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
        self.entry.selection_range(0, END)#Add student with <enter>
    
    def onStoreInformationClick(self):
        note_hold = self.noteEntry.get(1.0, END)
        val_hold = self.goalValEntry.get()
        validEntry = True
        try:
            entry_mode = current_student.goals['goal' + self.goalSelection.curselection()[0]]
        except(KeyError):
            entry_mode = 3
        if entry_mode in ['goal1', 'goal2', 'goal3']:
            if self.goalSelection.get() in ['<goal1 not set>', '<goal2 not set>', '<goal3 not set>']:
                tkMessageBox.showerror('Goal not defined')
                validEntry = False
            else:
                if note_hold == '':
                    note_hold = None
        elif entry_mode == 3:
            val_hold = None
            entry_mode = None
        if validEntry:
            current_student.dataHist.append(dataPointCompile(entry_mode, val_hold, note_hold))
            file_saver(current_student, 'GoalTrak/StudentInformation' + current_student.name)
            self.labelVariable.set(u"Data safely stored")
            
            
        
    def onShowInformationClick(self): #Refreshes student information display
        studentNameVar = student_list[int(self.StudentListDisplay.curselection()[0])]
        self.studentNameLabelVar.set(studentNameVar)
        
        global current_student
        current_student = file_loader('GoalTrak/StudentInformation' + studentNameVar)
        
        ####Each one of these try/except pairs makes the various User() attributes visible, if they exist. DO NOT BUNDLE AS ONE###
        
        #infoFrame
        try:
            self.studentClassLabelVar.set(current_student.usrClass)
        except (AttributeError):
            self.studentClassLabelVar.set(u'No set class')
        try:
            self.studentGoal1LabelVar.set(current_student.goals['goal1'])
        except (AttributeError):
            self.studentGoal1LabelVar.set(u'Goal 1 not set')
        #dataGenFrame
        self.goalSelection.delete(0, END)
        try:
            self.goalSelection.insert(END, current_student.goals['goal1'])
        except (AttributeError):
            pass
        try:
            self.goalSelection.insert(END, current_student.goals['goal2'])
        except (AttributeError, KeyError):
            pass
        try:
            self.goalSelection.insert(END, current_student.goals['goal3'])
        except (AttributeError, KeyError):
            pass
        self.goalSelection.insert(END, 'Unattached Note')

       

    def onInfoUpdateClick(self): #User Information Updater
        index = self.StudentListDisplay.curselection()
        index = int(index[0])
        student_name = student_list[index]
        
        try: #Gives new students a file object
            global current_student
            current_student = file_loader('GoalTrak/StudentInformation' + student_name)
        except (IOError):
            file_saver(User(student_name, None, None, None), 'GoalTrak/StudentInformation' + student_name)
            global current_student
            current_student = file_loader('GoalTrak/StudentInformation' + student_name)
        
        def onSaveQuitClick(): #Stores the data
        
            classHold = str(self.UserInformationUpdater.classEntry.get())
            goal1Hold = str(self.UserInformationUpdater.goal1Entry.get())
            
            global current_student
            try:
                current_student = file_loader('GoalTrak/StudentInformation' + student_name)
            except (IOError):
                print "New file being created for " + student_name
                current_student = User(student_name, None, None, None)
            
            for student in student_information: #I probably want to get rid of this for loop but I'm afraid to tinker with my code :(
                if student == student_name:
                    try:
                        global current_student
                        current_student.usrClass = classHold
                        current_student.goals['goal1'] = goal1Hold
                        file_saver(current_student, 'GoalTrak/StudentInformation' + student_name)
                    except (AttributeError):
                        print 'New file being created'
                        file_saver(User(student_name, classHold, {'goal1':goal1Hold}, []), 'GoalTrak/StudentInformation' + student_name, )
                        global current_student
                        current_student = file_loader('GoalTrak/StudentInformation' + student_name)
            self.UserInformationUpdater.destroy()

        
                
        
        self.UserInformationUpdater = Toplevel()
        self.UserInformationUpdater.grid()
        
        self.UserInformationUpdater.title("Update Information - %s" % (student_name))
        
        self.UserInformationUpdater.infolabel = Label(self.UserInformationUpdater, \
        text = (u"User Information - %s" % (student_name)), anchor="w", fg="white", bg="navy")
        self.UserInformationUpdater.infolabel.grid(column=0,row=0,columnspan=2,sticky='EW')
        
        #Visual stuff for the updater
        
        self.UserInformationUpdater.classVar = StringVar()
        self.UserInformationUpdater.classEntry = Entry(self.UserInformationUpdater, textvariable=self.UserInformationUpdater.classVar)
        self.UserInformationUpdater.classEntry.grid(column=0,row=1,sticky='EW')
        
        try:
            if current_student.usrClass != None:
                self.UserInformationUpdater.classVar.set(str(current_student.usrClass))
            else:
                self.UserInformationUpdater.classVar.set(u"Enter student's class here")
        except (AttributeError, TypeError):
            self.UserInformationUpdater.classVar.set(u"Enter student's class here")
        
        self.UserInformationUpdater.goal1Var = StringVar()
        self.UserInformationUpdater.goal1Entry = Entry(self.UserInformationUpdater, textvariable=self.UserInformationUpdater.goal1Var)
        self.UserInformationUpdater.goal1Entry.grid(column=0,row=2,sticky='EW')
        
        try:
            self.UserInformationUpdater.goal1Var.set(str(current_student.goals['goal1']))
        except (AttributeError, TypeError):
            self.UserInformationUpdater.goal1Var.set(u"Enter goal 1 here")
        
        
        self.UIU_quitButton = Button(self.UserInformationUpdater, text=u"Save and Quit", command=onSaveQuitClick) #Save & Quit button
        self.UIU_quitButton.grid(column=1, row=2)
        
        self.UserInformationUpdater.grid_columnconfigure(0,weight=1) #This makes it so the window is resizable
        self.UserInformationUpdater.resizable(True,True)
        self.UserInformationUpdater.update()
        self.UserInformationUpdater.geometry(self.UserInformationUpdater.geometry())
        
    def goalSelDispSet(self):
        result = []
        global current_student
        try:
            result.append((current_student.goals['goal1'], '1'))
        except (KeyError, AttributeError):
            pass
        try:
            result.append((current_student.goals['goal2'], '2'))
        except (KeyError, AttributeError):
            pass
        try:
            result.append((current_student.goals['goal3'], '3'))
        except (KeyError, AttributeError):
            pass
        result.append(('Unattached Note', '4'))
        return result
        
        
if __name__ == "__main__": #Looper: Starring app.mainloop
    app = GoalTrak(None)
    app.title('GoalTrak v. 0.0.6')
    app.mainloop()