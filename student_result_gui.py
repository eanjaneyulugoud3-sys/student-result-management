import tkinter as tk
from tkinter import messagebox
import sqlite3


# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect("students.db")
cursor = conn.cursor()


# ==========================================
# CREATE TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    telugu INTEGER,
    english INTEGER,
    maths INTEGER,
    science INTEGER,
    computer INTEGER,
    total INTEGER,
    percentage REAL,
    grade TEXT
)
""")

conn.commit()


# ==========================================
# ADD STUDENT
# ==========================================

def add_student():

    form = tk.Toplevel(window)
    form.title("Add Student")
    form.geometry("500x650")

    tk.Label(
        form,
        text="ADD STUDENT",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    # Roll Number
    tk.Label(form, text="Roll Number").pack()
    roll_entry = tk.Entry(form)
    roll_entry.pack(pady=5)

    # Name
    tk.Label(form, text="Student Name").pack()
    name_entry = tk.Entry(form)
    name_entry.pack(pady=5)

    # Telugu
    tk.Label(form, text="Telugu Marks").pack()
    telugu_entry = tk.Entry(form)
    telugu_entry.pack(pady=5)

    # English
    tk.Label(form, text="English Marks").pack()
    english_entry = tk.Entry(form)
    english_entry.pack(pady=5)

    # Maths
    tk.Label(form, text="Maths Marks").pack()
    maths_entry = tk.Entry(form)
    maths_entry.pack(pady=5)

    # Science
    tk.Label(form, text="Science Marks").pack()
    science_entry = tk.Entry(form)
    science_entry.pack(pady=5)

    # Computer
    tk.Label(form, text="Computer Marks").pack()
    computer_entry = tk.Entry(form)
    computer_entry.pack(pady=5)


    # ==========================================
    # SAVE STUDENT
    # ==========================================

    def save_student():

        try:

            roll_no = int(roll_entry.get())
            name = name_entry.get()

            telugu = int(telugu_entry.get())
            english = int(english_entry.get())
            maths = int(maths_entry.get())
            science = int(science_entry.get())
            computer = int(computer_entry.get())

            # Check name
            if name == "":
                messagebox.showerror(
                    "Error",
                    "Please enter student name"
                )
                return

            # Check marks
            marks = [
                telugu,
                english,
                maths,
                science,
                computer
            ]

            for mark in marks:

                if mark < 0 or mark > 100:

                    messagebox.showerror(
                        "Error",
                        "Marks must be between 0 and 100"
                    )

                    return

            # Calculate total
            total = (
                telugu
                + english
                + maths
                + science
                + computer
            )

            # Calculate percentage
            percentage = (total / 500) * 100

            # Calculate grade
            if percentage >= 90:
                grade = "A+"
            elif percentage >= 80:
                grade = "A"
            elif percentage >= 70:
                grade = "B"
            elif percentage >= 60:
                grade = "C"
            elif percentage >= 50:
                grade = "D"
            else:
                grade = "F"


            # ==========================================
            # INSERT INTO DATABASE
            # ==========================================

            cursor.execute("""
            INSERT INTO students
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                roll_no,
                name,
                telugu,
                english,
                maths,
                science,
                computer,
                total,
                percentage,
                grade
            ))

            conn.commit()


            messagebox.showinfo(
                "Success",
                "Student Added Successfully!\n\n"
                + "Roll Number: " + str(roll_no)
                + "\nName: " + name
                + "\nTotal: " + str(total)
                + "\nPercentage: "
                + str(round(percentage, 2))
                + "%"
                + "\nGrade: " + grade
            )

            form.destroy()


        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Roll Number already exists!"
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter valid numbers!"
            )


    # Button
    tk.Button(
        form,
        text="Calculate & Add",
        font=("Arial", 13, "bold"),
        width=20,
        command=save_student
    ).pack(pady=20)


# ==========================================
# DISPLAY RESULTS
# ==========================================

def display_results():

    result_window = tk.Toplevel(window)

    result_window.title("Student Results")

    result_window.geometry("1000x600")


    tk.Label(
        result_window,
        text="STUDENT RESULTS",
        font=("Arial", 20, "bold")
    ).pack(pady=20)


    cursor.execute("SELECT * FROM students")

    records = cursor.fetchall()


    if len(records) == 0:

        tk.Label(
            result_window,
            text="No student records available",
            font=("Arial", 14)
        ).pack(pady=30)

        return


    for student in records:

        text = (
            "Roll No: " + str(student[0])
            + " | Name: " + student[1]
            + " | Telugu: " + str(student[2])
            + " | English: " + str(student[3])
            + " | Maths: " + str(student[4])
            + " | Science: " + str(student[5])
            + " | Computer: " + str(student[6])
            + " | Total: " + str(student[7])
            + " | Percentage: "
            + str(round(student[8], 2))
            + "% | Grade: " + student[9]
        )

        tk.Label(
            result_window,
            text=text,
            font=("Arial", 10)
        ).pack(pady=5)


# ==========================================
# SEARCH STUDENT
# ==========================================

