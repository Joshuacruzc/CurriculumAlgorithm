from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from CurriculumAlgorithmWebApp import settings

MAXIMUM_SEMESTER_CREDITS = 21

DEPARTMENT_CHOICES = [
    ('INSO', 'Software Engineering'),
    ('CIIC', 'Computer Science and Engineering'),
]

POSITION_CHOICES = [
    ('0', 'Fall'),
    ('1', 'Spring'),
    ('2', 'Summer'),
    ('3', 'Always'),
]


class Course(models.Model):

    # TODO: Add pre-requisite and co-requisite. What is "position" field?
    code = models.CharField(max_length=4)
    season = models.CharField(max_length=1, choices=POSITION_CHOICES)
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES)
    credit_hours = models.IntegerField(default=0)

    @property
    def course_id(self):
        return '%s%s' % (self.department, self.code)

    def __str__(self):
        return self.course_id

    def get_credit_hours(self):
        if hasattr(self, 'laboratory'):
            return self.credit_hours + self.laboratory.credit_hours
        else:
            return self.credit_hours

    # def get_level(self):
    #     level = 1
    #     for course in self.pre_requisites:
    #         inner_level = course.get_level()
    #         if inner_level >= level:
    #             level = inner_level + 1
    #     return level


# TODO: co-requisite and laboratory are special types of courses?
class Laboratory(Course):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)


class Curriculum(models.Model):
    courses = models.ManyToManyField(Course, related_name='courses')
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES)

    def get_concentration_courses(self):
        return [course for course in self.courses.all() if course.department == self.department]

    def get_course(self, course_id):
        for course in self.courses.all():
            if course.course_id == course_id:
                return course
        return None

    def get_total_credit_hours(self):
        credit_hours = 0
        for course in self.courses.all():
            credit_hours += course.credit_hours
        return credit_hours

    # def get_minimun_semester_count(self):
    #     max_level = 0
    #     for course in self.courses.all():
    #         max_level = max(max_level, course.get_level())
    #     return max_level


class Semester(models.Model):
    is_full = models.BooleanField(default=False, null=True)
    past = models.BooleanField(default=False, null=True)
    credit_hours = models.IntegerField(default=0)
    max_credits = models.IntegerField(validators=[
        MaxValueValidator(22, settings.ERROR_MESSAGES['semester_credits']['max_semester_credits']),
        MinValueValidator(11, settings.ERROR_MESSAGES['semester_credits']['min_semester_credits'])])
    position = models.IntegerField(default=0)

    def get_year(self):
        return int(self.position/2) if self.position % 2 == 0 else self.position//2 + 1
    year = property(get_year)


