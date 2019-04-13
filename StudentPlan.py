from import_curriculum import import_curriculum


class StudentPlan:

    semesters = []

    def __init__(self, curriculum, max_credits, past_semesters=None):
        self.curriculum = curriculum
        self.max_credits = max_credits
        if past_semesters is not None:
            for semester_position in range(max(past_semesters.keys())+1):
                past_semester = self.add_semester(semester_position, past=True)
                courses_to_add = past_semesters.get(semester_position, None)
                for course in courses_to_add:
                    past_semester.add_course(curriculum.get_course(course))

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
        min_position = self.set_to_earliest_possible_semester(min_position=min_position, course=course)
        return min_position + 1 if not correq else course.position

    def add_semester(self, position, past=False):
        semester = Semester(max_credits=self.max_credits, position=position, past=past)
        self.semesters.append(semester)
        return semester

    def force_accommodate(self, position, course):
        if not self.get_semester(position):
            new_semester = self.add_semester(position)
            new_semester.add_course(course)

    def get_semester(self, position):
        for semester in self.semesters:
            if semester.position == position:
                return semester

    def set_to_earliest_possible_semester(self, course, min_position):
        if not self.get_semester(min_position):
            self.add_semester(position=min_position)
        self.semesters = sorted(self.semesters, key=lambda s: s.position,)
        for semester_index in range(min_position, len(self.semesters)):
            if self.semesters[semester_index].course_valid(course):
                self.semesters[semester_index].add_course(course)
                return semester_index
        semester = self.add_semester(position=len(self.semesters))
        semester.add_course(course)
        return semester.position


class Semester:
    is_full = False
    credit_hours = 0

    def __init__(self, max_credits, position, past=False):
        self.max_credits = max_credits
        self.position = position
        self.courses = list()
        self.past = past

    def course_valid(self, course):
        if not self.is_full and not self.past and self.credit_hours + course.get_credit_hours() <= self.max_credits:
            if course.season == 2:
                return self.position % 2 == 0
            elif course.season == 1:
                return self.position % 2 == 1
            else:
                return True

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


if __name__ == '__main__':
    # Example Use
    ciic = import_curriculum('CIIC')
    my_past_semesters = {
        0: ['INGL3--1', 'ESPA3101', 'MATE3005', 'INGL3--2', 'ESPA3102'],
        1: ['MATE3031', 'QUIM3131', 'INGL3211', 'INGE3011', 'SOHU1111'],
        2: ['MATE3032', 'QUIM3132', 'CIIC3011', 'EDFI---1', 'EDFI---2'],
        3: ['CIIC5--1', 'CIIC5--2'],
        4: ['CIIC4010', 'CIIC3075', 'INGL3212', 'FREE---1'],
    }
    everson_semester = {
        1: ['MATE3005', 'QUIM3131', 'INGL3--1', 'INGE3011', 'ESPA3101'],
        2: ['MATE3031', 'QUIM3132', 'INGL3--2', 'EDFI---1', 'EDFI---2', 'ESPA3102'],
        3: ['MATE3032', 'CIIC3011', 'FISI3171', 'INGL3211'],
        4: ['MATE3063', 'CIIC4010', 'CIIC3075', 'FISI3172', 'INGL3212'],
        5: ['CIIC4020', 'MATE4145', 'INEL3105', 'INGE3035'],
        6: ['CIIC5--1']
    }
    plan = StudentPlan(curriculum=ciic, max_credits=16, past_semesters=everson_semester)
    # plan.force_accommodate(6, ciic.get_course('MATE3063'))
    for semester in plan.build_plan():
        print(semester, semester.credit_hours)