class Course:

    def __init__(self, credit_hours, department, code, pre_requisites=None, co_requisites=None):
        self.course_id = department + code
        self.credit_hours = credit_hours
        self.department = department
        self.code = code
        if pre_requisites is None:
            self.pre_requisites = list()
        else:
            self.pre_requisites = pre_requisites
        if co_requisites is None:
            self.co_requisites = list()
        else:
            self.co_requisites = co_requisites

    def get_level(self):
        level = 1
        for course in self.pre_requisites:
            inner_level = course.get_level()
            if inner_level >= level:
                level = inner_level + 1
        return level

    def __repr__(self):
        return self.course_id


if __name__ == '__main__':
    print('bops')
