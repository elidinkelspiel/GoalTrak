#####GoalTrak version v. 0.0.4 (alpha version 4)#####

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
#8) User information updater receives input and stores it as usrClass

#Changes from last version:#
#Imported Tkinter like a real boy
#Capability to remove names from list
#Quit button now quits python correctly
#Cool about button that I wrote on the plane 'cause I was bored
#Update information now stores student classes and will load properly (data persistence)

#Goals for next version#
#Allow teachers to assign goals
#Improve the data structure
#Transition to notebook functionality
    #Should have student info display and goal setting


from Tkinter import *
import pickle
import tkMessageBox
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

def file_saver(data, location):
    file = open(location, 'w')
    pickle.dump(data, file)
    file.close()
    
def file_loader(location):
    with open(location, 'rb') as mydoc:
        result = pickle.load(mydoc) 
    mydoc.close()
    return result


class User(object):
    def __init__(self, name, usrClass): #, grades, goals, goalHist, notes):
        self.name = name
        self.usrClass = usrClass
        #self.notes = notes
        #self.grades = grades
        #self.goals = goals
        #self.goalHist = goalHist

#Loading Section#

student_list = []

student_information = {}

with open('GoalTrak/StudentList', 'rb') as file:
    student_list = pickle.load(file)
    file.close()

student_information = student_list
for student in student_information:
    student = User(student, None)
    
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
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter new student here")
        
        self.quitButton = Button(self,text=u"Quit", command=self.OnQuitClick) #Quit button
        self.quitButton.grid(column=1,row=4, sticky='SE')
        
        self.labelVariable = StringVar() #Banner
        self.labelVariable.set(u"Welcome to GoalTrak")
        label = Label(self,textvariable=self.labelVariable, \
        anchor="w",fg="white",bg="navy")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')
        
        
        self.infoUpdate = Button(self, text=u"Update Student Info", command=self.OninfoUpdateClick)
        self.infoUpdate.grid(column=1, row=1)
        
        self.StudentListDisplay = Listbox(self) #First widget I wrote myself!
        self.StudentListDisplay.grid(row=2,column=0,columnspan=2,sticky='W')
        for student in student_list:
            self.StudentListDisplay.insert(END, student)
        
        self.removeButton = Button(self, text=u"Remove student", command=self.OnRemoveClick) #Remove student button
        self.removeButton.grid(column=0,row=3, sticky='W')
        
        self.optionMenu = Button(self, text=u"About", command=self.onAboutClick)
        self.optionMenu.grid(column=0, row=4, sticky='W')
        
        self.grid_columnconfigure(0,weight=1) #This makes it so the window is resizable
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, END)
        
    def onAboutClick(self):
        tkMessageBox.showinfo(title=u'About', message=u'GoalTrak v. Alpha IV by Eli Dinkelspiel')
    
        
    def student_list_updater(self, studentlist):
        self.StudentListDisplay.delete(0, END)
        for student in studentlist:
            self.StudentListDisplay.insert(END, student)
    
    def OnQuitClick(self):
        result = tkMessageBox.askokcancel(title='GoalTrak', message='Are you sure you want to quit GoalTrak?')
        if result == True:
            GoalTrak.destroy(self)
            
        
    def OnRemoveClick(self):
        index = self.StudentListDisplay.curselection()
        index = int(index[0])
        result = tkMessageBox.askokcancel(title='Are you sure?', \
        message='Are you sure you want to remove %s? This cannot be undone and will remove all associated data.' \
        % (student_list[index]))
        if result == True:
            del student_list[index]
            self.student_list_updater(student_list)
            file_saver(student_list, 'GoalTrak/StudentList')
                
        
    def OnPressEnter(self, event): #Enters students into save file
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
        
    def OninfoUpdateClick(self):
    
        def onSaveQuitClick():
            hold = self.UserInformationUpdater.classEntry.get()
            hold = str(hold)
            for student in student_information:
                if student == student_name:
                    current_student.usrClass = hold
                    file_saver(current_student, 'GoalTrak/StudentInformation' + student_name)
            self.UserInformationUpdater.destroy()
            
        index = self.StudentListDisplay.curselection()
        index = int(index[0])
        student_name = student_list[index]
        try:
            current_student = file_loader('GoalTrak/StudentInformation' + student_name) 
        except (IOError):
            current_student = User(student_name, None) #, None, None, None, None)
        
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
        if current_student.usrClass == None:
            self.UserInformationUpdater.classEntryInit.set(u"Enter student's class here")
        else:
            self.UserInformationUpdater.classEntryInit.set(str(current_student.usrClass))
        
        self.UIU_quitButton = Button(self.UserInformationUpdater, text=u"Save and Quit", command=onSaveQuitClick)
        self.UIU_quitButton.grid(column=1, row=2)
        
        self.UserInformationUpdater.grid_columnconfigure(0,weight=1) #This makes it so the window is resizable
        self.UserInformationUpdater.resizable(True,True)
        self.UserInformationUpdater.update()
        self.UserInformationUpdater.geometry(self.UserInformationUpdater.geometry())
        
        
        '''with open('GoalTrak/StudentInformation.txt', 'r') as textfile:
            StudentInfo = textfile.read()
            existing = False
            for student in StudentInfo:
                if key == student_list[index]:
                    existing = True
                    student[strftime('%m/%d/%Y')] = hold
            if existing == False:
                for student in StudentInfo:
                    if key == student_list[index]:
                        student[strftime('%m/%d/%Y')] = hold
            textfile.close()
        open('GoalTrak/StudentInformation.txt.', 'w').close()
        with open('GoalTrak/StudentInformation.txt', 'a') as textfile:
            textfile.write(StudentInfo)'''

        
if __name__ == "__main__": #Looper: Starring app.mainloop
    app = GoalTrak(None)
    app.title('GoalTrak v. 0.0.4')
    app.mainloop()