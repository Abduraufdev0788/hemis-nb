from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attendance
from django.conf import settings
import requests

def send_telegram_alert(chat_id, text):
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'})

@receiver(post_save, sender=Attendance)
def check_absences_and_notify(sender, instance, created, **kwargs):
    # Agar yangi yo'qlama yaratilsa va u "Kelmadi (NB)" bo'lsa
    if instance.pk and not instance.is_present:
        student = instance.student
        parent = student.parent
        
        if parent and parent.telegram_id:
            # Talabaning ushbu fandan barcha NB lari sonini hisoblash
            nb_count = Attendance.objects.filter(
                student=student, 
                subject=instance.subject, 
                is_present=False
            ).count()

            subject_name = instance.subject.name
            student_name = student.user.get_full_name() or student.user.username

            if nb_count == 3:
                msg = f"⚠️ <b>Ogohlantirish!</b>\nFarzandingiz <b>{student_name}</b> bugun <b>{subject_name}</b> fanidan dars qoldirdi.\nJami NB lar soni: 3 ta."
                send_telegram_alert(parent.telegram_id, msg)
            
            elif nb_count >= 5:
                msg = f"🚨 <b>Qat'iy Ogohlantirish (XAT)!</b>\nFarzandingiz <b>{student_name}</b> <b>{subject_name}</b> fanidan qatorasiga 5 marta (yoki undan ko'p) dars qoldirdi. Zudlik bilan dekanatga uchrashingiz so'raladi!"
                send_telegram_alert(parent.telegram_id, msg)