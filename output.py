"""Module for curses output (drawing only, no data entry)."""
import curses


def init_colors():
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)


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


def show(win, title, lines):
    header(win, title)
    for i, line in enumerate(lines):
        put(win, 3 + i, 3, line)
    put(win, 4 + len(lines), 3, "Press any key to go back...", curses.A_DIM)
    win.refresh()
    win.getch()


def draw_menu(win, title, items, choice):
    header(win, title)
    for i, label in enumerate(items):
        if i == choice:
            put(win, 3 + i, 3, f" > {label} ", curses.color_pair(4) | curses.A_BOLD)
        else:
            put(win, 3 + i, 3, f"   {label} ")
    put(win, 4 + len(items), 3, "Up/Down: move   Enter: select", curses.A_DIM)
    win.refresh()


def list_courses(win, school):
    show(win, "Courses", [str(c) for c in school.courses.values()] or ["(empty)"])


def list_students(win, school):
    show(win, "Students", [str(s) for s in school.students] or ["(empty)"])


def show_marks(win, school, cid):
    if cid not in school.courses:
        show(win, "Show marks", ["Course not found."])
        return
    lines = [
        f"{s.name:<22} {s.marks[cid]:.1f}" for s in school.students if cid in s.marks
    ]
    show(win, f"Marks - {school.courses[cid].name}", lines or ["(no marks yet)"])


def show_gpa(win, school, sid):
    s = school.find_student(sid)
    if s is None:
        show(win, "Student GPA", ["Student not found."])
        return
    show(win, "Student GPA", [f"{s.name}: GPA = {s.gpa(school.courses):.2f}"])


def show_ranking(win, school):
    lines = [
        f"{i + 1:>2}. {s.name:<22} GPA: {s.gpa(school.courses):.2f}"
        for i, s in enumerate(school.students)
    ]
    show(win, "Ranking by GPA (descending)", lines or ["(empty)"])
