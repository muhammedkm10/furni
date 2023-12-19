from django.db import models
from django.shortcuts import redirect
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
import pyotp




# Create your models here.


# user signup 

class CustomUser1(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField()
    phone  = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.username


# otp storing table
class otpverification(models.Model):
    user = models.OneToOneField(CustomUser1, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=200)
    otp_nuber = models.IntegerField()


# otp generation
def generate_otp(user):
    secret_key = pyotp.random_base32()
    otp = pyotp.TOTP(secret_key)
    otp_code = otp.now()
    user_profile = otpverification.objects.create(user=user, otp_secret=secret_key,otp_nuber=otp_code)
    return otp_code

# Send OTP email
def send_otp_email(email, otp_code):
    subject = 'OTP Verification'
    message = f'Your OTP for verification is: {otp_code}'
    from_email = 'muhammedmamu2906@gmail.com'  # Replace with your email
    send_mail(subject, message, from_email, [email])



# signal to post save
@receiver(post_save, sender=CustomUser1)
def generate_and_send_otp(sender, instance, created, **kwargs):
    if created:
        otp_code = generate_otp(instance)
        send_otp_email(instance.email, otp_code)

        

    