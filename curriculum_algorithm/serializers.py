from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import StudentPlan, Semester, CurriculumCourse, Course, \
    PlanWarning


class PlanWarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanWarning
        fields = ['text']


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class CurriculumCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    plan_warnings = PlanWarningSerializer(many=True)

    class Meta:
        model = CurriculumCourse
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    curriculum_courses = CurriculumCourseSerializer(many=True)
    plan_warnings = PlanWarningSerializer(many=True)

    class Meta:
        model = Semester
        fields = '__all__'


class StudentPlanSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    semester_set = SemesterSerializer(many=True, read_only=True)
    remaining_courses = CurriculumCourseSerializer(many=True, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = StudentPlan
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
