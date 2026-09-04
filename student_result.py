# ==========================================
# STUDENT RESULT MANAGEMENT SYSTEM
# ==========================================


# ==========================================
# STEP 1 & 2: STUDENT DATA
# ==========================================

students = [
    {
        "roll_no": 101,
        "name": "Anjaneyulu",
        "telugu": 80,
        "english": 75,
        "maths": 90,
        "science": 85,
        "computer": 88
    },
    {
        "roll_no": 102,
        "name": "Ramu",
        "telugu": 78,
        "english": 82,
        "maths": 85,
        "science": 80,
        "computer": 90
    },
    {
        "roll_no": 103,
        "name": "Abhilash",
        "telugu": 85,
        "english": 88,
        "maths": 92,
        "science": 90,
        "computer": 86
    },
    {
        "roll_no": 104,
        "name": "Rakesh",
        "telugu": 70,
        "english": 75,
        "maths": 80,
        "science": 78,
        "computer": 82
    },
    {
        "roll_no": 105,
        "name": "Harshith",
        "telugu": 90,
        "english": 85,
        "maths": 88,
        "science": 92,
        "computer": 95
    },
    {
        "roll_no": 106,
        "name": "Giridhar",
        "telugu": 76,
        "english": 80,
        "maths": 75,
        "science": 82,
        "computer": 79
    }
]


# ==========================================
# STEP 3: MARKS VALIDATION
# ==========================================

def get_marks(subject):

    while True:

        try:
            marks = int(input("Enter " + subject + " Marks: "))

            if 0 <= marks <= 100:
                return marks

            else:
                print("Invalid marks!")
                print("Enter marks between 0 and 100.")

        except ValueError:
            print("Please enter numbers only.")


# ==========================================
# STEP 4: CALCULATE TOTAL, PERCENTAGE, GRADE
# ==========================================

def calculate_result(student):

    total = (
        student["telugu"]
        + student["english"]
        + student["maths"]
        + student["science"]
        + student["computer"]
    )

    percentage = (total / 500) * 100

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

    student["total"] = total
    student["percentage"] = percentage
    student["grade"] = grade


# Calculate results for existing students

for student in students:
    calculate_result(student)


# ==========================================
# STEP 5: LINEAR SEARCH
# ==========================================

def search_student(roll_no):

    for student in students:

        if student["roll_no"] == roll_no:
            return student

    return None


# ==========================================
# STEP 6: MERGE SORT
# ==========================================

def merge(left, right):

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i]["total"] >= right[j]["total"]:

            result.append(left[i])
            i += 1

        else:

            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def merge_sort(data):

    if len(data) <= 1:
        return data

    mid = len(data) // 2

    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    return merge(left, right)


# ==========================================
# STEP 7: FIND TOPPER
# ==========================================

def find_topper():

    topper = students[0]

    for student in students:

        if student["total"] > topper["total"]:
            topper = student

    return topper


# ==========================================
# STEP 8: DISPLAY ONE STUDENT
# ==========================================

def display_student(student):

    print("\n------------------------------------------")
    print("Roll Number :", student["roll_no"])
    print("Name        :", student["name"])
    print("Telugu      :", student["telugu"])
    print("English     :", student["english"])
    print("Maths       :", student["maths"])
    print("Science     :", student["science"])
    print("Computer    :", student["computer"])
    print("Total       :", student["total"])
    print("Percentage  :", round(student["percentage"], 2), "%")
    print("Grade       :", student["grade"])
    print("------------------------------------------")


# ==========================================
# STEP 9 & 10: MAIN MENU
# ==========================================

while True:

    print("\n==========================================")
    print("     STUDENT RESULT MANAGEMENT SYSTEM")
    print("==========================================")

    print("1. Add Student")
    print("2. Display Results")
    print("3. Search Student")
    print("4. Sort Students")
    print("5. Find Topper")
    print("6. Exit")

    choice = input("Enter your choice: ")


    # ======================================
    # 1. ADD STUDENT
    # ======================================

    if choice == "1":

        try:

            roll_no = int(input("\nEnter Roll Number: "))

            # Check duplicate roll number

            if search_student(roll_no) is not None:

                print("\nRoll Number already exists!")

                continue

            name = input("Enter Student Name: ")

            # Get marks

            telugu = get_marks("Telugu")
            english = get_marks("English")
            maths = get_marks("Maths")
            science = get_marks("Science")
            computer = get_marks("Computer")

            # Create student

            student = {
                "roll_no": roll_no,
                "name": name,
                "telugu": telugu,
                "english": english,
                "maths": maths,
                "science": science,
                "computer": computer
            }

            # Calculate result

            calculate_result(student)

            # Add student to list

            students.append(student)

            print("\nStudent added successfully!")

            print("Total Marks:", student["total"])
            print("Percentage:", round(student["percentage"], 2), "%")
            print("Grade:", student["grade"])

        except ValueError:

            print("\nPlease enter a valid Roll Number.")


    # ======================================
    # 2. DISPLAY RESULTS
    # ======================================

    elif choice == "2":

        print("\n" + "=" * 115)
        print("                         STUDENT RESULTS")
        print("=" * 115)

        print(
            f"{'Roll':<7}"
            f"{'Name':<15}"
            f"{'Telugu':<9}"
            f"{'English':<10}"
            f"{'Maths':<8}"
            f"{'Science':<10}"
            f"{'Computer':<11}"
            f"{'Total':<8}"
            f"{'Percentage':<13}"
            f"{'Grade':<6}"
        )

        print("-" * 115)

        for student in students:

            print(
                f"{student['roll_no']:<7}"
                f"{student['name']:<15}"
                f"{student['telugu']:<9}"
                f"{student['english']:<10}"
                f"{student['maths']:<8}"
                f"{student['science']:<10}"
                f"{student['computer']:<11}"
                f"{student['total']:<8}"
                f"{student['percentage']:<13.2f}"
                f"{student['grade']:<6}"
            )

        print("=" * 115)


    # ======================================
    # 3. SEARCH STUDENT
    # ======================================

    elif choice == "3":

        try:

            roll_no = int(input("\nEnter Roll Number: "))

            student = search_student(roll_no)

            if student is not None:

                print("\n========== STUDENT FOUND ==========")

                display_student(student)

            else:

                print("\nStudent Not Found!")

        except ValueError:

            print("\nPlease enter a valid Roll Number.")


    # ======================================
    # 4. SORT STUDENTS
    # ======================================

    elif choice == "4":

        sorted_students = merge_sort(students)

        print("\n========== STUDENT RANKING ==========")

        rank = 1

        for student in sorted_students:

            print(
                "Rank:",
                rank,
                "| Name:",
                student["name"],
                "| Total:",
                student["total"],
                "| Percentage:",
                round(student["percentage"], 2),
                "%",
                "| Grade:",
                student["grade"]
            )

            rank += 1


    # ======================================
    # 5. FIND TOPPER
    # ======================================

    elif choice == "5":

        topper = find_topper()

        print("\n========== TOPPER ==========")

        print("Roll No      :", topper["roll_no"])
        print("Name         :", topper["name"])
        print("Total Marks  :", topper["total"])
        print("Percentage   :", round(topper["percentage"], 2), "%")
        print("Grade        :", topper["grade"])


    # ======================================
    # 6. EXIT
    # ======================================

    elif choice == "6":

        print("\nThank you for using")
        print("Student Result Management System!")

        break


    # ======================================
    # INVALID CHOICE
    # ======================================

    else:

        print("\nInvalid Choice!")
        print("Please select 1 to 6.")