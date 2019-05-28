from django.contrib import admin

from curriculum_algorithm.models import Curriculum, Course, CurriculumCourse, StudentPlan, Semester


class CurriculumCourseInline(admin.TabularInline):
    fields = ['course', 'pre_requisites', 'co_requisites']
    fk_name = 'curriculum'
    model = CurriculumCourse


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    fields = ['name', 'department']
    inlines = [CurriculumCourseInline]


class SemesterInline(admin.TabularInline):
    fields = ['curriculum_courses', 'position',  'past']
    fk_name = 'student_plan'
    model = Semester


@admin.register(StudentPlan)
class StudentPlanAdmin(admin.ModelAdmin):
    fields = ['max_credits', 'curriculum']
    inlines = [SemesterInline]
