"""Python+Sqlite+GUIdesign
Created by Sasita C."""
"""Description: input 000(for example)and press "Search Info" button,
the information will show. Other input(not in database) will show no member.
To save more information, fill empty blanks before press "Save Info" button"""
import sqlite3
from tkinter import *
from tkinter import ttk

################ Database(Sqlite) ####################
conn = sqlite3.connect("AttendanceDB.sqlite3")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS memberinfo(
				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				studentID TEXT,
				first_name TEXT,
				last_name TEXT,
				english_name TEXT,
				email TEXT) """)
c.execute("""CREATE TABLE IF NOT EXISTS Attendance(
				Name TEXT,
				Time TEXT) """)

def Insert_NewMember(studentID, first_name, last_name, english_name, email):
    with conn:
        command = "INSERT INTO memberinfo VALUES (?,?,?,?,?,?)"
        c.execute(command, (None, studentID, first_name, last_name, english_name, email))
    conn.commit()
    print("Saved")
def Insert_Attendance():
    with open("Attendance.csv", "r") as file:
        record = 1
        for row in file:
            c.execute("INSERT INTO Attendance VALUES (?,?)", row.split(","))
            conn.commit()
            record += 1
    conn.close()

def View_Member():
    with conn:
        command = "SELECT * FROM memberinfo"
        c.execute(command)
        result = c.fetchall()
    print(result)
    return (result)

def View_OneMember(studentID):
    with conn:
        command = "SELECT * FROM memberinfo WHERE studentID = (?)"
        c.execute(command, ([studentID]))
        result = c.fetchall()
    print(result)
    return (result)

def View_OneMember_T(english_name):
    with conn:
        command = "SELECT Time FROM Attendance WHERE Name = (?)"
        c.execute(command, ([english_name]))
        result = c.fetchall()
    print(result)
    return (result)

def Delete_Member(ID):
    with conn:
        command = "DELETE FROM memberinfo WHERE ID=(?)"
        c.execute(command, ([ID]))
    conn.commit()
    print("{}: deleted".format(ID))

def Update_Member(ID, field, data):
    with conn:
        command = "UPDATE memberinfo SET {} = (?) WHERE ID=(?)".format(field)
        c.execute(command, ([data, ID]))
    conn.commit()
    print("{}: {}={}".format(ID, field, data))
#Insert_Attendance() #Just once you want to import .csv file
# View_OneMember_T("SASITA C.") #Test

################ GUIdesign ####################
GUI = Tk()
GUI.geometry("900x600")
GUI.title("Attending Member")
################ LEFT ####################
v_search = StringVar()
v_search.set("XXX")
search = ttk.Entry(GUI, textvariable=v_search, font=(None, 20), width=20)
search.place(x=50, y=50)

from tkinter import messagebox

def SearchMember():
    search = v_search.get()
    data = View_OneMember(search)
    if len(data) >= 1:
        data = data[0]
        v_studentID.set(data[1])
        v_first_name.set(data[2])
        v_last_name.set(data[3])
        v_english_name.set(data[4])
        v_email.set(data[5])
    else:
        messagebox.showwarning("Not found", "Member not found\n Please try again")

    searchT = v_english_name.get()
    dataT = View_OneMember_T(searchT)
    if len(dataT) >= 1:
        dataT = dataT[0]
        v_Time.set(dataT[0])

FB1 = Frame(GUI)
FB1.place(x=75, y=100)
bsearch = Button(FB1, text="Search Info", command=SearchMember)
bsearch.pack(ipadx=20, ipady=20)

v_Time = StringVar()
L = Label(FB1, text="Time & Attendance", font=(None, 15)).pack()
E0 = ttk.Entry(FB1, textvariable=v_Time, font=(None, 20), width=15)
E0.pack()
################ RIGHT ####################
FB2 = Frame(GUI)
FB2.place(x=400, y=100)

v_studentID = StringVar()
L = Label(FB2, text="ID", font=(None, 15)).pack()
E1 = ttk.Entry(FB2, textvariable=v_studentID, font=(None, 20), width=25)
E1.pack()

v_first_name = StringVar()
L = Label(FB2, text="First name", font=(None, 15)).pack()
E2 = ttk.Entry(FB2, textvariable=v_first_name, font=(None, 20), width=25)
E2.pack()

v_last_name = StringVar()
L = Label(FB2, text="Last name", font=(None, 15)).pack()
E3 = ttk.Entry(FB2, textvariable=v_last_name, font=(None, 20), width=25)
E3.pack()

v_english_name = StringVar()
L = Label(FB2, text="English name", font=(None, 15)).pack()
E4 = ttk.Entry(FB2, textvariable=v_english_name, font=(None, 20), width=25)
E4.pack()

v_email = StringVar()
L = Label(FB2, text="Email", font=(None, 15)).pack()
E5 = ttk.Entry(FB2, textvariable=v_email, font=(None, 20), width=25)
E5.pack()

def SaveMember():
    studentID = v_studentID.get()
    first_name = v_first_name.get()
    last_name = v_last_name.get()
    english_name = v_english_name.get()
    email = v_email.get()
    data = Insert_NewMember(studentID, first_name, last_name, english_name, email)
    v_studentID.set(data[1])
    v_first_name.set(data[2])
    v_last_name.set(data[3])
    v_english_name.set(data[4])
    v_email.set(data[5])

FB2 = Frame(GUI)
FB2.place(x=510, y=420)
bsave = Button(FB2, text="Save Info", command=SaveMember)
bsave.pack(ipadx=20, ipady=20)

GUI.mainloop()
