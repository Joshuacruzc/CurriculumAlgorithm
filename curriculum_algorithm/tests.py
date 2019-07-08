from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from curriculum_algorithm.models import StudentPlan
from import_curriculum import import_curriculum


class StudentPlanTestCase(APITestCase):
    def post_student_plan(self, curriculum_id, max_credits):
        url = reverse('create_student_plan')
        data = {'curriculum_id': curriculum_id, 'max_credits': max_credits}
        return self.client.post(url, data, format='json')

    def get_student_plan(self, id):
        url = reverse('view_plan')
        return self.client.get(url, format='json')

    def test_create_student_plan(self):
        """
        We can create a new StudentPlan object using API
        """
        import_curriculum('CIIC')
        StudentPlan.objects.all().delete()
        response = self.post_student_plan(1, 16)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Server did not return Status Code 201:'
                                                                        ' CREATED.')
        self.assertEqual(StudentPlan.objects.count(), 1, 'Student Plan was not created in database.')

    def test_retrieve_test_plan(self):
        """
        We can retrieve StudentPlan object using API
        """
        import_curriculum('CIIC')
        response = self.post_student_plan(1, 16)
        student_plan = json.loads(response.content)
        retrieved_student_plan = json.loads(self.get_student_plan(student_plan['id']))
        self.assertEqual(student_plan, retrieved_student_plan, 'Student Plan acquired from POST request is different '
                                                               'to the one in the GET request.')
        self.assertIn('semester_set', retrieved_student_plan.keys(), '"semester_set" not found in GET response'
                                                                     ' content.')
        self.assertIn('remaining_courses', retrieved_student_plan.keys(),
                      '"remaining_courses" not found in GET response content.')
        self.assertIn('max_credits', retrieved_student_plan.keys(),
                      '"max_credits" not found in GET response content.')
        self.assertIn('curriculum', retrieved_student_plan.keys(),
                      '"curriculum" not found in GET response content.')

