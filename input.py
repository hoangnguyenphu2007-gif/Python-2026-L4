"""Module for input (reads data from the user through curses)."""
import curses

import output


def ask(win, row, label):
    output.put(win, row, 3, label, curses.color_pair(3))
    win.refresh()
    curses.echo()
    curses.curs_set(1)
    text = win.getstr(row, 3 + len(label) + 1, 40).decode().strip()
    curses.noecho()
    curses.curs_set(0)
    return text


def ask_number(win, row, label, cast, minimum=None, maximum=None):
    while True:
        try:
            value = cast(ask(win, row, label))
            if (minimum is not None and value < minimum) or (
                maximum is not None and value > maximum
            ):
                raise ValueError
            return value
        except ValueError:
            output.put(win, row, 3, " " * 70)  # clear the line and ask again


def input_students(win, school):
    output.header(win, "Input students")
    n = ask_number(win, 3, "Number of students:", int, 1)
    for i in range(n):
        output.header(win, f"Student {i + 1}/{n}")
        sid = ask(win, 3, "ID:")
        name = ask(win, 4, "Name:")
        dob = ask(win, 5, "DoB (dd/mm/yyyy):")
        school.add_student(sid, name, dob)


def input_courses(win, school):
    output.header(win, "Input courses")
    n = ask_number(win, 3, "Number of courses:", int, 1)
    for i in range(n):
        output.header(win, f"Course {i + 1}/{n}")
        cid = ask(win, 3, "ID:")
        name = ask(win, 4, "Name:")
        credit = ask_number(win, 5, "Credits:", int, 1)
        school.add_course(cid, name, credit)


def input_marks(win, school):
    if not school.courses or not school.students:
        output.show(win, "Input marks", ["Please input students and courses first."])
        return
    output.header(win, "Input marks")
    for i, c in enumerate(school.courses.values()):
        output.put(win, 3 + i, 3, str(c))
    cid = ask(win, 4 + len(school.courses), "Select course ID:")
    if cid not in school.courses:
        output.show(win, "Input marks", ["Course not found."])
        return
    for s in school.students:
        output.header(win, f"Marks - {school.courses[cid].name}")
        mark = ask_number(win, 3, f"Mark of {s.name} (0-20):", float, 0, 20)
        s.set_mark(cid, mark)  # floored to 1 decimal inside Student
