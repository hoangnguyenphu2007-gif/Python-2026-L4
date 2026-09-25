students = {}   
courses = {}    
marks = {}     


def input_students():
    """List and information about students."""
    n = int(input("Nhập số lượng sinh viên: "))
    for _ in range(n):
        sid = input("  Student ID: ").strip()
        name = input("  Name: ").strip()
        dob = input("  Date of birth (dd/mm/yyyy): ").strip()
        students[sid] = {"name": name, "dob": dob}


def input_courses():
    """how many and what the information about the course."""
    n = int(input("Subjects: "))
    for _ in range(n):
        cid = input("  Course ID: ").strip()
        name = input("  Course name: ").strip()
        courses[cid] = {"name": name}


def input_marks_for_course():
    """Choose one and write the marks for that course."""
    if not courses:
        print("there are no subjects pls write one.")
        return
    list_courses()
    cid = input("ID course for mark: ").strip()
    if cid not in courses:
        print("Invalid ID.")
        return

    marks.setdefault(cid, {})
    for sid, info in students.items():
        mark = float(input(f"  Điểm của {info['name']} ({sid}): "))
        marks[cid][sid] = mark


def list_courses():
    """List the subjects course."""
    print("\n--- Subjects ---")
    if not courses:
        print("  (where are your subjects)")
    for cid, info in courses.items():
        print(f"  {cid} - {info['name']}")


def list_students():
    """List students."""
    print("\n--- List students ---")
    if not students:
        print("  (there are nơ students in course)")
    for sid, info in students.items():
        print(f"  {sid} - {info['name']} - {info['dob']}")


def show_marks_for_course():
    """Show the mark."""
    list_courses()
    cid = input("Write mark of the ID course: ").strip()
    if cid not in courses:
        print("Invalid course ID.")
        return
    if cid not in marks or not marks[cid]:
        print("no mark for this course.")
        return

    print(f"\n--- mark {courses[cid]['name']} ---")
    for sid, mark in marks[cid].items():
        name = students.get(sid, {}).get("name", "Unknown")
        print(f"  {sid} - {name}: {mark}")



def main():
    actions = {
        "1": input_students,
        "2": input_courses,
        "3": input_marks_for_course,
        "4": list_students,
        "5": list_courses,
        "6": show_marks_for_course,
    }

    menu = """
===== STUDENT MARK MANAGEMENT =====
1. Input students
2. Input courses
3. Input marks for a course
4. List students
5. List courses
6. Show marks for a course
0. Exit
"""
    while True:
        print(menu)
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()