import curses
import math

import numpy as np


class Student:
    def __init__(self, sid, name, dob):
        self.sid = sid
        self.name = name
        self.dob = dob
        self.marks = {}  

    def set_mark(self, course_id, mark):
        self.marks[course_id] = math.floor(mark * 10) / 10

    def gpa(self, courses):
        """Weighted average: sum(mark * credit) / sum(credit), using numpy arrays."""
        ids = [cid for cid in self.marks if cid in courses]
        if not ids:
            return 0.0
        marks = np.array([self.marks[cid] for cid in ids])
        credits = np.array([courses[cid].credit for cid in ids])
        return float(np.sum(marks * credits) / np.sum(credits))

    def __str__(self):
        return f"{self.sid:<8} {self.name:<22} {self.dob}"


class Course:
    def __init__(self, cid, name, credit):
        self.cid = cid
        self.name = name
        self.credit = credit

    def __str__(self):
        return f"{self.cid:<8} {self.name:<22} credits: {self.credit}"


class School:
    def __init__(self):
        self.students = []
        self.courses = {}  

    def add_student(self, sid, name, dob):
        self.students.append(Student(sid, name, dob))

    def add_course(self, cid, name, credit):
        self.courses[cid] = Course(cid, name, credit)

    def find_student(self, sid):
        for s in self.students:
            if s.sid == sid:
                return s
        return None

    def sort_by_gpa(self):
        self.students.sort(key=lambda s: s.gpa(self.courses), reverse=True)


def put(win, y, x, text, attr=0):
    h, w = win.getmaxyx()
    if 0 <= y < h - 1 and x < w - 1:
        try:
            win.addstr(y, x, text[: w - x - 1], attr)
        except curses.error:
            pass


def header(win, title):
    win.clear()
    win.attron(curses.color_pair(1) | curses.A_BOLD)
    win.border()
    win.attroff(curses.color_pair(1) | curses.A_BOLD)
    put(win, 1, 3, f"=== {title} ===", curses.color_pair(2) | curses.A_BOLD)


def ask(win, row, label):
    put(win, row, 3, label, curses.color_pair(3))
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
            put(win, row, 3, " " * 70)  


def show(win, title, lines):
    header(win, title)
    for i, line in enumerate(lines):
        put(win, 3 + i, 3, line)
    put(win, 4 + len(lines), 3, "Press any key to go back...", curses.A_DIM)
    win.refresh()
    win.getch()


def input_students(win, school):
    header(win, "Input students")
    n = ask_number(win, 3, "Number of students:", int, 1)
    for i in range(n):
        header(win, f"Student {i + 1}/{n}")
        sid = ask(win, 3, "ID:")
        name = ask(win, 4, "Name:")
        dob = ask(win, 5, "DoB (dd/mm/yyyy):")
        school.add_student(sid, name, dob)


def input_courses(win, school):
    header(win, "Input courses")
    n = ask_number(win, 3, "Number of courses:", int, 1)
    for i in range(n):
        header(win, f"Course {i + 1}/{n}")
        cid = ask(win, 3, "ID:")
        name = ask(win, 4, "Name:")
        credit = ask_number(win, 5, "Credits:", int, 1)
        school.add_course(cid, name, credit)


def input_marks(win, school):
    if not school.courses or not school.students:
        show(win, "Input marks", ["Please input students and courses first."])
        return
    header(win, "Input marks")
    for i, c in enumerate(school.courses.values()):
        put(win, 3 + i, 3, str(c))
    row = 4 + len(school.courses)
    cid = ask(win, row, "Select course ID:")
    if cid not in school.courses:
        show(win, "Input marks", ["Course not found."])
        return
    for s in school.students:
        header(win, f"Marks - {school.courses[cid].name}")
        mark = ask_number(win, 3, f"Mark of {s.name} (0-20):", float, 0, 20)
        s.set_mark(cid, mark)  


def list_courses(win, school):
    show(win, "Courses", [str(c) for c in school.courses.values()] or ["(empty)"])


def list_students(win, school):
    show(win, "Students", [str(s) for s in school.students] or ["(empty)"])


def show_marks(win, school):
    header(win, "Show marks")
    cid = ask(win, 3, "Course ID:")
    if cid not in school.courses:
        show(win, "Show marks", ["Course not found."])
        return
    lines = [
        f"{s.name:<22} {s.marks[cid]:.1f}" for s in school.students if cid in s.marks
    ]
    show(win, f"Marks - {school.courses[cid].name}", lines or ["(no marks yet)"])


def show_gpa(win, school):
    header(win, "Student GPA")
    s = school.find_student(ask(win, 3, "Student ID:"))
    if s is None:
        show(win, "Student GPA", ["Student not found."])
        return
    show(win, "Student GPA", [f"{s.name}: GPA = {s.gpa(school.courses):.2f}"])


def show_ranking(win, school):
    school.sort_by_gpa()
    lines = [
        f"{i + 1:>2}. {s.name:<22} GPA: {s.gpa(school.courses):.2f}"
        for i, s in enumerate(school.students)
    ]
    show(win, "Ranking by GPA (descending)", lines or ["(empty)"])


MENU = [
    ("Input students", input_students),
    ("Input courses", input_courses),
    ("Input marks for a course", input_marks),
    ("List courses", list_courses),
    ("List students", list_students),
    ("Show marks of a course", show_marks),
    ("Show GPA of a student", show_gpa),
    ("Sort students by GPA (desc)", show_ranking),
    ("Exit", None),
]


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    stdscr.keypad(True)

    school = School()
    choice = 0
    while True:
        header(stdscr, "STUDENT MARK MANAGEMENT")
        for i, (label, _) in enumerate(MENU):
            if i == choice:
                put(stdscr, 3 + i, 3, f" > {label} ", curses.color_pair(4) | curses.A_BOLD)
            else:
                put(stdscr, 3 + i, 3, f"   {label} ")
        put(stdscr, 4 + len(MENU), 3, "Up/Down: move   Enter: select", curses.A_DIM)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            choice = (choice - 1) % len(MENU)
        elif key == curses.KEY_DOWN:
            choice = (choice + 1) % len(MENU)
        elif key in (curses.KEY_ENTER, 10, 13):
            func = MENU[choice][1]
            if func is None:
                break
            func(stdscr, school)


if __name__ == "__main__":
    curses.wrapper(main)