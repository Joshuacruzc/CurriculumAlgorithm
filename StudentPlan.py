from import_curriculum import import_curriculum_local


class StudentPlan:
    semesters = []
    flags = {}

    def __init__(self, curriculum, max_credits, past_semesters=None):
        self.curriculum = curriculum
        self.max_credits = max_credits
        if past_semesters is not None:
            for semester_position in range(max(past_semesters.keys()) + 1):
                past_semester = self.add_semester(semester_position, past=True)
                courses_to_add = past_semesters.get(semester_position, [])
                for course in courses_to_add:
                    past_semester.add_course(curriculum.get_course(course))

    def build_plan(self):
        sorted_courses = sorted(self.curriculum.courses, key=lambda c: c.level,
                                reverse=True)
        for course in sorted_courses:
            self.accommodate(course)
        return self.semesters

    def accommodate(self, course, co_requisite=False):
        if course.position is not None:
            return course.position + 1 if not co_requisite else course.position
        min_position = 0
        for pre_requisite in course.pre_requisites:
            min_position = max(min_position, self.accommodate(pre_requisite))
        for co_requisite in course.co_requisites:
            min_position = max(min_position, self.accommodate(
                co_requisite,
                co_requisite=True))
        min_position = self.set_to_earliest_possible_semester(
            min_position=min_position, course=course)
        return min_position + 1 if not co_requisite else course.position

    def add_semester(self, position, past=False):
        new_semester = Semester(max_credits=self.max_credits,
                                position=position,
                                past=past)
        self.semesters.append(new_semester)
        return new_semester

    def force_accommodate(self, position, course):
        target = self.get_semester(position)
        if not target:
            target = self.add_semester(position)
        target.add_course(course)
        self.generate_warnings(course, position)

    def generate_warnings(self, course, position):
        for pre_requisite in course.pre_requisites:
            if not pre_requisite.position \
                    or pre_requisite.position >= course.position:
                self.flags[
                    course.course_id] = \
                    f'Prerequisite {pre_requisite.course_id}' f' not met'
        for co_requisite in course.co_requisites:
            if not co_requisite.position \
                    or course.position > co_requisite.position:
                self.flags[
                    course.course_id] = \
                    f'co-requisite {co_requisite.course_id} not met'
        target_semester = self.get_semester(position)
        if target_semester.credit_hours > target_semester.max_credits:
            self.flags[
                f'Semester {target_semester.position}'] = \
                f"Max credits exceeded in {target_semester}"

    def get_semester(self, position):
        for sem in self.semesters:
            if sem.position == position:
                return sem

    def set_to_earliest_possible_semester(self, course, min_position):
        if not self.get_semester(min_position):
            self.add_semester(position=min_position)
        self.semesters = sorted(self.semesters, key=lambda s: s.position, )
        for semester_index in range(min_position, len(self.semesters)):
            if self.semesters[semester_index].course_valid(course):
                self.semesters[semester_index].add_course(course)
                return semester_index
        new_semester = self.add_semester(position=len(self.semesters))
        new_semester.add_course(course)
        return new_semester.position

    def remove(self, course):
        position = course.position
        course.position = None
        sem = self.get_semester(position)
        sem.courses.remove(course)
        self.flags.pop(course.course_id)


class Semester:
    is_full = False
    credit_hours = 0

    def __init__(self, max_credits, position, past=False):
        self.max_credits = max_credits
        self.position = position
        self.courses = list()
        self.past = past

    def course_valid(self, course):
        if not self.is_full and not self.past and self.credit_hours \
                + course.get_credit_hours() <= self.max_credits:
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
        if self.position % 2 == 0:
            year = int(self.position / 2)
        else:
            year = self.position // 2 + 1
        return year

    year = property(get_year)

    def __repr__(self):
        if self.position > 0:
            return f'Semester: year:{self.year}  ' \
                   f'semester: {2 if self.position % 2 == 0 else 1},' \
                   f' Courses: {self.courses}'
        else:
            return f'Before College: Courses{self.courses}'


if __name__ == '__main__':
    # Example Use
    ciic = import_curriculum_local('CIIC')
    my_past_semesters = {
        0: ['INGL3--1', 'ESPA3101', 'MATE3005', 'INGL3--2', 'ESPA3102'],
        1: ['MATE3031', 'QUIM3131', 'INGL3211', 'INGE3011', 'SOHU1111'],
        2: ['MATE3032', 'QUIM3132', 'CIIC3011', 'EDFI---1', 'EDFI---2', 'CIIC5--1', 'CIIC5--2'],
        3: ['CIIC4010', 'CIIC3075', 'INGL3212', 'FREE---1'],
        4: ['CIIC4020', 'SOHU1112', 'FISI3171'],
        5: ['CIIC4025', 'INEL3105', 'FISI3172', 'MATE3063'],
        6: ['CIIC4030', 'CIIC3081', 'CIIC5045', 'MATE4145', 'SOHU1113']
    }
    everson_semester = {
        1: ['MATE3005', 'QUIM3131', 'INGL3--1', 'INGE3011', 'ESPA3101'],
        2: ['MATE3031', 'QUIM3132', 'INGL3--2', 'EDFI---1', 'EDFI---2',
            'ESPA3102'],
        3: ['MATE3032', 'CIIC3011', 'FISI3171', 'INGL3211'],
        4: ['MATE3063', 'CIIC4010', 'CIIC3075', 'FISI3172', 'INGL3212'],
        5: ['CIIC4020', 'MATE4145', 'INEL3105', 'INGE3035'],
        6: ['CIIC5--1']
    }
    plan = StudentPlan(curriculum=ciic, max_credits=16,
                       past_semesters=my_past_semesters)
    # plan.remove(ciic.get_course('MATE3063'))
    # plan.accommodate(ciic.get_course('MATE3063'))
    # plan.force_accommodate(9, ciic.get_course("CIIC4082"))
    # plan.force_accommodate(11, ciic.get_course("CIIC4070"))
    # plan.force_accommodate(11, ciic.get_course("CIIC5995"))
    for semester in plan.build_plan():
        print(semester, semester.credit_hours)
    print(plan.flags)
