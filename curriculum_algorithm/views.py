from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from curriculum_algorithm.models import Semester, StudentPlan, CurriculumCourse
from curriculum_algorithm.serializers import StudentPlanSerializer, SemesterSerializer


@api_view(['POST'])
def transfer_course(request):
    if request.method == 'POST':
        data = request.POST
        semester = Semester.objects.get(pk=data['source_semester'])
        new_semester = Semester.objects.get(pk=data['new_semester'])
        course = CurriculumCourse.objects.get(pk=data['course_id'])
        semester.curriculum_courses.remove(course)
        new_semester.curriculum_courses.add(course)
        bops = Semester.objects.filter(id__in=[new_semester.id, semester.id])
        return Response(SemesterSerializer(bops, many=True).data)
    return Response({"message": "Hello, world!"})


class CreateStudentPlanView(generics.CreateAPIView):
    serializer_class = StudentPlanSerializer


class SemestersView(generics.ListCreateAPIView):
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    lookup_field = 'student_plan__id'


class RetrieveUpdateStudentPlanView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentPlanSerializer
    queryset = StudentPlan.objects.all()
    lookup_field = 'pk'
