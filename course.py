class Course:
    def __init__(self, cid, name, credit):
        self.cid = cid
        self.name = name
        self.credit = credit

    def __str__(self):
        return f"{self.cid:<8} {self.name:<22} credits: {self.credit}"
