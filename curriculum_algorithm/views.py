from rest_framework import generics

from curriculum_algorithm.models import Semester, StudentPlan
from curriculum_algorithm.serializers import StudentPlanSerializer, SemesterSerializer


class CreateStudentPlanView(generics.CreateAPIView):
    serializer_class = StudentPlanSerializer


class RetrieveUpdateSemesterView(generics.RetrieveUpdateAPIView):
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    lookup_field = 'pk'


class RetrieveUpdateStudentPlanView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentPlanSerializer
    queryset = StudentPlan.objects.all()
    lookup_field = 'pk'
