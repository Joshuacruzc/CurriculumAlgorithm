from import_curriculum import import_curriculum


class StudentPlan:

    semesters = []

    def __init__(self, curriculum, max_credits):
        self.curriculum = curriculum
        self.max_credits = max_credits

    def build_plan(self):
        sorted_courses = sorted(self.curriculum.courses, key=lambda c: c.level, reverse=True)
        for course in sorted_courses:
            self.accommodate(course)
        return self.semesters

    def accommodate(self, course, correq=False):
        if course.position is not None:
            return course.position + 1 if not correq else course.position
        min_position = 0
        for pre_requisite in course.pre_requisites:
            min_position = max(min_position, self.accommodate(pre_requisite))
        for co_requisite in course.co_requisites:
            min_position = max(min_position, self.accommodate(co_requisite, correq=True))
        min_position = self.bops(min_position=min_position, course=course)
        return min_position + 1 if not correq else course.position

    def add_semester(self, position):
        semester = Semester(max_credits=self.max_credits, position=position)
        self.semesters.append(semester)
        return semester

    def bops(self, course, min_position):
        if min_position >= len(self.semesters):
            self.add_semester(position=min_position)
        for semester_index in range(min_position, len(self.semesters)):
            if not self.semesters[semester_index].is_full:
                if self.semesters[semester_index].credit_hours + course.credit_hours <= self.semesters[semester_index].max_credits:
                    self.semesters[semester_index].add_course(course)
                    return semester_index
        semester = self.add_semester(position=len(self.semesters))
        semester.add_course(course)
        return semester.position


class Semester:

    is_full = False
    credit_hours = 0

    def __init__(self, max_credits, position):
        self.max_credits = max_credits
        self.position = position
        self.courses = list()

    def add_course(self, course):
        course.position = self.position
        self.courses.append(course)
        self.credit_hours += course.credit_hours
        self.is_full = self.credit_hours >= self.max_credits

    def __repr__(self):
        return f'Semester: year:{self.position//2 + 1}  semester: {1 if self.position % 2 == 0 else 2},' \
            f' Courses: {self.courses}'


if __name__ == '__main__':
    ciic = import_curriculum('CIIC')
    plan = StudentPlan(curriculum=ciic, max_credits=16)
    for semester in plan.build_plan():
        print(semester, semester.credit_hours)