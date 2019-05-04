from GUI import DatabaseGUI
from Curriculum import initdatabase

if __name__ == "__main__":
    initdatabase()
    root = DatabaseGUI()
    root.mainloop()
