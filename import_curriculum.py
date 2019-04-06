from Course import Course
from Curriculum import Curriculum


def import_curriculum(name):
    file = open(name + '.txt', 'r')
    curriculum = Curriculum(department=name)
    for line in file:
        line = line.split()
        print(line)
        course = Course(department=line[0][:4], code=line[0][4:], credit_hours=int(line[1]))
        curriculum.courses.append(course)
        if line[3] != '--------':
            courses = line[3].split(',')
            for prereq in courses:
               course.pre_requisites.append(curriculum.get_course(prereq))
    print(curriculum.get_minimum_semester_count())


if __name__ == '__main__':
    import_curriculum('CIIC')