
class Curriculum:

    def __init__(self, department, courses=None):
        self.department = department
        if courses is None:
            self.courses = list()
        else:
            self.courses = courses

    def get_concentration_courses(self):
        return [course for course in self.courses if course.department == self.department]

    def get_course(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course

    def get_total_credit_hours(self):
        credits_hours = 0
        for course in self.courses:
            credits_hours += course.credit_hours
        return credits_hours

    def get_minimum_semester_count(self):
        max_level = 0
        for course in self.courses:
            max_level = max(max_level, course.get_level())
        return max_level
