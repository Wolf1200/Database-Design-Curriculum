import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from tkinter import Canvas
from Curriculum import *

LARGE_FONT = ("Verdana", 12)


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
                  CurriculumDashboardPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class SearchCurriculumPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search Curriculum Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        curriculums = getcurrentcurriculums()

        self.labelCName = ""
        self.labelCID = ""
        self.labelCCred = ""
        self.labelmaxCUnits = ""
        self.labelCCoverage = ""
        self.labelCNumGoals = ""

        self.curriculum = ttk.Combobox(self, values=curriculums)
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
        totCredits = info[2]
        maxUnits = info[3]
        coverage = info[4]
        numGoals = info[5]

        self.labelCName = tk.Label(self, text="Name: " + name)
        self.labelCID = tk.Label(self, text="Head ID: " + str(headID))
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


class SearchCoursePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search Course Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.labelCName = ""
        self.labelCCode = ""
        self.labelCNum = ""
        self.labelCHours = ""
        self.labelCDesc = ""

        courses = getcurrentcourses()

        self.course = ttk.Combobox(self, values=courses[0])
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

        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        button5.pack()
