from import_curriculum import import_curriculum


class StudentPlan:

    semesters = []

    def __init__(self, curriculum, max_credits, past_semesters=None):
        self.curriculum = curriculum
        self.max_credits = max_credits
        if past_semesters is not None:
            for past_semester_key in past_semesters.keys():
                past_semester = self.add_semester(int(past_semester_key), past=True)
                courses_to_add = past_semesters[past_semester_key]
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

    def get_semester(self, position):
        for semester in self.semesters:
            if semester.position == position:
                return semester

    def set_to_earliest_possible_semester(self, course, min_position):
        if not self.get_semester(min_position):
            self.add_semester(position=min_position)
        self.semesters = sorted(self.semesters, key=lambda s: s.position,)
        for semester_index in range(min_position, len(self.semesters)):
            if not self.semesters[semester_index].is_full and not self.semesters[semester_index].past:
                if self.semesters[semester_index].credit_hours + course.get_credit_hours() \
                        <= self.semesters[semester_index].max_credits:
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
        # return f'Semester{self.position}, Courses: {self.courses}'
        if self.position > 0:
            return f'Semester: year:{ self.year }  semester: {2 if self.position % 2 == 0 else 1},' \
            f' Courses: {self.courses}'
        else:
            return f'Before College: Courses{self.courses}'


if __name__ == '__main__':
    ciic = import_curriculum('CIIC')
    my_past_semesters = {
        '0': ['INGL3--1', 'ESPA3101', 'MATE3005', 'INGL3--2', 'ESPA3102'],
        '1': ['MATE3031', 'QUIM3131', 'INGL3211', 'INGE3011', 'SOHU1111'],
        '2': ['MATE3032', 'QUIM3132', 'CIIC3011', 'EDFI---1', 'EDFI---2'],
        '3': ['CIIC5--1', 'CIIC5--2'],
        '4': ['CIIC4010', 'CIIC3075', 'INGL3212', 'FREE---1'],
    }
    plan = StudentPlan(curriculum=ciic, max_credits=16, past_semesters=my_past_semesters)
    # for semester_index in range(5):
    #     semester = plan.add_semester(semester_index, past=True)
    #     if semester_index == 0:
    #         for course in ['INGL3--1', 'ESPA3101', 'MATE3005', 'INGL3--2', 'ESPA3102']:
    #             semester.add_course(ciic.get_course(course))
    #     if semester_index == 1:
    #         for course in ['MATE3031', 'QUIM3131', 'INGL3211', 'INGE3011', 'SOHU1111']:
    #             semester.add_course(ciic.get_course(course))
    #     if semester_index == 2:
    #         for course in ['MATE3032', 'QUIM3132', 'CIIC3011', 'EDFI---1', 'EDFI---2']:
    #             semester.add_course(ciic.get_course(course))
    #     if semester_index == 3:
    #         for course in ['CIIC5--1', 'CIIC5--2']:
    #             semester.add_course(ciic.get_course(course))
    #     if semester_index == 4:
    #         for course in c:
    #             semester.add_course(ciic.get_course(course))

    # semester = plan.add_semester(6)
    # semester.add_course(ciic.get_course('MATE3063'))
    for semester in plan.build_plan():
        print(semester, semester.credit_hours)