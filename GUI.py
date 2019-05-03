import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)

class DatabaseGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, SearchCurriculumPage):
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
        button1 = tk.Button(self, text="Search")
        button2 = tk.Button(self, text="Back to Start Page",
                            command=lambda: controller.show_frame(StartPage))

        curriculum.pack(side=tk.TOP)
        button1.pack(side=tk.BOTTOM)
        button2.pack(side=tk.BOTTOM)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Curriculum Info", fg="red",
                            command=lambda:
                            controller.show_frame(SearchCurriculumPage))
        button2 = tk.Button(self, text="Course Info", fg="red")
        button3 = tk.Button(self, text="Course Sections by Curriculum",
                            fg="red")
        button4 = tk.Button(self, text="Course Outcomes", fg="red")
        button5 = tk.Button(self, text="Curriculum Dashboard", fg="red")

        button5.pack(side=tk.BOTTOM)
        button4.pack(side=tk.BOTTOM)
        button3.pack(side=tk.BOTTOM)
        button2.pack(side=tk.BOTTOM)
        button1.pack(side=tk.BOTTOM)


if __name__ == "__main__":
    root = DatabaseGUI()
    root.mainloop()
