from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('grades/', views.grades, name='grades'),
    path('attendance/', views.attendance, name='attendance'),
] 