from django.db import models
from django.conf import settings
from datetime import datetime


# Create your models here.
class newterm(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    non_answer = models.CharField(max_length=100)
    score = models.IntegerField(default=0)  # 현재까지 맞은 개수
    correct = models.BooleanField(default=False)  # 이전 문제가 맞았는지 틀렸는지
    randanswer = models.IntegerField(default=0)


class communityText(models.Model):
    date = models.DateTimeField()
    text = models.CharField(max_length=500)
    like = models.IntegerField()
    dis_like = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=30, default='')
    selected=models.BooleanField(default=False,null=True)
    def __str__(self):
        if len(self.text) > 100:
            return self.text[:100]+"..."
        else:
            return self.text


class communityComment(models.Model):
    date = models.DateTimeField()
    communitytext = models.ForeignKey(
        communityText, on_delete=models.CASCADE, default='')
    like = models.IntegerField()
    dis_like = models.IntegerField()
    text = models.CharField(max_length=300)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default='')
    getcoin=models.BooleanField(default=False,null=True)

class manner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default='')
    text = models.CharField(max_length=18)
    like = models.IntegerField()
    dis_like = models.IntegerField()
    hashtag_me = models.CharField(max_length=20)
    hashtag_you = models.CharField(max_length=20)
    hashtag_situation = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now, blank=True)
    getcoin=models.BooleanField(default=False,null=True)
    secret=models.BooleanField(default=False,null=True)

class product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default='')
    date = models.DateTimeField()
    productName = models.CharField(max_length=30, default='')
    productText = models.CharField(max_length=1000, default='')
    like = models.IntegerField()
    image = models.ImageField(upload_to='product/', null=False, blank=False)
    getcoin=models.BooleanField(default=False,null=True)
    
    def __str__(self):
        if len(self.productText)>50:
            return self.productText[:50]+"..."
        else:
            return self.productText

class certification(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    job=models.CharField(max_length=20,default='',blank=True)
    image = models.ImageField(null=True, blank=True)
    certified=models.BooleanField(default=False,null=True)

class notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default='')
    text=models.CharField(max_length=100,default='',blank=True)