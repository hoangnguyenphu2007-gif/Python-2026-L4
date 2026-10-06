"""Main script: coordinates input, output and domain classes."""
import curses

import input as inp
import output
from domains import School


def show_marks_action(win, school):
    output.header(win, "Show marks")
    cid = inp.ask(win, 3, "Course ID:")
    output.show_marks(win, school, cid)


def show_gpa_action(win, school):
    output.header(win, "Student GPA")
    sid = inp.ask(win, 3, "Student ID:")
    output.show_gpa(win, school, sid)


def ranking_action(win, school):
    school.sort_by_gpa()
    output.show_ranking(win, school)


MENU = [
    ("Input students", inp.input_students),
    ("Input courses", inp.input_courses),
    ("Input marks for a course", inp.input_marks),
    ("List courses", output.list_courses),
    ("List students", output.list_students),
    ("Show marks of a course", show_marks_action),
    ("Show GPA of a student", show_gpa_action),
    ("Sort students by GPA (desc)", ranking_action),
    ("Exit", None),
]


def main(stdscr):
    output.init_colors()
    stdscr.keypad(True)
    school = School()
    labels = [label for label, _ in MENU]
    choice = 0
    while True:
        output.draw_menu(stdscr, "STUDENT MARK MANAGEMENT", labels, choice)
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
