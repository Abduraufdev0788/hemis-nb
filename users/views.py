from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Parent, CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from attendance.models import StudentProfile
from django.contrib.auth import logout


class ParentCreateAPIView(APIView):
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        phone_number = request.data.get('phone_number')
        name = request.data.get('name')

        if not all([telegram_id, phone_number, name]):
            return Response({"error": "Ma'lumot to'liq emas!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        # Telefon raqamni tozalash
        clean_phone = phone_number.replace('+', '')

        # Ota-onani saqlash yoki bazadan olish
        parent, created = Parent.objects.get_or_create(
            phone_number=clean_phone,
            defaults={'telegram_id': telegram_id, 'name': name}
        )

        # Agar bazada allaqachon bor bo'lsa
        if not created:
            return Response(
                {"message": "Ushbu raqam bazada allaqachon ro'yxatdan o'tgan!"}, 
                status=status.HTTP_400_BAD_REQUEST # yoki 200_OK, loyihangiz mantig'iga qarab
            )

        return Response({"message": "Muvaffaqiyatli saqlandi"}, status=status.HTTP_201_CREATED)
    

class CustomLoginView(LoginView):
    template_name = 'login.html'

@login_required
def dashboard_redirect(request):
    """Rolga qarab kerakli sahifaga yo'naltiruvchi mantiq"""
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')

def register_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        parent_phone = request.POST.get('parent_phone').replace('+', '')

        # User yaratamiz
        user = CustomUser.objects.create_user(
            username=username, password=password, first_name=first_name, role='student'
        )
        
        # Ota-onani raqam orqali topamiz (Bot orqali start bosgan bo'lishi kerak)
        parent = Parent.objects.filter(phone_number__contains=parent_phone).first()
        
        # Talaba profilini yaratish
        StudentProfile.objects.create(user=user, parent=parent)
        
        return redirect('login')
    return render(request, 'register.html')



# users/views.py ichidagi qismni shunga almashtiring:

@login_required
def dashboard_redirect(request):
    """Rolga qarab kerakli sahifaga yo'naltiruvchi mantiq"""
    # Agar foydalanuvchi superuser bo'lsa yoki roli admin bo'lsa
    if request.user.role == 'admin' or request.user.is_superuser:
        return redirect('admin_dashboard')
    elif request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')
    

from django.contrib import messages
from attendance.models import Group, StudentProfile

@login_required
def add_teacher(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu login allaqachon band!")
        else:
            CustomUser.objects.create_user(
                username=username, password=password, first_name=first_name, role='teacher', phone_number=phone
            )
            messages.success(request, "O'qituvchi muvaffaqiyatli qo'shildi!")
            return redirect('admin_dashboard')
            
    return render(request, 'admin/add_teacher.html')

@login_required
def add_student(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    groups = Group.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        group_id = request.POST.get('group')
        parent_phone = request.POST.get('parent_phone').replace('+', '')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu login allaqachon band!")
        else:
            user = CustomUser.objects.create_user(
                username=username, password=password, first_name=first_name, role='student'
            )
            parent = Parent.objects.filter(phone_number__contains=parent_phone).first()
            group = Group.objects.get(id=group_id)
            StudentProfile.objects.create(user=user, parent=parent, group=group)
            
            messages.success(request, "Talaba muvaffaqiyatli qo'shildi!")
            return redirect('admin_dashboard')
            
    return render(request, 'admin/add_student.html', {'groups': groups})

def custom_logout(request):
    """Foydalanuvchini tizimdan chiqarish funksiyasi"""
    logout(request) # Django sessiyani tozalab, foydalanuvchini chiqarib yuboradi
    return redirect('home') 