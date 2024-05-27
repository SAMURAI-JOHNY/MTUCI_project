from django.db import models
from gameinfocus.models import User


class Lol(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=25)

    def __str__(self):
        return self.course_name


class LolBlocks(models.Model):
    block_id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=25)
    link = models.CharField(max_length=150)
    text = models.TextField(max_length=20000)
    course_id = models.ForeignKey(Lol, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.course_name} - {self.block_name}"


class UserLol(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    block_id = models.ForeignKey(LolBlocks, on_delete=models.CASCADE)
    block_name = models.CharField(max_length=25)
    course_name = models.CharField(max_length=25)
    status = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.course_name}: {self.block_name}'
