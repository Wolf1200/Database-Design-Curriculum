import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import Scrollbar
from Curriculum import *

LARGE_FONT = ("Verdana", 12)
CURRICULUMS = []
COURSES = []


def updatecurriculums():
    global CURRICULUMS
    tempcurriculums = getcurrentcurriculums()
    CURRICULUMS = [None] * len(tempcurriculums)
    i = 0
    for curr in tempcurriculums:
        CURRICULUMS[i] = curr[0]
        i += 1


def updatecourses():
    global COURSES
    tempcourses = getcurrentcourses()
    COURSES = [None] * len(tempcourses)
    i = 0
    for curr in tempcourses:
        COURSES[i] = curr[0]
        i += 1


class DatabaseGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, SearchCurriculumPage, SearchCoursePage,
                  SearchCourseByCurriculumPage, CurriculumSemesterRangeSearch,
                  CurriculumDashboardPage, InsertCurriculumPage, InsertCoursePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont == SearchCurriculumPage:
            frame.updatecurrlist()
        frame.tkraise()


class InsertCurriculumPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Curriculum Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        labelCName = tk.Label(self, text="Name")
        labelCID = tk.Label(self, text="Head ID")
        labelCHeadName = tk.Label(self, text="Head Name")
        labelCCred = tk.Label(self, text="Total Credits")
        labelmaxCUnits = tk.Label(self, text="Max Units")
        labelCCoverage = tk.Label(self, text="Coverage")
        labelCNumGoals = tk.Label(self, text="Number of Goals")
        insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        button = tk.Button(self, text="Back to Start Page",
                           command=lambda: self.backtostart(controller))

        vcmd = (self.register(self.validateint))
        vcmd2 = (self.register(self.validatefloat), '%S', '%P')
        self.nametext = tk.Entry(self)
        self.headidtext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.headname = tk.Entry(self)
        self.totcreditstext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.maxunitstext = tk.Entry(self, validate='all', validatecommand=vcmd2)
        self.coveragetext = tk.Entry(self)
        self.numgoalstext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))

        self.errorlabel = tk.Label(self, text="One or more fields were left blank", fg='red')

        labelCName.pack()
        self.nametext.pack()
        labelCID.pack()
        self.headidtext.pack()
        labelCHeadName.pack()
        self.headname.pack()
        labelCCred.pack()
        self.totcreditstext.pack()
        labelmaxCUnits.pack()
        self.maxunitstext.pack()
        labelCCoverage.pack()
        self.coveragetext.pack()
        labelCNumGoals.pack()
        self.numgoalstext.pack()
        insert.pack(side=tk.BOTTOM)
        button.pack(side=tk.BOTTOM)

    def insertpressed(self, controller):
        name = self.nametext.get()
        id = self.headidtext.get()
        headname = self.headname.get()
        totcred = self.totcreditstext.get()
        maxunits = self.maxunitstext.get()
        coverage = self.coveragetext.get()
        numgoals = self.numgoalstext.get()

        if not name or not id or not headname or not totcred or not maxunits or not coverage or not numgoals:
            self.errorlabel.pack()
        else:
            self.nametext.delete(0, 'end')
            self.headidtext.delete(0, 'end')
            self.headname.delete(0, 'end')
            self.totcreditstext.delete(0, 'end')
            self.maxunitstext.delete(0, 'end')
            self.coveragetext.delete(0, 'end')
            self.numgoalstext.delete(0, 'end')
            array = [name, id, totcred, maxunits, coverage, numgoals]
            insertcurriculum(array)
            if self.errorlabel.winfo_ismapped():
                self.errorlabel.pack_forget()
            controller.show_frame(StartPage)
            updatecurriculums()

    def backtostart(self, controller):
        if self.errorlabel.winfo_ismapped():
            self.errorlabel.pack_forget()
        controller.show_frame(StartPage)

    def validateint(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def validatefloat(self, text, P):
        if text in '0123456789.':
            try:
                float(P)
                return True
            except ValueError:
                return False
        else:
            return False


class SearchCurriculumPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search Curriculum Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        updatecurriculums()

        self.labelCName = tk.Label(self)
        self.labelCID = tk.Label(self)
        self.labelCHeadName = tk.Label(self)
        self.labelCCred = tk.Label(self)
        self.labelmaxCUnits = tk.Label(self)
        self.labelCCoverage = tk.Label(self)
        self.labelCNumGoals = tk.Label(self)

        global CURRICULUMS
        self.curriculum = ttk.Combobox(self, values=CURRICULUMS)
        button1 = tk.Button(self, text="Search", command=lambda: self.getinfo())
        button2 = tk.Button(self, text="Back to Start Page",
                            command=lambda: self.gotostartpage(controller))

        self.curriculum.pack(side=tk.TOP)
        button1.pack(side=tk.BOTTOM)
        button2.pack(side=tk.BOTTOM)

    def getinfo(self):
        info = getcurriculum(self.curriculum.get())
        info = info[0]

        name = info[0]
        headID = info[1]
        headName = info[2]
        totCredits = info[3]
        maxUnits = info[4]
        coverage = info[5]
        numGoals = info[6]

        if self.labelCName.winfo_ismapped():
            self.labelCName.pack_forget()
            self.labelCID.pack_forget()
            self.labelCHeadName.pack_forget()
            self.labelCCred.pack_forget()
            self.labelmaxCUnits.pack_forget()
            self.labelCCoverage.pack_forget()
            self.labelCNumGoals.pack_forget()

        self.labelCName = tk.Label(self, text="Name: " + name)
        self.labelCID = tk.Label(self, text="Head ID: " + str(headID))
        self.labelCHeadName = tk.Label(self, text="Head Name: " + headName)
        self.labelCCred = tk.Label(self, text="Total Credits: " + str(totCredits))
        self.labelmaxCUnits = tk.Label(self, text="Max Units: " + str(maxUnits))
        self.labelCCoverage = tk.Label(self, text="Coverage: " + coverage)
        self.labelCNumGoals = tk.Label(self, text="Number of Goals: " + str(numGoals))

        self.labelCName.pack()
        self.labelCID.pack()
        self.labelCCred.pack()
        self.labelmaxCUnits.pack()
        self.labelCCoverage.pack()
        self.labelCNumGoals.pack()

    def gotostartpage(self, controller):
        self.labelCName.pack_forget()
        self.labelCID.pack_forget()
        self.labelCCred.pack_forget()
        self.labelmaxCUnits.pack_forget()
        self.labelCCoverage.pack_forget()
        self.labelCNumGoals.pack_forget()
        controller.show_frame(StartPage)

    def updatecurrlist(self):
        global CURRICULUMS
        self.curriculum.pack_forget()
        self.curriculum = ttk.Combobox(self, values=CURRICULUMS)
        self.curriculum.pack()


class CurriculumDashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Curriculum Dashboard", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        button = tk.Button(self, text="Back to Start Page",
                           command=lambda: controller.show_frame(StartPage))

        scrollbar.pack(side="right", fill="y")
        button.pack(side=tk.BOTTOM)


class CurriculumSemesterRangeSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search Aggregate Distribution Page",
                         font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        labelCurr = tk.Label(self, text="Curriculum")
        labelYear1 = tk.Label(self, text="Year")
        labelYear2 = tk.Label(self, text="Year")
        labelSemester1 = tk.Label(self, text="Semester Start")
        labelSemester2 = tk.Label(self, text="Semester Start")

        curriculum = ttk.Combobox(self, values=["CS", "MTH", "PHY"])
        curriculum.current(0)
        semesterStart = ttk.Combobox(self, values=["Spring", "Fall"])
        semesterStart.current(0)
        semesterEnd = ttk.Combobox(self, values=["Spring", "Fall"])
        semesterEnd.current(0)
        yearStart = ttk.Combobox(self, values=["2016", "2017", "2018"])
        yearStart.current(0)
        yearEnd = ttk.Combobox(self, values=["2016", "2017", "2018"])
        yearEnd.current(0)
        button1 = tk.Button(self, text="Search")
        button2 = tk.Button(self, text="Back to Start Page",
                            command=lambda: controller.show_frame(StartPage))

        labelCurr.pack(side=tk.TOP)
        curriculum.pack(side=tk.TOP)

        labelYear1.pack(side=tk.TOP)
        yearStart.pack(side=tk.TOP)

        labelSemester1.pack(side=tk.TOP)
        semesterStart.pack(side=tk.TOP)

        labelYear2.pack(side=tk.TOP)
        yearEnd.pack(side=tk.TOP)

        labelSemester2.pack(side=tk.TOP)
        semesterEnd.pack(side=tk.TOP)

        button1.pack(side=tk.BOTTOM)
        button2.pack(side=tk.BOTTOM)


class SearchCoursePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search Course Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.labelCName = tk.Label(self)
        self.labelCCode = tk.Label(self)
        self.labelCNum = tk.Label(self)
        self.labelCHours = tk.Label(self)
        self.labelCDesc = tk.Label(self)

        coursestemp = getcurrentcourses()
        courses = [None] * len(coursestemp)
        i = 0
        for curr in coursestemp:
            courses[i] = curr[0]
            i += 1

        self.course = ttk.Combobox(self, values=courses)
        button1 = tk.Button(self, text="Search", command=lambda: self.getinfo())
        button2 = tk.Button(self, text="Back to Start Page",
                            command=lambda: self.gotostartpage(controller))

        self.course.pack(side=tk.TOP)
        button1.pack(side=tk.BOTTOM)
        button2.pack(side=tk.BOTTOM)

    def getinfo(self):
        info = getcourse(self.course.get())
        info = info[0]

        name = info[0]
        code = info[1]
        num = info[2]
        hours = info[3]
        desc = info[4]

        if self.labelCName.winfo_ismapped():
            self.labelCName.pack_forget()
            self.labelCCode.pack_forget()
            self.labelCNum.pack_forget()
            self.labelCHours.pack_forget()
            self.labelCDesc.pack_forget()

        self.labelCName = tk.Label(self, text="Name: " + name)
        self.labelCCode = tk.Label(self, text="Head ID: " + code)
        self.labelCNum = tk.Label(self, text="Total Credits: " + str(num))
        self.labelCHours = tk.Label(self, text="Max Units: " + str(hours))
        self.labelCDesc = tk.Label(self, text="Coverage: " + desc)

        self.labelCName.pack()
        self.labelCCode.pack()
        self.labelCNum.pack()
        self.labelCHours.pack()
        self.labelCDesc.pack()

    def gotostartpage(self, controller):
        self.labelCName.pack_forget()
        self.labelCCode.pack_forget()
        self.labelCNum.pack_forget()
        self.labelCHours.pack_forget()
        self.labelCDesc.pack_forget()
        controller.show_frame(StartPage)


class InsertCoursePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Course Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        labelCName = tk.Label(self, text="Name")
        labelCCode = tk.Label(self, text="Sub Code")
        labelCNum = tk.Label(self, text="Course Number")
        labelCHours = tk.Label(self, text="Credit Hours")
        labelCDesc = tk.Label(self, text="Description")

        insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        button = tk.Button(self, text="Back to Start Page",
                           command=lambda: self.backtostart(controller))

        vcmd = (self.register(self.validateint))
        self.nametext = tk.Entry(self)
        self.codetext = tk.Entry(self)
        self.coursenumtext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.hourstext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.desctext = tk.Text(self)

        self.errorlabel = tk.Label(self, text="One or more fields were left blank", fg='red')

        labelCName.pack()
        self.nametext.pack()
        labelCCode.pack()
        self.codetext.pack()
        labelCNum.pack()
        self.coursenumtext.pack()
        labelCHours.pack()
        self.hourstext.pack()
        labelCDesc.pack()
        self.desctext.pack()
        insert.pack(side=tk.BOTTOM)
        button.pack(side=tk.BOTTOM)

    def insertpressed(self, controller):
        name = self.nametext.get()
        code = self.codetext.get()
        coursenum = self.coursenumtext.get()
        hours = self.hourstext.get()
        desc = self.desctext.get(1.0, tk.END)

        if not name or not code or not coursenum or not hours or not desc:
            self.errorlabel.pack()
        else:
            array = [name, code, coursenum, hours, desc]
            print(array)
            insertcourse(array)
            if self.errorlabel.winfo_ismapped():
                self.errorlabel.pack_forget()
            controller.show_frame(StartPage)

    def backtostart(self, controller):
        if self.errorlabel.winfo_ismapped():
            self.errorlabel.pack_forget()
        controller.show_frame(StartPage)

    def validateint(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False


class SearchCourseByCurriculumPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search Course by Curriculum Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        labelCurr = tk.Label(self, text="Curriculum")
        labelCourse = tk.Label(self, text="Course")

        curriculum = ttk.Combobox(self, values=["Test", "Test2", "Testetc"])
        curriculum.current(0)
        course = ttk.Combobox(self, values=["Test", "Test2", "Testetc"])
        course.current(0)
        button1 = tk.Button(self, text="Search")
        button2 = tk.Button(self, text="Back to Start Page",
                            command=lambda: controller.show_frame(StartPage))

        labelCurr.pack(side=tk.TOP)
        curriculum.pack(side=tk.TOP)
        labelCourse.pack(side=tk.TOP)
        course.pack(side=tk.TOP)
        button1.pack(side=tk.BOTTOM)
        button2.pack(side=tk.BOTTOM)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Curriculum Info", command=lambda:
                            controller.show_frame(SearchCurriculumPage))
        button2 = tk.Button(self, text="Course Info", command=lambda:
                            controller.show_frame(SearchCoursePage))
        button3 = tk.Button(self, text="Course Sections by Curriculum",
                            command=lambda: controller.
                            show_frame(SearchCourseByCurriculumPage))
        button4 = tk.Button(self, text="Course Outcomes", command=lambda:
                            controller.show_frame(CurriculumSemesterRangeSearch
                                                  ))
        button5 = tk.Button(self, text="Curriculum Dashboard", command=lambda:
                            controller.show_frame(CurriculumDashboardPage))
        button6 = tk.Button(self, text="Insert Curriculum", command=lambda:
                            controller.show_frame(InsertCurriculumPage))
        button7 = tk.Button(self, text="Insert Course", command=lambda:
                            controller.show_frame(InsertCoursePage))

        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        button5.pack()
        button6.pack()
        button7.pack()
