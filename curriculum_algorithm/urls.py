from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateStudentPlanView, SemestersView, RetrieveUpdateStudentPlanView, transfer_course

urlpatterns = {
    url(r'create_student_plan/$', CreateStudentPlanView.as_view(), name="create_student_plan"),
    path(r'view_student_plan/<int:pk>/$', RetrieveUpdateStudentPlanView.as_view(), name='view_plan'),
    path(r'transfer_course/$', transfer_course, name='transfer_course')
}

urlpatterns = format_suffix_patterns(urlpatterns)