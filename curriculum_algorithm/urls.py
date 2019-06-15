from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateStudentPlanView, RetrieveUpdateSemesterView, RetrieveUpdateStudentPlanView

urlpatterns = {
    url(r'^create_student_plan/$', CreateStudentPlanView.as_view(), name="create_student_plan"),
    path('view_semester/<int:pk>/', RetrieveUpdateSemesterView.as_view(), name='semester'),
    path('view_student_plan/<int:pk>/', RetrieveUpdateStudentPlanView.as_view(), name='semester')

}

urlpatterns = format_suffix_patterns(urlpatterns)