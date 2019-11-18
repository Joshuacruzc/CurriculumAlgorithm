from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import CreateStudentPlanView, RetrieveUpdateStudentPlanView, transfer_course, \
    accommodate_remaining_courses, CurrentUserView

urlpatterns = {
    path('create_student_plan/', CreateStudentPlanView.as_view(), name="create_student_plan"),
    path('view_student_plan/<int:pk>/', RetrieveUpdateStudentPlanView.as_view(), name='view_plan'),
    path('transfer_course/', transfer_course, name='transfer_course'),
    path('accommodate_remaining_courses/<int:student_plan_id>/', accommodate_remaining_courses, name='build_plan'),
    path('get_user_info/', CurrentUserView.as_view(), name='get_current_user'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
