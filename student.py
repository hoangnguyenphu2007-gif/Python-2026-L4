import math

import numpy as np


class Student:
    def __init__(self, sid, name, dob):
        self.sid = sid
        self.name = name
        self.dob = dob
        self.marks = {}  # course_id -> mark

    def set_mark(self, course_id, mark):
        # Round DOWN to 1 decimal digit using math.floor()
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
