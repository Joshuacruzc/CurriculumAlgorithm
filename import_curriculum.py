import os

import django

from Course import Course
from Curriculum import Curriculum

os.environ['DJANGO_SETTINGS_MODULE'] = 'CurriculumAlgorithmWebApp.settings'
django.setup()
from curriculum_algorithm.models import CurriculumCourse as CourseModel
from curriculum_algorithm.models import Course as CurriculumCourseModel
from curriculum_algorithm.models import Curriculum as CurriculumModel


def import_curriculum(name):
    file = open(name + '.txt', 'r')
    curriculum = CurriculumModel.objects.create(name=name)
    for line in file:
        line = line.split()
        course = CurriculumCourseModel.objects.create(curriculum=curriculum,
                                                      course=CourseModel.objects.create(course_number=line[0],
                                                                                        credit_hours=int(line[1])))
        if line[2] != '--------':
            courses = line[2].split(',')
            for correq in courses:
                course.co_requisites.add(
                    CurriculumCourseModel.objects.filter(course__course_number=correq, curriculum=curriculum).first())
        if line[3] != '--------':
            courses = line[3].split(',')
            for prereq in courses:
                course.add_pre_requisite(
                    CurriculumCourseModel.objects.filter(course__course_number=prereq, curriculum=curriculum).first())
        if line[4] != '--------':
            lab = CurriculumCourseModel.objects.create(curriculum=curriculum,
                                                       course=CourseModel.objects.create(course_number=line[4],
                                                                                         credit_hours=1))
            course.course.laboratory = lab.course
            course.course.save()
        if line[5] != '--------':
            course.course.season = int(line[5][-1])
            course.course.save()
        course.save()

    return curriculum


def import_curriculum_local(name):
    file = open(name + '.txt', 'r')
    curriculum = Curriculum(department=name)
    for line in file:
        line = line.split()
        print(line)
        course = Course(department=line[0][:4], code=line[0][4:], credit_hours=int(line[1]))
        curriculum.courses.append(course)
        if line[2] != '--------':
            courses = line[2].split(',')
            for correq in courses:
                course.co_requisites.append(curriculum.get_course(correq))
        if line[3] != '--------':
            courses = line[3].split(',')
            for prereq in courses:
                course.pre_requisites.append(curriculum.get_course(prereq))
        if line[4] != '--------':
            lab = Course(department=line[4][:4], code=line[4][4:], credit_hours=1)
            curriculum.courses.append(lab)
            course.lab = lab
        if line[5] != '--------':
            course.season = int(line[5][-1])
    return curriculum


if __name__ == '__main__':
    import_curriculum('CIIC')