from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Group, Subject, Attendance, StudentProfile
from datetime import date

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('dashboard_redirect')
    
    today = date.today()
    # Optimizatsiya (N+1 oldini olish u-n annotate)
    groups = Group.objects.annotate(
        today_absent=Count(
            'students__attendances', 
            filter=Q(students__attendances__date=today, students__attendances__is_present=False)
        )
    )
    return render(request, 'admin/dashboard.html', {'groups': groups})

@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('dashboard_redirect')
        
    subjects = Subject.objects.filter(teacher=request.user)
    groups = Group.objects.all() # Aslida fanga biriktirilgan guruhlar olinishi kerak
    
    return render(request, 'teacher/dashboard.html', {'subjects': subjects, 'groups': groups})

@login_required
def mark_attendance(request, group_id, subject_id):
    group = get_object_or_404(Group, id=group_id)
    subject = get_object_or_404(Subject, id=subject_id, teacher=request.user)
    
    # select_related orqali optimizatsiya
    students = StudentProfile.objects.filter(group=group).select_related('user')

    if request.method == "POST":
        today = date.today()
        # Kelganlar ro'yxati (Galochka qoldirilganlar)
        present_student_ids = request.POST.getlist('is_present')
        
        attendance_records =[]
        for student in students:
            is_present = str(student.id) in present_student_ids
            # Bazani ortiqcha zo'riqtirmaslik uchun update_or_create
            obj, created = Attendance.objects.update_or_create(
                student=student, subject=subject, date=today,
                defaults={'is_present': is_present}
            )
        return redirect('teacher_dashboard')

    return render(request, 'teacher/mark_attendance.html', {
        'group': group, 'subject': subject, 'students': students
    })

@login_required
def student_dashboard(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    # Fanlar bo'yicha jami NB larni hisoblash
    absences = Attendance.objects.filter(student=profile, is_present=False)\
        .values('subject__name').annotate(total_nb=Count('id'))
    
    return render(request, 'student/dashboard.html', {'absences': absences})

# attendance/views.py faylining ichiga quyidagini qo'shing

def home_page(request):
    # Agar foydalanuvchi oldin tizimga kirgan bo'lsa, to'g'ridan-to'g'ri paneliga o'tib ketadi
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    # Aks holda chiroyli Asosiy sahifa ochiladi
    return render(request, 'home.html')



# attendance/views.py ichidagi admin_dashboard funksiyasi

from users.models import CustomUser

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    today = date.today()
    # Guruhlar va ularning bugungi NB lari
    groups = Group.objects.annotate(
        today_absent=Count(
            'students__attendances', 
            filter=Q(students__attendances__date=today, students__attendances__is_present=False)
        )
    )
    
    # Qo'shimcha statistika
    total_students = CustomUser.objects.filter(role='student').count()
    total_teachers = CustomUser.objects.filter(role='teacher').count()
    total_absent_today = Attendance.objects.filter(date=today, is_present=False).count()
    
    context = {
        'groups': groups,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_absent_today': total_absent_today,
    }
    return render(request, 'admin/dashboard.html', context)





from django.contrib import messages
from users.models import CustomUser

@login_required
def add_group(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        if Group.objects.filter(name=name).exists():
            messages.error(request, "Bu guruh bazada mavjud!")
        else:
            Group.objects.create(name=name)
            messages.success(request, "Yangi guruh yaratildi!")
            return redirect('admin_dashboard')
            
    return render(request, 'admin/add_group.html')

@login_required
def add_subject(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    teachers = CustomUser.objects.filter(role='teacher')
    if request.method == 'POST':
        name = request.POST.get('name')
        teacher_id = request.POST.get('teacher')
        teacher = CustomUser.objects.get(id=teacher_id)
        
        Subject.objects.create(name=name, teacher=teacher)
        messages.success(request, "Yangi fan yaratildi!")
        return redirect('admin_dashboard')
        
    return render(request, 'admin/add_subject.html', {'teachers': teachers})