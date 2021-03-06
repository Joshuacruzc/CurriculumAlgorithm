from django.contrib.auth import get_user_model
from django.db import models

POSITION_CHOICES = [
    ('0', 'Any'),
    ('1', 'Fall'),
    ('2', 'Spring'),
]


class BaseModel(models.Model):
    class Meta:
        abstract = True


class PlanWarning(BaseModel):
    PRE_REQUISITE_NOT_MET = "Pre-requisite %s not met"
    CO_REQUISITE_NOT_MET = "Co-requisite %s met"
    MAX_CREDITS_EXCEEDED = "Max credits for %s exceeded"

    text = models.CharField(max_length=64)

    def __str__(self):
        return self.text


class Course(BaseModel):
    course_number = models.CharField(max_length=8, unique=True)
    season = models.CharField(max_length=1, choices=POSITION_CHOICES)
    credit_hours = models.IntegerField(default=0)
    laboratory = models.ForeignKey('Course', null=True,
                                   on_delete=models.SET_NULL,
                                   related_name='main_course')

    def __str__(self):
        return self.course_number


class Curriculum(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=50)
    courses = models.ManyToManyField(Course, through='CurriculumCourse')

    def __str__(self):
        return self.name


class CurriculumCourse(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    pre_requisites = models.ManyToManyField('self', related_name='unlocked',
                                            symmetrical=False)
    co_requisites = models.ManyToManyField("self", related_name='co_unlocked',
                                           symmetrical=False)
    level = models.IntegerField(default=0)
    plan_warnings = models.ManyToManyField(PlanWarning)

    @property
    def position(self):
        return self.semester_set.last().position

    def add_pre_requisite(self, curriculum_course):
        self.pre_requisites.add(curriculum_course)
        self.level = max(self.level, curriculum_course.level) + 1
        self.save()

    def generate_warnings(self):
        # Clears warnings before generating them
        self.plan_warnings.all().delete()

        # Checks if pre_requisites for course are met
        for pre_requisite in self.pre_requisites.all():
            if not pre_requisite.position or \
                    pre_requisite.position >= self.position:
                warning = PlanWarning.objects.create(
                    text=PlanWarning.PRE_REQUISITE_NOT_MET % pre_requisite)
                self.plan_warnings.add(warning)

        # Checks if co_requisites for course are met
        for co_requisite in self.co_requisites.all():
            if not co_requisite.position or self.position > self.position:
                warning = PlanWarning.objects.create(
                    text=PlanWarning.CO_REQUISITE_NOT_MET % co_requisite)
                self.plan_warnings.add(warning)
        # Generates warnings for all courses who depend on this one
        for curriculum_course in (self.unlocked.all() | self.unlocked.all()):
            curriculum_course.generate_warnings()

    @property
    def credit_hours(self):
        return self.course.credit_hours + self.course.laboratory.credit_hours \
            if self.course.laboratory else self.course.credit_hours

    def __str__(self):
        return f'{self.course.course_number}'


class Semester(BaseModel):
    student_plan = models.ForeignKey('StudentPlan', on_delete=models.CASCADE)
    curriculum_courses = models.ManyToManyField(CurriculumCourse)
    is_full = models.BooleanField(default=False)
    past = models.BooleanField(default=False)
    max_credits = models.PositiveIntegerField()
    position = models.IntegerField(default=0)
    credit_hours = models.IntegerField(default=0)
    plan_warnings = models.ManyToManyField(PlanWarning)

    @property
    def year(self):
        if self.position % 2 == 0:
            year = int(self.position / 2)
        else:
            year = self.position // 2 + 1
        return year

    def __str__(self):
        return f'Semester: year:{self.year}' \
               f'  semester: {2 if self.position % 2 == 0 else 1}'

    def add_curriculum_course(self, curriculum_course):
        self.curriculum_courses.add(curriculum_course)
        if curriculum_course.course.laboratory:
            self.curriculum_courses.add(CurriculumCourse.objects.get(
                course=curriculum_course.course.laboratory))
        self.credit_hours += curriculum_course.credit_hours
        self.is_full = self.credit_hours >= self.max_credits
        self.save()

    def generate_warnings(self):
        # Clear warnings before generating them
        self.plan_warnings.all().delete()

        # Check if semester exceeds maximum credits
        if self.credit_hours > self.max_credits:
            warning = PlanWarning.objects.create(
                text=PlanWarning.MAX_CREDITS_EXCEEDED % self)
            self.plan_warnings.add(warning)

    def remove_curriculum_course(self, course):
        self.curriculum_courses.remove(course)
        course.plan_warnings.all().delete()
        self.generate_warnings()

    def course_valid(self, curriculum_course):
        if not self.is_full and not self.past \
                and self.credit_hours \
                + curriculum_course.credit_hours <= self.max_credits:
            if curriculum_course.course.season == 2:
                return self.position % 2 == 0
            elif curriculum_course.course.season == 1:
                return self.position % 2 == 1
            else:
                return True


class StudentPlan(BaseModel):
    max_credits = models.IntegerField(default=0)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.SET_NULL,
                                   null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True)

    @property
    def remaining_courses(self):
        return CurriculumCourse.objects.filter(curriculum=self.curriculum) \
            .exclude(semester__in=self.semester_set.all()) \
            .order_by('-level')

    def build_plan(self):
        self.semester_set.filter(past=False).delete()
        for course in self.remaining_courses:
            self.accommodate(course)
        return self.semester_set

    def force_accommodate(self, position, curriculum_course):
        target_semester = self.semester_set.filter(position=position).first()
        if not target_semester:
            target_semester = Semester.objects.create(
                student_plan=self,
                max_credits=self.max_credits,
                position=position)
        target_semester.add_curriculum_course(curriculum_course)
        curriculum_course.generate_warnings()
        target_semester.generate_warnings()

    def accommodate(self, curriculum_course, is_co_requisite=False):
        if curriculum_course not in self.remaining_courses:
            return curriculum_course.semester_set.last().position + 1 \
                if not is_co_requisite \
                else curriculum_course.semester_set.last().position
        min_position = 1
        for pre_requisite in curriculum_course.pre_requisites.all():
            min_position = max(min_position, self.accommodate(pre_requisite))
        for co_requisite in curriculum_course.co_requisites.all():
            min_position = max(min_position, self.accommodate(
                co_requisite,
                is_co_requisite=True))
        min_position = self.set_to_earliest_possible_semester(
            min_position=min_position,
            curriculum_course=curriculum_course)
        return min_position + 1 if not is_co_requisite else min_position

    def set_to_earliest_possible_semester(self, curriculum_course,
                                          min_position):
        if not self.semester_set.filter(position=min_position).exists():
            Semester.objects.create(student_plan=self,
                                    max_credits=self.max_credits,
                                    position=min_position)
        for semester in self.semester_set.filter(
                position__gte=min_position).order_by('position'):
            if semester.course_valid(curriculum_course):
                semester.add_curriculum_course(curriculum_course)
                return semester.position
        # TODO: Consider using max aggregate
        new_semester = Semester.objects.create(
            student_plan=self,
            max_credits=self.max_credits,
            position=self.semester_set.count())
        new_semester.add_curriculum_course(curriculum_course)
        return new_semester.position
