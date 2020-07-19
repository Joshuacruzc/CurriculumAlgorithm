from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from curriculum_algorithm.models import StudentPlan
from import_curriculum import import_curriculum


class CARequestsMixin:
    client = None

    def post_student_plan(self, curriculum_id, max_credits):
        url = reverse('create_student_plan')
        data = {'curriculum_id': curriculum_id, 'max_credits': max_credits}
        return self.client.post(url, data, format='json')

    def get_student_plan(self, student_plan_id):
        url = reverse('view_plan', args=(student_plan_id,))
        return self.client.get(url, format='json')

    def accommodate_remaining_courses(self, student_plan_id):
        url = reverse('build_plan', args=(student_plan_id,))
        return self.client.get(url, format='json')

    def get_user_info(self):
        url = reverse('get_current_user')
        return self.client.get(url, format='json')


class StudentPlanTestCase(CARequestsMixin, APITestCase):
    def setUp(self):
        user = get_user_model().objects.create(username='test_user', password='test')
        self.client.force_authenticate(user=user)

    def test_create_student_plan(self):
        """
        We can create a new StudentPlan object using API
        """
        import_curriculum('CIIC')
        StudentPlan.objects.all().delete()
        response = self.post_student_plan(curriculum_id=1, max_credits=16)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Server did not return Status Code 201:'
                                                                        ' CREATED.')
        self.assertEqual(StudentPlan.objects.count(), 1, 'Student Plan was not created in database.')

    def test_retrieve_test_plan(self):
        """
        We can retrieve StudentPlan object using API
        """
        import_curriculum('CIIC')
        response = self.post_student_plan(curriculum_id=1, max_credits=16)
        student_plan = json.loads(response.content)
        retrieved_student_plan = json.loads(self.get_student_plan(student_plan['id']).content)
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

    def test_accommodate_remaining_courses(self):
        """
        We can accommodate all remaining courses using "accommodate remaining courses endpoint
        """
        import_curriculum('CIIC')
        StudentPlan.objects.all().delete()
        response = self.post_student_plan(curriculum_id=1, max_credits=16)
        created_student_plan = json.loads(response.content)
        self.assertEqual(0, len(created_student_plan['semester_set']), 'Student Plan that was just created already has'
                                                                       'semesters.')
        response = self.accommodate_remaining_courses(student_plan_id=created_student_plan['id'])
        retrieved_student_plan = json.loads(response.content)
        self.assertEqual(0, len(retrieved_student_plan['remaining_courses']), 'Courses left without accommodating.')


class AuthenticationTestCase(CARequestsMixin, APITestCase):

    def test_get_user_info(self):
        """
        We can retrieve User info using API
        """
        user = get_user_model().objects.create(username='test_user', password='test')

        self.client.force_authenticate(user=user)
        response = self.get_user_info()
        data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Server did not return Status Code: 200')
        self.assertEqual(data['username'], user.username)

    def test_unauthorized_requests(self):
        """
        Verifies that no endpoint can be accessed without authentication
        :return:
        """
        response = self.post_student_plan(curriculum_id=1, max_credits=16)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Server did not return Status Code: 401')
        response = self.get_student_plan(student_plan_id=1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Server did not return Status Code: 401')
        response = self.accommodate_remaining_courses(student_plan_id=1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Server did not return Status Code: 401')
        response = self.get_user_info()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Server did not return Status Code: 401')
