class Semester:

    def __init__(self, max_credits, max_difficulty, position, past=False):
        self.max_credits = max_credits
        self.max_difficulty = max_difficulty
        self.position = position
        self.courses = list()
        self.past = past
        self.is_full = False
        self.credit_hours = 0

    def course_valid(self, course):
        if self.is_full:
            return False
        if self.past:
            return False
        if not self.credit_hours + course.get_credit_hours() <= self.max_credits:
            return False
        if self.calculate_difficulty(course) > self.max_difficulty:
            return False
        if course.season == 2 and not self.position % 2 == 0:
            return False
        if course.season == 1 and not self.position % 2 == 1:
            return False
        return True

    def calculate_difficulty(self, new_course=None):
        difficulty_sum = 0
        for course in self.courses:
            difficulty_sum += course.difficulty
        if new_course is not None:
            difficulty_sum += new_course.get_difficulty()
        return difficulty_sum

    def add_course(self, course):
        course.position = self.position
        self.courses.append(course)
        if course.lab:
            course.lab.position = self.position
            self.courses.append(course.lab)
        self.credit_hours += course.get_credit_hours()
        self.is_full = self.credit_hours >= self.max_credits

    def get_year(self):
        return int(self.position/2) if self.position % 2 == 0 else self.position//2 + 1

    year = property(get_year)

    def __repr__(self):
        if self.position > 0:
            return f'Semester: year:{ self.year }  semester: {2 if self.position % 2 == 0 else 1},' \
            f' Courses: {self.courses}'
        else:
            return f'Before College: Courses{self.courses}'
