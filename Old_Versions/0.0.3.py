import Tkinter
import tempfile

student_list_temp = []

with open('GoalTrak/StudentList.txt') as fd:
    for ln in fd:
        Student_Name = ln
        student_list_temp.append(Student_Name[:-1])
fd.close()

class GoalTrak(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=1,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter new student here.")
        
        quitButton = Tkinter.Button(self,text=u"Quit", command=self.OnButtonClick)
        quitButton.grid(column=1,row=1)
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable, \
        anchor="w",fg="white",bg="navy")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Welcome to GoalTrak")
        
        StudentListDisplay = Tkinter.Listbox(self)
        StudentListDisplay.grid(row=2,column=0,columnspan=2,sticky='W')
        for student in student_list_temp:
            StudentListDisplay.insert(Tkinter.END, student)
        
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
    
    def OnButtonClick(self):
        GoalTrak.destroy(self)
        
    def OnPressEnter(self,event):
        hold = self.entryVariable.get()
        hold = str(hold)
        with open('GoalTrak/StudentList.txt', 'a') as textfile:
            if (hold) not in student_list_temp:
                student_list_temp.append(hold[:-1])
                textfile.write(hold + '\n')
                self.labelVariable.set( self.entryVariable.get() + " added" )
            else:
                self.labelVariable.set( self.entryVariable.get() + " is already in list" )
            textfile.close()
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
if __name__ == "__main__":
    app = GoalTrak(None)
    app.title('GoalTrak v. 0.0.2')
    app.mainloop()