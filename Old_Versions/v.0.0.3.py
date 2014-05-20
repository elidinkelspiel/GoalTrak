#####GoalTrak version v. 0.0.3 (alpha version 3)#####

###March 28th, 2014###

#By Eli Dinkelspiel#

#This version's functionality:
#1) Can add names to a list database of Students
#2) Recognizes if name is already in list
#3) Refreshes listbox upon adding new name
#4) Quit button
#5) I started documenting cause I'm cool like that. You can thank me later.

#Changes from last version:
#Everything cause I just started documenting

#Goals for next version#
#Remove names from list
#Display a simple piece of data upon name selection (arbitrary, doesn't have to have any relevance or functionality


import Tkinter
import tempfile #Prolly will use later

student_list_temp = []

#Loads data from a save#

with open('GoalTrak/StudentList.txt') as fd:
    for ln in fd:
        Student_Name = ln
        student_list_temp.append(Student_Name[:-1])
fd.close()

###The Big Cheese###

class GoalTrak(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        
        self.entryVariable = Tkinter.StringVar() #Entry Box#
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=1,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter new student here.")
        
        self.quitButton = Tkinter.Button(self,text=u"Quit", command=self.OnButtonClick) #Quit button#
        self.quitButton.grid(column=1,row=1)
        
        self.labelVariable = Tkinter.StringVar() #Banner#
        label = Tkinter.Label(self,textvariable=self.labelVariable, \
        anchor="w",fg="white",bg="navy")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Welcome to GoalTrak")
        
        self.StudentListDisplay = Tkinter.Listbox(self) #First widget I wrote myself!
        self.StudentListDisplay.grid(row=2,column=0,columnspan=2,sticky='W')
        for student in student_list_temp:
            self.StudentListDisplay.insert(Tkinter.END, student)
        
        self.grid_columnconfigure(0,weight=1) #This makes it so the window is resizable#
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
    
    def OnButtonClick(self): 
        GoalTrak.destroy(self) #Question: is this legit?
                
    def OnPressEnter(self,event): #Enters students into save file#
        hold = self.entryVariable.get()
        hold = str(hold)
        with open('GoalTrak/StudentList.txt', 'a') as textfile: #This appends students to the already existing document of students
            if (hold) not in student_list_temp:
                student_list_temp.append(hold)
                textfile.write(hold + '\n')
                self.labelVariable.set( self.entryVariable.get() + " added" )
                self.StudentListDisplay.delete(0, Tkinter.END)
                for student in student_list_temp:
                    self.StudentListDisplay.insert(Tkinter.END, student)
            else: #If student is already in list, aborts#
                self.labelVariable.set( self.entryVariable.get() + " is already in list" )
            textfile.close()
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
if __name__ == "__main__": #Looper: Starring app.mainloop#
    app = GoalTrak(None)
    app.title('GoalTrak v. 0.0.3')
    app.mainloop()