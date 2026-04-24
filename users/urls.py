from django.urls import path
from attendance import views
from .views import ParentCreateAPIView
from .views import CustomLoginView, dashboard_redirect, register_student, add_teacher, add_student, custom_logout

urlpatterns =[
    path('api/parent/create/', ParentCreateAPIView.as_view(), name='api-parent-create'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_student, name='register'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('admin-panel/add-teacher/', add_teacher, name='add_teacher'),
    path('admin-panel/add-student/', add_student, name='add_student'),
    path('logout/', custom_logout, name='logout'),
]