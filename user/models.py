from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.



class UserBot(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name



class VipMembers(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    GENDERS = {
        ('female', 'زن'),
        ('male', 'مرد'),
        ('unknown', 'ناشناخته')
    }
    gender = models.CharField(max_length=10, choices=GENDERS, blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, unique=True, max_length=11, validators=[MinLengthValidator(11)])
    telegram_id = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    STATUS = [
        ('instagram', 'ارتباط از اینستا'),
        ('subscribed', 'عضو کانال'),
        ('unsubscribed', 'لغو عضویت'),
        ('guest', 'مهمان'),
        ('conditions', 'درخواست شرایط'),
        ('resubscribed', 'تمدید عضویت'),
        ('unresubscribed', 'عدم تمدید')
    ]
    status = models.CharField(max_length=20, blank=True, null=True, choices=STATUS)
    conract_start_date = models.DateTimeField(blank=True, null=True)
    contract_end_date = models.DateTimeField(blank=True, null=True)
    SKILL_LEVELS = [
        ('advanced', 'پیشرفته'),
        ('intermediate', 'متوسط'),
        ('beginner', 'مبتدی')
    ]
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS, blank=True, null=True)
    last_checked = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)