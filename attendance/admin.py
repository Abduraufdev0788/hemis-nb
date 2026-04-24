from django.contrib import admin
from .models import Group, Subject, StudentProfile, Attendance

admin.site.register(Group)
admin.site.register(Subject)
admin.site.register(StudentProfile)
admin.site.register(Attendance)