def search_student():

    search_window = tk.Toplevel(window)

    search_window.title("Search Student")

    search_window.geometry("500x350")


    tk.Label(
        search_window,
        text="SEARCH STUDENT",
        font=("Arial", 20, "bold")
    ).pack(pady=30)


    tk.Label(
        search_window,
        text="Enter Roll Number"
    ).pack()


    roll_entry = tk.Entry(search_window)

    roll_entry.pack(pady=10)


    def perform_search():

        try:

            roll_no = int(roll_entry.get())


            # Linear Search
            cursor.execute(
                "SELECT * FROM students"
            )

            records = cursor.fetchall()


            for student in records:

                if student[0] == roll_no:

                    messagebox.showinfo(

                        "Student Found",

                        "Roll Number: "
                        + str(student[0])
                        + "\nName: "
                        + student[1]
                        + "\nTotal: "
                        + str(student[7])
                        + "\nPercentage: "
                        + str(round(student[8], 2))
                        + "%"
                        + "\nGrade: "
                        + student[9]
                    )

                    return


            messagebox.showerror(
                "Not Found",
                "Student not found!"
            )


        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter a valid roll number!"
            )


    tk.Button(
        search_window,
        text="Search",
        font=("Arial", 13, "bold"),
        width=15,
        command=perform_search
    ).pack(pady=20)


# ==========================================
# MERGE
# ==========================================

def merge(left, right):

    result = []

    i = 0
    j = 0


    while i < len(left) and j < len(right):

        if left[i][7] >= right[j][7]:

            result.append(left[i])
            i += 1

        else:

            result.append(right[j])
            j += 1


    result.extend(left[i:])
    result.extend(right[j:])


    return result


# ==========================================
# MERGE SORT
# ==========================================

def merge_sort(data):

    if len(data) <= 1:

        return data


    mid = len(data) // 2


    left = merge_sort(
        data[:mid]
    )

    right = merge_sort(
        data[mid:]
    )


    return merge(left, right)


# ==========================================
# SORT STUDENTS
# ==========================================

def sort_students():

    cursor.execute(
        "SELECT * FROM students"
    )

    records = cursor.fetchall()


    if len(records) == 0:

        messagebox.showinfo(
            "Sort",
            "No student records available"
        )

        return


    sorted_students = merge_sort(records)


    sort_window = tk.Toplevel(window)

    sort_window.title("Student Ranking")

    sort_window.geometry("800x500")


    tk.Label(
        sort_window,
        text="STUDENT RANKING",
        font=("Arial", 20, "bold")
    ).pack(pady=20)


    rank = 1


    for student in sorted_students:

        text = (
            "Rank: " + str(rank)
            + " | Roll No: " + str(student[0])
            + " | Name: " + student[1]
            + " | Total: " + str(student[7])
            + " | Percentage: "
            + str(round(student[8], 2))
            + "%"
            + " | Grade: " + student[9]
        )


        tk.Label(
            sort_window,
            text=text,
            font=("Arial", 11)
        ).pack(pady=5)


        rank += 1


# ==========================================
# FIND TOPPER
# ==========================================

def find_topper():

    cursor.execute(
        "SELECT * FROM students"
    )

    records = cursor.fetchall()


    if len(records) == 0:

        messagebox.showinfo(
            "Topper",
            "No student records available"
        )

        return


    # Linear scan
    topper = records[0]


    for student in records:

        if student[7] > topper[7]:

            topper = student


    messagebox.showinfo(

        "TOPPER",

        "Roll Number: "
        + str(topper[0])

        + "\nName: "
        + topper[1]

        + "\nTotal Marks: "
        + str(topper[7])

        + "\nPercentage: "
        + str(round(topper[8], 2))

        + "%"

        + "\nGrade: "
        + topper[9]
    )


# ==========================================
# MAIN WINDOW
# ==========================================

window = tk.Tk()

window.title(
    "Student Result Management System"
)

window.geometry("700x600")


tk.Label(

    window,

    text="STUDENT RESULT MANAGEMENT SYSTEM",

    font=("Arial", 22, "bold")
).pack(pady=30)


# Add Student

tk.Button(

    window,

    text="Add Student",

    font=("Arial", 14),

    width=25,

    command=add_student

).pack(pady=10)


# Display Results

tk.Button(

    window,

    text="Display Results",

    font=("Arial", 14),

    width=25,

    command=display_results

).pack(pady=10)


# Search Student

tk.Button(

    window,

    text="Search Student",

    font=("Arial", 14),

    width=25,

    command=search_student

).pack(pady=10)


# Sort Students

tk.Button(

    window,

    text="Sort Students",

    font=("Arial", 14),

    width=25,

    command=sort_students

).pack(pady=10)


# Find Topper

tk.Button(

    window,

    text="Find Topper",

    font=("Arial", 14),

    width=25,

    command=find_topper

).pack(pady=10)


# Exit

tk.Button(

    window,

    text="Exit",

    font=("Arial", 14),

    width=25,

    command=window.destroy

).pack(pady=10)


# ==========================================
# START PROGRAM
# ==========================================

window.mainloop()


# Close database connection
conn.close()
