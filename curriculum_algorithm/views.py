from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from curriculum_algorithm.models import Semester, StudentPlan, CurriculumCourse
from curriculum_algorithm.serializers import StudentPlanSerializer, SemesterSerializer


@api_view(['POST'])
def transfer_course(request):
    data = request.POST
    source_semester_pk = data.get('source_semester', None)
    destination_semester_pk = data.get('new_semester', None)
    course = CurriculumCourse.objects.get(pk=data['course_id'])
    updated_semesters = []
    if source_semester_pk is not None:
        source_semester = Semester.objects.get(pk=source_semester_pk)
        source_semester.curriculum_courses.remove(course)
        updated_semesters.append(source_semester_pk)
    if destination_semester_pk is not None:
        new_semester = Semester.objects.get(pk=data['new_semester'])
        new_semester.curriculum_courses.add(course)
        updated_semesters.append(destination_semester_pk)
    result = Semester.objects.filter(id__in=updated_semesters)
    return Response(SemesterSerializer(result, many=True).data)


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
