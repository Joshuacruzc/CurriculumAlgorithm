from rest_framework import serializers
from .models import StudentPlan, Semester, CurriculumCourse, Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class CurriculumCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = CurriculumCourse
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    curriculum_courses = CurriculumCourseSerializer(many=True)

    class Meta:
        model = Semester
        fields = '__all__'


class StudentPlanSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    semester_set = SemesterSerializer(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = StudentPlan
        fields = '__all__'