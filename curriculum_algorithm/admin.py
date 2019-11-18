from django.contrib import admin

from curriculum_algorithm.models import Curriculum, CurriculumCourse, StudentPlan, Semester


class CurriculumCourseInline(admin.TabularInline):
    fields = ['course', 'pre_requisites', 'co_requisites', 'plan_warnings']
    fk_name = 'curriculum'
    model = CurriculumCourse


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    fields = ['name', 'department']
    inlines = [CurriculumCourseInline]


class SemesterInline(admin.TabularInline):
    fields = ['curriculum_courses', 'credit_hours', 'position', 'past', 'plan_warnings']
    fk_name = 'student_plan'
    model = Semester
    extra = 0


@admin.register(StudentPlan)
class StudentPlanAdmin(admin.ModelAdmin):
    fields = ['max_credits', 'curriculum', 'user']
    inlines = [SemesterInline]

    def save_model(self, request, obj, form, change):
        super(StudentPlanAdmin, self).save_model(request, obj, form, change)
        obj.build_plan()
