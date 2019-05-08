import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import Scrollbar
from Curriculum import *

LARGE_FONT = ("Verdana", 12)
CURRICULUMS = []
COURSES = []
GOALS = []


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


def updategoals():
    global GOALS
    tempgoals = getgoals()
    size = len(tempgoals)
    GOALS = [None] * int(size)
    for x in range(0, size):
        GOALS[x] = tempgoals[x][0]


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
        updategoals()

        for F in (StartPage, SearchCurriculumPage, SearchCoursePage,
                  SearchCourseByCurriculumPage, CurriculumSemesterRangeSearch,
                  CurriculumDashboardPage, InsertCurriculumPage, InsertCoursePage,
                  InsertTopicPage, InsertStudentGrades, InsertGoalPage,
                  InsertCurriculumCoursePage, InsertCourseGoalPage, InsertGoalGrades,
                  InsertCourseSectionsPage, InsertCourseTopicsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont == SearchCurriculumPage or cont == InsertGoalPage:
            frame.updatecurrlist()
        if cont == SearchCoursePage or cont == InsertStudentGrades:
            frame.updatecourselist()
        if cont == SearchCourseByCurriculumPage:
            frame.updatecomboboxes()
        frame.tkraise()


class InsertCurriculumPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Curriculum Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.labelCName = tk.Label(self, text="Name")
        self.labelCID = tk.Label(self, text="Head ID")
        self.labelCHeadName = tk.Label(self, text="Head Name")
        self.labelCCred = tk.Label(self, text="Total Credits")
        self.labelmaxCUnits = tk.Label(self, text="Max Units")
        self.insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        self.button = tk.Button(self, text="Back to Start Page",
                                command=lambda: self.backtostart(controller))

        vcmd = (self.register(self.validateint))
        vcmd2 = (self.register(self.validatefloat), '%S', '%P')
        self.nametext = tk.Entry(self)
        self.headidtext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.headname = tk.Entry(self)
        self.totcreditstext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.maxunitstext = tk.Entry(self, validate='all', validatecommand=vcmd2)

        self.errorlabel = tk.Label(self, text="One or more fields were left blank", fg='red')

        self.labelCName.pack()
        self.nametext.pack()
        self.labelCID.pack()
        self.headidtext.pack()
        self.labelCHeadName.pack()
        self.headname.pack()
        self.labelCCred.pack()
        self.totcreditstext.pack()
        self.labelmaxCUnits.pack()
        self.maxunitstext.pack()

        self.insert.pack(side=tk.BOTTOM)
        self.button.pack(side=tk.BOTTOM)


    def insertpressed(self, controller):
        name = self.nametext.get()
        id = self.headidtext.get()
        headname = self.headname.get()
        totcred = self.totcreditstext.get()
        maxunits = self.maxunitstext.get()

        if not name or not id or not headname or not totcred or not maxunits:
            self.errorlabel.pack()
        else:
            array = [name, id, headname, totcred, maxunits]
            insertcurriculum(array)
            updatecurriculums()
            self.backtostart(controller)

    def backtostart(self, controller):
        self.nametext.delete(0, 'end')
        self.headidtext.delete(0, 'end')
        self.headname.delete(0, 'end')
        self.totcreditstext.delete(0, 'end')
        self.maxunitstext.delete(0, 'end')
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

        self.labelCName = tk.Label(self)
        self.labelCID = tk.Label(self)
        self.labelCHeadName = tk.Label(self)
        self.labelCCred = tk.Label(self)
        self.labelmaxCUnits = tk.Label(self)
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
            self.labelCTopics.pack_forget()
            self.labelCCourses.pack_forget()

        self.labelCName = tk.Label(self, text="Name: " + name)
        self.labelCID = tk.Label(self, text="Head ID: " + str(headID))
        self.labelCHeadName = tk.Label(self, text="Head Name: " + headName)
        self.labelCCred = tk.Label(self, text="Total Credits: " + str(totCredits))
        self.labelmaxCUnits = tk.Label(self, text="Max Units: " + str(maxUnits))
        self.labelCTopics = tk.Label(self, text="Topics:\n" + topics)
        self.labelCCourses = tk.Label(self, text="Courses:\n" + courses)

        self.labelCName.pack()
        self.labelCID.pack()
        self.labelCCred.pack()
        self.labelmaxCUnits.pack()
        self.labelCTopics.pack()
        self.labelCCourses.pack()

    def gotostartpage(self, controller):
        if self.labelCName.winfo_ismapped():
            self.labelCName.pack_forget()
            self.labelCID.pack_forget()
            self.labelCCred.pack_forget()
            self.labelmaxCUnits.pack_forget()
            self.labelCTopics.pack_forget()
            self.labelCCourses.pack_forget()
        controller.show_frame(StartPage)

    def updatecurrlist(self):
        global CURRICULUMS
        self.curriculum.config(values=CURRICULUMS)


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
        self.course.config(values=COURSES)


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

        insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        button = tk.Button(self, text="Back to Start Page",
                           command=lambda: self.backtostart(controller))

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
            insertcourse(array)
            updatecourses()
            self.backtostart(controller)

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


class InsertCurriculumCoursePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Curriculum Course Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        global CURRICULUMS
        global COURSES
        self.curriculumlabel = tk.Label(self, text="Curriculum")
        self.courselabel = tk.Label(self, text="Course")
        self.curriculums = ttk.Combobox(self, values=CURRICULUMS)
        self.courses = ttk.Combobox(self, values=COURSES)
        self.var = tk.IntVar()
        self.optional = tk.Checkbutton(self, text="Optional", variable=self.var)

        self.curriculumlabel.pack()
        self.curriculums.pack()
        self.courselabel.pack()
        self.courses.pack()
        self.optional.pack()


class SearchCourseByCurriculumPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search Course by Curriculum Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.labelCurr = tk.Label(self, text="Curriculum")
        self.labelCourse = tk.Label(self, text="Course")

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
        self.curriculum.bind("<<ComboboxSelected>>", self.updatecourse)
        self.course = ttk.Combobox(self, values=COURSES)
        self.button1 = tk.Button(self, text="Search", command=lambda: self.searchpressed())
        self.button2 = tk.Button(self, text="Back to Start Page",
                            command=lambda: self.backtostart(controller))

        self.labelCurr.pack()
        self.curriculum.pack()
        self.labelCourse.pack()
        self.course.pack()
        self.button1.pack(side=tk.BOTTOM)
        self.button2.pack(side=tk.BOTTOM)

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

    def updatecomboboxes(self):
        global CURRICULUMS
        global COURSES
        self.curriculum.config(values=CURRICULUMS)
        self.course.config(values=COURSES)

    def updatecourse(self, *args):
        tempcourses = getcurriculumcourses(self.curriculum.get())
        size = len(tempcourses)
        courses = [None] * int(size)
        for x in range(0, size):
            courses[x] = tempcourses[x][0]
        self.course.config(values=courses)


class InsertCurriculumTopicPage(tk.Frame):
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
            topic = [topicid, topicname]
            inserttopics(topic)

            array = [curric, topicid, topicname, level, subject, units]
            insertcurriculumtopics(array)

            self.backtostart(controller)

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
        global COURSES

        vcmd = (self.register(self.validateint))
        self.limitvalue = tk.StringVar()
        self.limitvalue.trace('w', self.limitsize)

        self.semesterlabel = tk.Label(self, text="Semester")
        self.semesterbox = ttk.Combobox(self, values=["Spring", "Summer", "Fall", "Winter"])
        self.yearlabel = tk.Label(self, text="Year")
        self.yearentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.sectionidlabel = tk.Label(self, text="Section ID")
        self.sectionidentry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'), textvariable=self.limitvalue)
        self.coursenamelabel = tk.Label(self, text="Course Name")
        self.coursenamebox = ttk.Combobox(self, values=COURSES)

        self.apluslabel = tk.Label(self, text="Number of A Plus")
        self.alabel = tk.Label(self, text="Number of A")
        self.aminuslabel = tk.Label(self, text="Number of A Minus")
        self.bpluslabel = tk.Label(self, text="Number of B Plus")
        self.blabel = tk.Label(self, text="Number of B")
        self.bminuslabel = tk.Label(self, text="Number of B Minus")
        self.cpluslabel = tk.Label(self, text="Number of C Plus")
        self.clabel = tk.Label(self, text="Number of C")
        self.cminuslabel = tk.Label(self, text="Number of C Minus")
        self.dpluslabel = tk.Label(self, text="Number of D Plus")
        self.dlabel = tk.Label(self, text="Number of D")
        self.dminuslabel = tk.Label(self, text="Number of D Minus")
        self.flabel = tk.Label(self, text="Number of F")
        self.wlabel = tk.Label(self, text="Number of Withdrawal")
        self.ilabel = tk.Label(self, text="Number of I")

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

        self.insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        self.button = tk.Button(self, text="Back to Start Page",
                           command=lambda: self.backtostart(controller))
        self.errorlabel = tk.Label(self, text="One or more fields were left blank", fg='red')

    def insertpressed(self, controller):
        semester = self.semesterbox.get()
        year = self.yearentry.get()
        sectionid = self.sectionidentry.get()
        coursename = self.coursenamebox.get()
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

            self.backtostart(controller)

    def backtostart(self, controller):
        self.yearentry.delete(0, 'end')
        self.sectionidentry.delete(0, 'end')
        self.coursenamebox.delete(0, 'end')
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

    def updatecourselist(self):
        global COURSES
        self.coursenamebox.config(values=COURSES)


class InsertGoalPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Goal Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        labelcurr = tk.Label(self, text="Curriculum")
        labeldescription = tk.Label(self, text="Description")
        labelid = tk.Label(self, text="Goal ID")

        vcmd = (self.register(self.validateint))

        self.identry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.desctext = tk.Text(self)
        self.curriculumbox = ttk.Combobox(self, values=CURRICULUMS)

        insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        button = tk.Button(self, text="Back to Start Page",
                           command=lambda: self.backtostart(controller))
        self.errorlabel = tk.Label(self, text="One or more fields were left blank", fg='red')

        labelid.pack()
        self.identry.pack()
        labeldescription.pack()
        self.desctext.pack()
        labelcurr.pack()
        self.curriculumbox.pack()
        insert.pack(side=tk.BOTTOM)
        button.pack(side=tk.BOTTOM)

    def validateint(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def insertpressed(self, controller):
        curr = self.curriculumbox.get()
        id = self.identry.get()
        description = self.desctext.get(1.0, 'end')

        if not curr or not id or not description:
            self.errorlabel.pack()
        else:
            array = [id, description, curr]
            insertgoal(array)

            self.backtostart(controller)

    def backtostart(self, controller):
        if self.errorlabel.winfo_ismapped():
            self.errorlabel.pack_forget()
        self.desctext.delete(1.0, 'end')
        self.identry.delete(0, 'end')
        controller.show_frame(StartPage)

    def updatecurrlist(self):
        global COURSES
        self.curriculumbox.pack_forget()
        self.curriculumbox = ttk.Combobox(self, values=CURRICULUMS)
        self.curriculumbox.pack()


class InsertCourseGoalPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Student Grades Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        global CURRICULUMS
        global COURSES
        global GOALS

        labelcurr = tk.Label(self, text="Curriculum")
        labelcourse = tk.Label(self, text="Course")
        labelid = tk.Label(self, text="Goal ID")

        self.curriculum = ttk.Combobox(self, values=CURRICULUMS)
        self.curriculum.bind("<<ComboboxSelected>>", self.updateothers)
        self.course = ttk.Combobox(self, values=COURSES)
        self.id = ttk.Combobox(self, values=GOALS)

        insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        button = tk.Button(self, text="Back to Start Page",
                           command=lambda: controller.show_frame(StartPage))
        self.errorlabel = tk.Label(self, text="One or more fields were left blank", fg='red')

        labelcurr.pack()
        self.curriculum.pack()
        labelcourse.pack()
        self.course.pack()
        labelid.pack()
        self.id.pack()
        insert.pack(side=tk.BOTTOM)
        button.pack(side=tk.BOTTOM)

    def insertpressed(self, controller):
        curr = self.curriculum.get()
        cour = self.course.get()
        id = self.id.get()

        if not curr or not id or not cour:
            self.errorlabel.pack()
        else:
            array = [curr, cour, id]
            insertcoursegoals(array)

            if self.errorlabel.winfo_ismapped():
                self.errorlabel.pack_forget()
            controller.show_frame(StartPage)

    def updateothers(self, *args):
        tempcourses = getcurriculumcourses(self.curriculum.get())
        size = len(tempcourses)
        courses = [None] * int(size)
        for x in range(0, size):
            courses[x] = tempcourses[x][0]
        self.course.config(values=courses)

        tempids = getcurricgoals(self.curriculum.get())
        size = len(tempids)
        ids = [None] * int(size)
        for x in range(0, size):
            ids[x] = tempids[x][0]
        self.id.config(values=ids)


class InsertTopicPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Student Grades Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        vcmd = (self.register(self.validateint))
        topiclabel = tk.Label(self, text="Topic ID")
        self.topicidtext = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        topicnamelabel = tk.Label(self, text="Topic Name")
        self.topicnametext = tk.Entry(self)

        topiclabel.pack()
        self.topicidtext.pack()
        topicnamelabel.pack()
        self.topicnametext.pack()


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
        button7 = tk.Button(self, text="Insert Curriculum Course", command=lambda:
                            controller.show_frame(InsertCurriculumCoursePage))
        button8 = tk.Button(self, text="Insert Curriculum Topic", command=lambda:
                            controller.show_frame(InsertTopicPage))
        button9 = tk.Button(self, text="Insert Student Grades", command=lambda:
                            controller.show_frame(InsertStudentGrades))
        button10 = tk.Button(self, text="Insert Goal", command=lambda:
                             controller.show_frame(InsertGoalPage))
        button11 = tk.Button(self, text="Insert Course Goal", command=lambda:
                             controller.show_frame(InsertCourseGoalPage))
        button12 = tk.Button(self, text="Insert Topic", command=lambda: controller.show_frame(InsertTopicPage))
        button12 = tk.Button(self, text="Insert Course Topic", command=lambda:
                             controller.show_frame(InsertCourseTopicsPage))
        button13 = tk.Button(self, text="Insert Course Section", command=lambda:
                             controller.show_frame(InsertCourseSectionsPage))
        button14 = tk.Button(self, text="Insert Goal Grades", command=lambda:
                             controller.show_frame(InsertGoalGrades))

        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        button5.pack()
        button6.pack()
        button7.pack()
        button8.pack()
        button9.pack()
        button10.pack()
        button11.pack()
        button12.pack()
        button13.pack()
        button14.pack()


class InsertCourseTopicsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Course Topics Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        global COURSES
        self.courseLabel = tk.Label(self, text="Course")
        self.courseBox = ttk.Combobox(self, values=COURSES)

        global CURRICULUMS
        self.curriculumLabel = tk.Label(self, text="Curriculum")
        self.curriculumBox = ttk.Combobox(self, values=CURRICULUMS)
        self.curriculumBox.bind("<<ComboboxSelected>>", self.updateothers)

        self.topicIDLabel = tk.Label(self, text="Topic ID")
        self.topicIDBox = ttk.Combobox(self)

        vcmd2 = (self.register(self.validatefloat), '%S', '%P')
        self.unitsLabel = tk.Label(self, text="Units")
        self.unitsEntry = tk.Entry(self, validate='all', validatecommand=vcmd2)

        self.insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        self.button = tk.Button(self, text="Back to Start Page",
                           command=lambda: self.backtostart(controller))

        self.errorlabel = tk.Label(self, text="One or more fields were left blank", fg='red')
    
        self.courseLabel.pack()
        self.courseBox.pack()

        self.curriculumLabel.pack()
        self.curriculumBox.pack()

        self.topicIDLabel.pack()
        self.topicIDBox.pack()
        
        self.unitsLabel.pack()
        self.unitsEntry.pack()
        
        self.insert.pack(side=tk.BOTTOM)
        self.button.pack(side=tk.BOTTOM)

    def validatefloat(self, text, P):
        if text in '0123456789.':
            try:
                float(P)
                return True
            except ValueError:
                return False
        else:
            return False

    def insertpressed(self, controller):
        curric = self.curriculumBox.get()
        course = self.courseBox.get()
        topicID = self.topicIDBox.get()
        units = self.unitsEntry.get()

        if not curric or not course or not topicID or not units:
            self.errorlabel.pack()
        else:
            array = [course, curric, topicID, units]
            insertcoursetopics(array)
            self.backtostart(controller)

    def backtostart(self, controller):
        self.curriculumBox.set('')
        self.topicIDBox.set('')
        self.unitsEntry.delete(0, 'end')
        controller.show_frame(StartPage)

    def updateothers(self, *args):
        tempcourses = getcurriculumcourses(self.curriculumBox.get())
        size = len(tempcourses)
        courses = [None] * int(size)
        for x in range(0, size):
            courses[x] = tempcourses[x][0]
        self.courseBox.config(values=courses)
        self.courseBox.set('')

        tempids = getcurriculumtopics(self.curriculumBox.get())
        size = len(tempids)
        ids = [None] * int(size)
        for x in range(0, size):
            ids[x] = tempids[x][0]
        self.topicIDBox.config(values=ids)
        self.topicIDBox.set('')

    
class InsertCourseSectionsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Course Sections Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.semesterLabel = tk.Label(self, text="Semester")
        self.semesterBox = ttk.Combobox(self, values=["Spring", "Summer",
                                                      "Fall", "Winter"])

        vcmd = (self.register(self.validateint)) 
        self.yearLabel = tk.Label(self, text="Year")
        self.yearEntry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))

        self.limitvalue = tk.StringVar()
        self.limitvalue.trace('w', self.limitsize)
        self.sectionIDLabel = tk.Label(self, text="Section ID")
        self.sectionIDEntry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'),
                                       textvariable=self.limitvalue)

        global COURSE
        self.courseLabel = tk.Label(self, text="Course")
        self.courseBox = ttk.Combobox(self, values=COURSES)

        self.enrolledLabel = tk.Label(self, text="Enrolled")                              
        self.enrolledEntry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))

        self.comOneLabel = tk.Label(self, text="Comment 1")
        self.comOneEntry = tk.Entry(self)

        self.comTwoLabel = tk.Label(self, text="Comment 2")    
        self.comTwoEntry = tk.Entry(self)

        self.insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        self.button = tk.Button(self, text="Back to Start Page",
                           command=lambda: self.backtostart(controller))

        self.errorlabel = tk.Label(self, text="One or more fields were left blank", fg='red')

        self.semesterLabel.pack()
        self.semesterBox.pack()

        self.yearLabel.pack()
        self.yearEntry.pack()                        

        self.enrolledLabel.pack()
        self.enrolledEntry.pack()

        self.comOneLabel.pack()
        self.comOneEntry.pack()

        self.comTwoLabel.pack()
        self.comTwoEntry.pack()
                                    
        self.insert.pack(side=tk.BOTTOM)
        self.button.pack(side=tk.BOTTOM)

    def validateint(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def limitsize(self, *args):
        value = self.limitvalue.get()
        if len(value) > 3:
            self.limitvalue.set(value[:3])

    def insertpressed(self, controller):
        semester = self.semesterBox.get()
        year = self.yearEntry.get()
        enrolled = self.enrolledEntry.get()
        comment1 = self.comOneEntry.get()
        comment2 = self.comTwoEntry.get()

        if not semester or not year or not enrolled or not comment1 or not comment2:
            self.errorlabel.pack()
        else:
            array = [semester, year, enrolled, comment1, comment2]
            insertcoursesections(array)
            self.backtostart(controller)

    def backtostart(self, controller):
        self.errorlabel.pack_forget()
        self.semesterBox.set('')
        self.yearEntry.delete(0, 'end')
        self.enrolledEntry.delete(0, 'end')
        self.comOneEntry.delete(0, 'end')
        self.comTwoEntry.delete(0, 'end')
        controller.show_frame(StartPage)


class InsertGoalGrades(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Goal Grades Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.semesterLabel = tk.Label(self, text="Semester")
        self.semesterBox = ttk.Combobox(self, values=["Spring", "Summer",
                                                      "Fall", "Winter"])
        
        vcmd = (self.register(self.validateint))         
        self.yearLabel = tk.Label(self, text="Year")
        self.yearEntry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))

        global COURSES
        self.courseLabel = tk.Label(self, text="Course")
        self.courseBox = ttk.Combobox(self, values=COURSES)

        self.sectionIDLabel = tk.Label(self, text="Section ID")
        self.sectionIDBox = ttk.Combobox(self)

        global GOALS
        self.goalIDLabel = tk.Label(self, text="Goal ID")
        self.goalIDBox = ttk.Combobox(self, values=GOALS)

        self.goalGradeLabel = tk.Label(self, text="Goal Grade")
        self.goalGradeEntry = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))

        self.insert = tk.Button(self, text="Insert", command=lambda: self.insertpressed(controller))
        self.button = tk.Button(self, text="Back to Start Page",
                           command=lambda: self.backtostart(controller))

        self.errorlabel = tk.Label(self, text="One or more fields were left blank", fg='red')

        self.semesterLabel.pack()
        self.semesterBox.pack()
                                       
        self.yearLabel.pack()
        self.yearEntry.pack()
                                   
        self.sectionIDLabel.pack()
        self.sectionIDBox.pack()
                                       
        self.courseLabel.pack()
        self.courseBox.pack()
                                       
        self.goalIDLabel.pack()
        self.goalIDBox.pack()

        self.goalGradeLabel.pack()
        self.goalGradeEntry.pack()

        self.insert.pack(side=tk.BOTTOM)
        self.button.pack(side=tk.BOTTOM)

    def validateint(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def insertpressed(self, controller):
        semester = self.semesterBox.get()
        year = self.yearEntry.get()
        section = self.sectionIDBox.get()
        course = self.courseBox.get()
        goalid = self.goalIDBox.get()
        goalgrade = self.goalGradeEntry.get()

        if not semester or not year or not section or not course or not goalid or not goalgrade:
            self.errorlabel.pack()
        else:
            array = [semester, year, section, course, goalid, goalgrade]

            insertgoalgrade(array)
            self.backtostart(controller)

    def backtostart(self, controller):
        self.errorlabel.pack()
        self.semesterBox.set('')
        self.yearEntry.delete(0, 'end')
        self.sectionIDBox.set('')
        self.courseBox.set('')
        self.goalIDBox.set('')
        self.goalGradeEntry.delete(0, 'end')
        controller.show_frame(StartPage)

    def updateoffcourse(self):
        getcoursegoals()