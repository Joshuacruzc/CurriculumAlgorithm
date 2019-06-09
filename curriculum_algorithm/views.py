from rest_framework import generics

from curriculum_algorithm.serializers import StudentPlanSerializer


class CreateStudentPlanView(generics.CreateAPIView):
    serializer_class = StudentPlanSerializer
