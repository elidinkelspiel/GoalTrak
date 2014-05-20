import Tkinter
import tempfile

student_list_temp = []

print student_list_temp

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter new student here.")
        
        button = Tkinter.Button(self,text=u"Add students to file", command=self.OnButtonClick)
        button.grid(column=1,row=0)
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable, \
        anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Hello !")
        
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
    
    def OnButtonClick(self):
        with open('StudentList.txt', 'r+') as textfile:
            for student in student_list_temp:
                textfile.write(student + '\n')
            textfile.close()
        self.labelVariable.set("Students added")
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
    def OnPressEnter(self,event):
        self.labelVariable.set( self.entryVariable.get()+" (Student added)" )
        hold = self.entryVariable.get()
        hold = str(hold)
        student_list_temp.append(hold)
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('GoalTrak v. 0.0.1')
    app.mainloop()