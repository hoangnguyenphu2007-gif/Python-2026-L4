from .course import Course
from .student import Student


class School:
    def __init__(self):
        self.students = []
        self.courses = {}  # cid -> Course

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
