from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from curriculum_algorithm.models import StudentPlan


class StudentPlanTestCase(APITestCase):
    def test_create_test_plan(self):
        """
        Ensure we can create a new StudentPlan object.
        """
        url = reverse('create_student_plan')
        data = {'curriculum_id': 1, 'max_credits': 16}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StudentPlan.objects.count(), 1)
        self.assertEqual(StudentPlan.objects.get().max_credits, 16)