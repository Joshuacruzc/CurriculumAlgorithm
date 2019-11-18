from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from curriculum_algorithm.models import Semester, StudentPlan, CurriculumCourse
from curriculum_algorithm.serializers import StudentPlanSerializer, SemesterSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_course(request):
    data = request.POST
    source_semester_pk = data.get('source_semester', None)
    destination_semester_pk = data.get('new_semester', None)
    course = CurriculumCourse.objects.get(pk=data['course_id'])
    updated_semesters = []
    if source_semester_pk is not None:
        source_semester = Semester.objects.get(pk=source_semester_pk)
        source_semester.remove_curriculum_course(course)
        updated_semesters.append(source_semester_pk)
    if destination_semester_pk is not None:
        new_semester = Semester.objects.get(pk=data['new_semester'])
        new_semester.student_plan.force_accommodate(new_semester, course)
        updated_semesters.append(destination_semester_pk)
    result = Semester.objects.filter(id__in=updated_semesters)
    return Response(SemesterSerializer(result, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accommodate_remaining_courses(request, student_plan_id):
    student_plan = StudentPlan.objects.get(pk=student_plan_id)
    student_plan.build_plan()
    return Response(StudentPlanSerializer(student_plan).data)


class CreateStudentPlanView(generics.CreateAPIView):
    serializer_class = StudentPlanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        extra_data = {}
        if 'user' not in serializer.validated_data:
            extra_data['user'] = self.request.user
        serializer.save(**extra_data)


class SemestersView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    lookup_field = 'student_plan__id'


class RetrieveUpdateStudentPlanView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentPlanSerializer
    queryset = StudentPlan.objects.all()
    lookup_field = 'pk'


class CurrentUserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
