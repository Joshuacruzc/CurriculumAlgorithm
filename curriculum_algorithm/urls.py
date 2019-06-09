from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateStudentPlanView

urlpatterns = {
    url(r'^create_student_plan/$', CreateStudentPlanView.as_view(), name="create_student_plan"),
}

urlpatterns = format_suffix_patterns(urlpatterns)