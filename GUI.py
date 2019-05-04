import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from tkinter import Canvas

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

        curriculum = ttk.Combobox(self, values=["Test", "Test2", "Testetc"])
        curriculum.current(0)
        button1 = tk.Button(self, text="Search")
        button2 = tk.Button(self, text="Back to Start Page",
                            command=lambda: controller.show_frame(StartPage))

        curriculum.pack(side=tk.TOP)
        button1.pack(side=tk.BOTTOM)
        button2.pack(side=tk.BOTTOM)


class SearchCoursePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search Course Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        course = ttk.Combobox(self, values=["Test", "Test2", "Testetc"])
        course.current(0)
        button1 = tk.Button(self, text="Search")
        button2 = tk.Button(self, text="Back to Start Page",
                            command=lambda: controller.show_frame(StartPage))

        course.pack(side=tk.TOP)
        button1.pack(side=tk.BOTTOM)
        button2.pack(side=tk.BOTTOM)


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
