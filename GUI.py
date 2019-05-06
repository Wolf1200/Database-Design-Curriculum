import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import Scrollbar
from Curriculum import *

LARGE_FONT = ("Verdana", 12)
CURRICULUMS = []
COURSES = []
HOURS = 0
TEMPHOURS = 0
CURRICULUM = ""


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
        updatecourses()
        updatecurriculums()

        for F in (StartPage, SearchCurriculumPage, SearchCoursePage,
                  SearchCourseByCurriculumPage, CurriculumSemesterRangeSearch,
                  CurriculumDashboardPage, InsertCurriculumPage, InsertCoursePage,
                  InsertTopicPage, InsertStudentGrades):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont == SearchCurriculumPage:
            frame.updatecurrlist()
        if cont == SearchCoursePage:
            frame.updatecourselist()
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
        self.coveragerror = tk.Label(self, text="Incorrect value entered for "
                                              "Coverage. Valid values are Extensive, Inclusive, Basic-plus, Basic, "
                                              "Unsatisfactory, or Substandard", fg='red')

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
            if self.coveragerror.winfo_ismapped():
                self.coveragerror.pack_forget()
            self.errorlabel.pack()
        elif (coverage != "Extensive" and coverage != "Inclusive" and coverage != "Basic-plus" and coverage != "Basic"
              and coverage != "Unsatisfactory" and coverage != "Substandard"):
            if self.errorlabel.winfo_ismapped():
                self.errorlabel.pack_forget()
            self.coveragerror.pack()
        else:
            self.nametext.delete(0, 'end')
            self.headidtext.delete(0, 'end')
            self.headname.delete(0, 'end')
            self.totcreditstext.delete(0, 'end')
            self.maxunitstext.delete(0, 'end')
            self.coveragetext.delete(0, 'end')
            self.numgoalstext.delete(0, 'end')
            global HOURS
            global CURRICULUM
            HOURS = totcred
            CURRICULUM = name
            array = [name, id, headname, totcred, maxunits, coverage, numgoals]
            insertcurriculum(array)
            if self.errorlabel.winfo_ismapped():
                self.errorlabel.pack_forget()
            if self.coveragerror.winfo_ismapped():
                self.coveragerror.pack_forget()
            updatecurriculums()
            controller.show_frame(InsertCoursePage)

    def backtostart(self, controller):
        self.nametext.delete(0, 'end')
        self.headidtext.delete(0, 'end')
        self.headname.delete(0, 'end')
        self.totcreditstext.delete(0, 'end')
        self.maxunitstext.delete(0, 'end')
        self.coveragetext.delete(0, 'end')
        self.numgoalstext.delete(0, 'end')
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
        self.labelCTopics = tk.Label(self)
        self.labelCCourses = tk.Label(self)

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

        temptopics = getcurriculumtopics(self.curriculum.get())
        topics = ""
        for topic in temptopics:
            topics += str(topic[0]) + "\n"

        tempcourses = getcurriculumcourses(self.curriculum.get())
        courses = ""
        for course in tempcourses:
            courses += course[0] + "\n"

        if self.labelCName.winfo_ismapped():
            self.labelCName.pack_forget()
            self.labelCID.pack_forget()
            self.labelCHeadName.pack_forget()
            self.labelCCred.pack_forget()
            self.labelmaxCUnits.pack_forget()
            self.labelCCoverage.pack_forget()
            self.labelCNumGoals.pack_forget()
            self.labelCTopics.pack_forget()
            self.labelCCourses.pack_forget()

        self.labelCName = tk.Label(self, text="Name: " + name)
        self.labelCID = tk.Label(self, text="Head ID: " + str(headID))
        self.labelCHeadName = tk.Label(self, text="Head Name: " + headName)
        self.labelCCred = tk.Label(self, text="Total Credits: " + str(totCredits))
        self.labelmaxCUnits = tk.Label(self, text="Max Units: " + str(maxUnits))
        self.labelCCoverage = tk.Label(self, text="Coverage: " + coverage)
        self.labelCNumGoals = tk.Label(self, text="Number of Goals: " + str(numGoals))
        self.labelCTopics = tk.Label(self, text="Topics:\n" + topics)
        self.labelCCourses = tk.Label(self, text="Courses:\n" + courses)

        self.labelCName.pack()
        self.labelCID.pack()
        self.labelCCred.pack()
        self.labelmaxCUnits.pack()
        self.labelCCoverage.pack()
        self.labelCNumGoals.pack()
        self.labelCTopics.pack()
        self.labelCCourses.pack()

    def gotostartpage(self, controller):
        if self.labelCName.winfo_ismapped():
            self.labelCName.pack_forget()
            self.labelCID.pack_forget()
            self.labelCCred.pack_forget()
            self.labelmaxCUnits.pack_forget()
            self.labelCCoverage.pack_forget()
            self.labelCNumGoals.pack_forget()
            self.labelCTopics.pack_forget()
            self.labelCCourses.pack_forget()
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
        global CURRICULUMS
        size = len(CURRICULUMS)
        names = [tk.Label(self)] * size
        headnames = [tk.Label(self)] * size
        required = [tk.Label(self)] * size
        optional = [tk.Label(self)] * size
        totalhours = [tk.Label(self)] * size

        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        for x in range(0, size):
            names[x] = tk.Label(self, text="Name: " + CURRICULUMS[x])
            names[x].pack()
            headname = getcurriculumhead(CURRICULUMS[x])
            headnames[x] = tk.Label(self, text="Head Name: " + headname[0][0])
            headnames[x].pack()
            reqandopt = getrequiredcount(CURRICULUMS[x])
            required[x] = tk.Label(self, text="Required Courses: " + str(reqandopt[0][0]))
            optional[x] = tk.Label(self, text="Optional Courses: " + str(reqandopt[1][0]))
            totcredits = getcurriculumcredits(CURRICULUMS[x])
            totalhours[x] = tk.Label(self, text="Total Credit Hours: " + str(totcredits))
            required[x].pack()
            optional[x].pack()
            totalhours[x].pack()

        button = tk.Button(self, text="Back to Start Page",
                           command=lambda: controller.show_frame(StartPage))

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

        global CURRICULUMS
        years = getyears()
        curriculum = ttk.Combobox(self, values=CURRICULUMS)
        semesterStart = ttk.Combobox(self, values=["Spring", "Summer", "Fall", "Winter"])
        semesterEnd = ttk.Combobox(self, values=["Spring", "Summer", "Fall", "Winter"])
        yearStart = ttk.Combobox(self, values=years)
        yearEnd = ttk.Combobox(self, values=years)
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
        self.labelCCurriculum = tk.Label(self)

        updatecourses()

        global COURSES
        self.course = ttk.Combobox(self, values=COURSES)
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

        tempcurric = getcoursecurriculum(self.course.get())
        curriculum = ""
        for curric in tempcurric:
            curriculum += curric[0] + "\n"

        if self.labelCName.winfo_ismapped():
            self.labelCName.pack_forget()
            self.labelCCode.pack_forget()
            self.labelCNum.pack_forget()
            self.labelCHours.pack_forget()
            self.labelCDesc.pack_forget()
            self.labelCCurriculum.pack_forget()

        self.labelCName = tk.Label(self, text="Name: " + name)
        self.labelCCode = tk.Label(self, text="Course Code: " + code)
        self.labelCNum = tk.Label(self, text="Course Number: " + str(num))
        self.labelCHours = tk.Label(self, text="Credit Hours: " + str(hours))
        self.labelCDesc = tk.Label(self, text="Description: " + desc)
        self.labelCCurriculum = tk.Label(self, text="Curriculum:\n" + curriculum)

        self.labelCName.pack()
        self.labelCCode.pack()
        self.labelCNum.pack()
        self.labelCHours.pack()
        self.labelCDesc.pack()
        self.labelCCurriculum.pack()

    def gotostartpage(self, controller):
        if self.labelCName.winfo_ismapped():
            self.labelCName.pack_forget()
            self.labelCCode.pack_forget()
            self.labelCNum.pack_forget()
            self.labelCHours.pack_forget()
            self.labelCDesc.pack_forget()
            self.labelCCurriculum.pack_forget()
        controller.show_frame(StartPage)

    def updatecourselist(self):
        global COURSES
        self.course.pack_forget()
        self.course = ttk.Combobox(self, values=COURSES)
        self.course.pack()


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

        vcmd = (self.register(self.validateint))
        self.nametext = tk.Entry(self)
        self.codetext = tk.Entry(self)
        self.coursenumtext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.hourstext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.desctext = tk.Text(self)
        self.var = tk.IntVar()
        self.optional = tk.Checkbutton(self, text="Optional", variable=self.var)

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
        self.optional.pack()
        insert.pack(side=tk.BOTTOM)

    def insertpressed(self, controller):
        name = self.nametext.get()
        code = self.codetext.get()
        coursenum = self.coursenumtext.get()
        hours = self.hourstext.get()
        desc = self.desctext.get(1.0, tk.END)

        if not name or not code or not coursenum or not hours or not desc:
            self.errorlabel.pack()
        else:
            self.nametext.delete(0, 'end')
            self.codetext.delete(0, 'end')
            self.coursenumtext.delete(0, 'end')
            self.hourstext.delete(0, 'end')
            self.desctext.delete('1.0', 'end')
            global TEMPHOURS
            global HOURS
            global CURRICULUM
            TEMPHOURS += int(hours)
            array = [name, code, coursenum, hours, desc]
            insertcourse(array)

            currcourse = [CURRICULUM, name, self.var.get()]
            insertcurriculumcourses(currcourse)
            if self.errorlabel.winfo_ismapped():
                self.errorlabel.pack_forget()
            if int(TEMPHOURS) >= int(HOURS):
                TEMPHOURS = 0
                HOURS = 0
                controller.show_frame(StartPage)

    def backtostart(self, controller):
        self.nametext.delete(0, 'end')
        self.codetext.delete(0, 'end')
        self.coursenumtext.delete(0, 'end')
        self.hourstext.delete(0, 'end')
        self.desctext.delete('1.0', 'end')
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

        self.labelname = tk.Label(self)
        self.labelcode = tk.Label(self)
        self.labelnum = tk.Label(self)
        self.labelhours = tk.Label(self)
        self.labeldesc = tk.Label(self)
        self.semester = [tk.Label(self)]
        self.year = [tk.Label(self)]
        self.section = [tk.Label(self)]
        self.aplus = [tk.Label(self)]
        self.a = [tk.Label(self)]
        self.aminus = [tk.Label(self)]
        self.bplus = [tk.Label(self)]
        self.b = [tk.Label(self)]
        self.bminus = [tk.Label(self)]
        self.cplus = [tk.Label(self)]
        self.c = [tk.Label(self)]
        self.cminus = [tk.Label(self)]
        self.dplus = [tk.Label(self)]
        self.d = [tk.Label(self)]
        self.dminus = [tk.Label(self)]
        self.f = [tk.Label(self)]
        self.w = [tk.Label(self)]
        self.i = [tk.Label(self)]

        global CURRICULUMS
        global COURSES
        self.curriculum = ttk.Combobox(self, values=CURRICULUMS)
        self.course = ttk.Combobox(self, values=COURSES)
        button1 = tk.Button(self, text="Search", command=lambda: self.searchpressed())
        button2 = tk.Button(self, text="Back to Start Page",
                            command=lambda: self.backtostart(controller))

        labelCurr.pack(side=tk.TOP)
        self.curriculum.pack(side=tk.TOP)
        labelCourse.pack(side=tk.TOP)
        self.course.pack(side=tk.TOP)
        button1.pack(side=tk.BOTTOM)
        button2.pack(side=tk.BOTTOM)

    def searchpressed(self):
        coursename = getcurriculumcourse(self.curriculum.get(), self.course.get())[0]
        print(coursename[0])
        course = getcourse(coursename[1])[0]
        print(course)

        sections = getcoursesections(course[0])
        size = len(sections)

        if self.labelname.winfo_ismapped():
            self.labelname.pack_forget()
            self.labelcode.pack_forget()
            self.labelnum.pack_forget()
            self.labelhours.pack_forget()
            self.labeldesc.pack_forget()
            for x in range(0, len(self.aplus)):
                self.semester[x].pack_forget()
                self.year[x].pack_forget()
                self.section[x].pack_forget()
                self.aplus[x].pack_forget()
                self.a[x].pack_forget()
                self.aminus[x].pack_forget()
                self.bplus[x].pack_forget()
                self.b[x].pack_forget()
                self.bminus[x].pack_forget()
                self.cplus[x].pack_forget()
                self.c[x].pack_forget()
                self.cminus[x].pack_forget()
                self.dplus[x].pack_forget()
                self.d[x].pack_forget()
                self.dminus[x].pack_forget()
                self.f[x].pack_forget()
                self.w[x].pack_forget()
                self.i[x].pack_forget()

        self.labelname = tk.Label(self, text="Name: " + course[0])
        self.labelcode = tk.Label(self, text="Sub Code: " + course[1])
        self.labelnum = tk.Label(self, text="Course Number: " + str(course[2]))
        self.labelhours = tk.Label(self, text="Credit Hours: " + str(course[3]))
        self.labeldesc = tk.Label(self, text="Description: " + course[4])

        self.labelname.pack()
        self.labelcode.pack()
        self.labelnum.pack()
        self.labelhours.pack()
        self.labeldesc.pack()

        self.semester = [tk.Label(self)] * size
        self.year = [tk.Label(self)] * size
        self.section = [tk.Label(self)] * size
        self.aplus = [tk.Label(self)] * size
        self.a = [tk.Label(self)] * size
        self.aminus = [tk.Label(self)] * size
        self.bplus = [tk.Label(self)] * size
        self.b = [tk.Label(self)] * size
        self.bminus = [tk.Label(self)] * size
        self.cplus = [tk.Label(self)] * size
        self.c = [tk.Label(self)] * size
        self.cminus = [tk.Label(self)] * size
        self.dplus = [tk.Label(self)] * size
        self.d = [tk.Label(self)] * size
        self.dminus = [tk.Label(self)] * size
        self.f = [tk.Label(self)] * size
        self.w = [tk.Label(self)] * size
        self.i = [tk.Label(self)] * size

        for x in range(0, size):
            self.semester[x] = tk.Label(self, text="Semester: " + sections[x][0])
            self.year[x] = tk.Label(self, text="Year: " + sections[x][1])
            self.section[x] = tk.Label(self, text="Section: " + sections[x][2])
            self.aplus[x] = tk.Label(self, text="A Plus': " + sections[x][4])
            self.a[x] = tk.Label(self, text="As: " + sections[x][4])
            self.aminus[x] = tk.Label(self, text="A Minus': " + sections[x][4])
            self.bplus[x] = tk.Label(self, text="B Plus': " + sections[x][4])
            self.b[x] = tk.Label(self, text="Bs: " + sections[x][4])
            self.bminus[x] = tk.Label(self, text="B Minus': " + sections[x][4])
            self.cplus[x] = tk.Label(self, text="C Plus': " + sections[x][4])
            self.c[x] = tk.Label(self, text="Cs: " + sections[x][4])
            self.cminus[x] = tk.Label(self, text="C Minus': " + sections[x][4])
            self.dplus[x] = tk.Label(self, text="D Plus': " + sections[x][4])
            self.d[x] = tk.Label(self, text="Ds: " + sections[x][4])
            self.dminus[x] = tk.Label(self, text="D Minus': " + sections[x][4])
            self.f[x] = tk.Label(self, text="Fs: " + sections[x][4])
            self.w[x] = tk.Label(self, text="Withdraws: " + sections[x][4])
            self.i[x] = tk.Label(self, text="Is: " + sections[x][4])

            self.semester[x].pack()
            self.year[x].pack()
            self.section[x].pack()
            self.aplus[x].pack()
            self.a[x].pack()
            self.aminus[x].pack()
            self.bplus[x].pack()
            self.b[x].pack()
            self.bminus[x].pack()
            self.cplus[x].pack()
            self.c[x].pack()
            self.cminus[x].pack()
            self.dplus[x].pack()
            self.d[x].pack()
            self.dminus[x].pack()
            self.f[x].pack()
            self.w[x].pack()
            self.i[x].pack()

    def backtostart(self, controller):
        if self.labelname.winfo_ismapped():
            self.labelname.pack_forget()
            self.labelcode.pack_forget()
            self.labelnum.pack_forget()
            self.labelhours.pack_forget()
            self.labeldesc.pack_forget()
            for x in range(0, len(self.aplus)):
                self.semester[x].pack_forget()
                self.year[x].pack_forget()
                self.section[x].pack_forget()
                self.aplus[x].pack_forget()
                self.a[x].pack_forget()
                self.aminus[x].pack_forget()
                self.bplus[x].pack_forget()
                self.b[x].pack_forget()
                self.bminus[x].pack_forget()
                self.cplus[x].pack_forget()
                self.c[x].pack_forget()
                self.cminus[x].pack_forget()
                self.dplus[x].pack_forget()
                self.d[x].pack_forget()
                self.dminus[x].pack_forget()
                self.f[x].pack_forget()
                self.w[x].pack_forget()
                self.i[x].pack_forget()

        controller.show_frame(StartPage)


class InsertTopicPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Topic Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        vcmd = (self.register(self.validateint))
        vcmd2 = (self.register(self.validatefloat), '%S', '%P')
        curriclabel = tk.Label(self, text="Curriculum")
        self.currictext = tk.Entry(self)
        topiclabel = tk.Label(self, text="Topic ID")
        self.topicidtext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        topicnamelabel = tk.Label(self, text="Topic Name")
        self.topicnametext = tk.Entry(self)
        levellabel = tk.Label(self, text="Level")
        self.leveltext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        subjectlabel = tk.Label(self, text="Subject Area")
        self.subjecttext = tk.Entry(self)
        unitslabel = tk.Label(self, text="Units")
        self.unitstext = tk.Entry(self, validate='all', validatecommand=vcmd2)
        self.errorlabel = tk.Label(self, text="One or more fields left blank", fg='red')
        self.curricerror = tk.Label(self, text="Curriculum not valid", fg='red')
        self.unitserror = tk.Label(self, text="Units above max units", fg='red')

        insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        button = tk.Button(self, text="Back to Start Page",
                           command=lambda: self.backtostart(controller))

        curriclabel.pack()
        self.currictext.pack()
        topiclabel.pack()
        self.topicidtext.pack()
        topicnamelabel.pack()
        self.topicnametext.pack()
        levellabel.pack()
        self.leveltext.pack()
        subjectlabel.pack()
        self.subjecttext.pack()
        unitslabel.pack()
        self.unitstext.pack()
        insert.pack(side=tk.BOTTOM)
        button.pack(side=tk.BOTTOM)

    def insertpressed(self, controller):
        curric = self.currictext.get()
        topicid = self.topicidtext.get()
        topicname = self.topicnametext.get()
        level = self.leveltext.get()
        subject = self.subjecttext.get()
        units = self.unitstext.get()

        global CURRICULUMS

        if not curric or not topicid or not topicname or not level or not subject or not units:
            if self.curricerror.winfo_ismapped():
                self.curricerror.pack_forget()
            if self.unitserror.winfo_ismapped():
                self.unitserror.pack_forget()
            self.errorlabel.pack()
        elif curric not in CURRICULUMS:
            if self.errorlabel.winfo_ismapped():
                self.errorlabel.pack_forget()
            if self.unitserror.winfo_ismapped():
                self.unitserror.pack_forget()
            self.curricerror.pack()
        elif float(units) > float(getcurriculum(curric)[0][3]):
            if self.errorlabel.winfo_ismapped():
                self.errorlabel.pack_forget()
            if self.curricerror.winfo_ismapped():
                self.curricerror.pack_forget()
            self.unitserror.pack()
        else:
            self.currictext.delete(0, 'end')
            self.topicidtext.delete(0, 'end')
            self.leveltext.delete(0, 'end')
            self.subjecttext.delete(0, 'end')
            self.unitstext.delete(0, 'end')

            topic = [topicid, topicname]
            inserttopics(topic)

            array = [curric, topicid, topicname, level, subject, units]
            insertcurriculumtopics(array)

            if self.errorlabel.winfo_ismapped():
                self.errorlabel.pack_forget()
            controller.show_frame(StartPage)

    def backtostart(self, controller):
        if self.curricerror.winfo_ismapped():
            self.curricerror.pack_forget()
        if self.errorlabel.winfo_ismapped():
            self.errorlabel.pack_forget()
        self.currictext.delete(0, 'end')
        self.topicidtext.delete(0, 'end')
        self.leveltext.delete(0, 'end')
        self.subjecttext.delete(0, 'end')
        self.unitstext.delete(0, 'end')
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


