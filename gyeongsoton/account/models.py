from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):

    SEX_CHOICES = (("", "성별을 선택하세요"), ("남", "남"), ("여", "여"))

    AGE_CHOICES = (
        ("", "나이대를 선택하세요"),
        ("5", "10대 이하"),
        ("10", "10대"),
        ("20", "20대"),
        ("30", "30대"),
        ("40", "40대"),
        ("50", "50대 이상"),
    )

    sex = models.CharField(
        max_length=3, choices=SEX_CHOICES, help_text="성별을 선택하세요", null=False
    )
    age = models.CharField(
        max_length=10, choices=AGE_CHOICES, help_text="나이대를 선택하세요", null=False
    )
    
    nickname = models.CharField(max_length=10,default="")
    profile=models.ImageField(null=True,blank=True)
    coin=models.IntegerField(default=0)