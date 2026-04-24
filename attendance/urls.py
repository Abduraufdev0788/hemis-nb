from django.urls import path
from . import views

urlpatterns =[
    path('', views.home_page, name='home'), 

    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher-panel/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student-panel/', views.student_dashboard, name='student_dashboard'),
    path('mark-attendance/<int:group_id>/<int:subject_id>/', views.mark_attendance, name='mark_attendance'),
    path('admin-panel/add-group/', views.add_group, name='add_group'),
    path('admin-panel/add-subject/', views.add_subject, name='add_subject'),
]