class InsertStudentGrades(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Student Grades Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        vcmd = (self.register(self.validateint))
        self.limitvalue = tk.StringVar()
        self.limitvalue.trace('w', self.limitsize)

        semesterlabel = tk.Label(self, text="Semester")
        self.semesterbox = ttk.Combobox(self, values=["Spring", "Summer", "Fall", "Winter"])
        yearlabel = tk.Label(self, text="Year")
        self.yearentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        sectionidlabel = tk.Label(self, text="Section ID")
        self.sectionidentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'), textvariable=self.limitvalue)
        coursenamelabel = tk.Label(self, text="Course Name")
        self.coursenameentry = tk.Entry(self)

        apluslabel = tk.Label(self, text="Number of A Plus")
        alabel = tk.Label(self, text="Number of A")
        aminuslabel = tk.Label(self, text="Number of A Minus")
        bpluslabel = tk.Label(self, text="Number of B Plus")
        blabel = tk.Label(self, text="Number of B")
        bminuslabel = tk.Label(self, text="Number of B Minus")
        cpluslabel = tk.Label(self, text="Number of C Plus")
        clabel = tk.Label(self, text="Number of C")
        cminuslabel = tk.Label(self, text="Number of C Minus")
        dpluslabel = tk.Label(self, text="Number of D Plus")
        dlabel = tk.Label(self, text="Number of D")
        dminuslabel = tk.Label(self, text="Number of D Minus")
        flabel = tk.Label(self, text="Number of F")
        wlabel = tk.Label(self, text="Number of Withdrawal")
        ilabel = tk.Label(self, text="Number of I")

        self.aplusentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.bplusentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.cplusentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.dplusentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.aminusentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.bminusentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.cminusentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.dminusentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.aentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.bentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.centry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.dentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.fentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.wentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.ientry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))

        insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        button = tk.Button(self, text="Back to Start Page",
                           command=lambda: self.backtostart(controller))
        self.errorlabel = tk.Label(self, text="One or more fields were left blank")

        semesterlabel.pack()
        self.semesterbox.pack()
        yearlabel.pack()
        self.yearentry.pack()
        sectionidlabel.pack()
        self.sectionidentry.pack()
        coursenamelabel.pack()
        self.coursenameentry.pack()

        apluslabel.pack()
        self.aplusentry.pack()
        alabel.pack()
        self.aentry.pack()
        aminuslabel.pack()
        self.aminusentry.pack()
        bpluslabel.pack()
        self.bplusentry.pack()
        blabel.pack()
        self.bentry.pack()
        bminuslabel.pack()
        self.bminusentry.pack()
        cpluslabel.pack()
        self.cplusentry.pack()
        clabel.pack()
        self.centry.pack()
        cminuslabel.pack()
        self.cminusentry.pack()
        dpluslabel.pack()
        self.dplusentry.pack()
        dlabel.pack()
        self.dentry.pack()
        dminuslabel.pack()
        self.dminusentry.pack()
        flabel.pack()
        self.fentry.pack()
        wlabel.pack()
        self.wentry.pack()
        ilabel.pack()
        self.ientry.pack()

        insert.pack(side=tk.BOTTOM)
        button.pack(side=tk.BOTTOM)

    def insertpressed(self, controller):
        semester = self.semesterbox.get()
        year = self.yearentry.get()
        sectionid = self.sectionidentry.get()
        coursename = self.coursenameentry.get()
        aplus = self.aplusentry.get()
        a = self.aentry.get()
        aminus = self.aminusentry.get()
        bplus = self.bplusentry.get()
        b = self.bentry.get()
        bminus = self.bminusentry.get()
        cplus = self.cplusentry.get()
        c = self.centry.get()
        cminus = self.cminusentry.get()
        dplus = self.dplusentry.get()
        d = self.dentry.get()
        dminus = self.dminusentry.get()
        f = self.fentry.get()
        withdraw = self.wentry.get()
        i = self.ientry.get()

        if (not semester or not year or not sectionid or not coursename or not aplus or not a
                or not aminus or not bplus or not b or not bminus or not cplus or not c or not cminus
                or not dplus or not d or not dminus or not f or not withdraw or not i):
            self.errorlabel.pack()
        else:
            enrolled = (int(aplus) + int(a) + int(aminus) + int(bplus) + int(b) + int(bminus) + int(cplus) + int(c) +
                        int(cminus) + int(dplus) + int(d) + int(dminus) + int(f) + int(withdraw) + int(i))
            array = [semester, year, sectionid, enrolled, "", ""]
            insertcoursesections(array)
            array = [semester, year, sectionid, coursename, aplus, a, aminus, bplus, b, bminus, cplus,
                     c, cminus, dplus, d, dminus, f, withdraw, i]
            insertstudentgrades(array)

            self.yearentry.delete(0, 'end')
            self.sectionidentry.delete(0, 'end')
            self.coursenameentry.delete(0, 'end')
            self.aplusentry.delete(0, 'end')
            self.aentry.delete(0, 'end')
            self.aminusentry.delete(0, 'end')
            self.bplusentry.delete(0, 'end')
            self.bentry.delete(0, 'end')
            self.bminusentry.delete(0, 'end')
            self.cplusentry.delete(0, 'end')
            self.centry.delete(0, 'end')
            self.cminusentry.delete(0, 'end')
            self.dplusentry.delete(0, 'end')
            self.dentry.delete(0, 'end')
            self.dminusentry.delete(0, 'end')
            self.fentry.delete(0, 'end')
            self.wentry.delete(0, 'end')
            self.ientry.delete(0, 'end')

            controller.show_frame(StartPage)

    def backtostart(self, controller):
        self.yearentry.delete(0, 'end')
        self.sectionidentry.delete(0, 'end')
        self.coursenameentry.delete(0, 'end')
        self.aplusentry.delete(0, 'end')
        self.aentry.delete(0, 'end')
        self.aminusentry.delete(0, 'end')
        self.bplusentry.delete(0, 'end')
        self.bentry.delete(0, 'end')
        self.bminusentry.delete(0, 'end')
        self.cplusentry.delete(0, 'end')
        self.centry.delete(0, 'end')
        self.cminusentry.delete(0, 'end')
        self.dplusentry.delete(0, 'end')
        self.dentry.delete(0, 'end')
        self.dminusentry.delete(0, 'end')
        self.fentry.delete(0, 'end')
        self.wentry.delete(0, 'end')
        self.ientry.delete(0, 'end')

        controller.show_frame(StartPage)

    def limitsize(self, *args):
        value = self.limitvalue.get()
        if len(value) > 3:
            self.limitvalue.set(value[:3])

    def validateint(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False


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
        button7 = tk.Button(self, text="Insert Curriculum Topic", command=lambda:
                            controller.show_frame(InsertTopicPage))
        button8 = tk.Button(self, text="Insert Student Grades", command=lambda:
                            controller.show_frame(InsertStudentGrades))

        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        button5.pack()
        button6.pack()
        button7.pack()
        button8.pack()
