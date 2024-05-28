from django.db import models

from gameinfocus.models import User


# Create your models here.
class Dota(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=25)

    def __str__(self):
        return self.course_name


class DotaBlocks(models.Model):
    block_id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=25)
    link = models.CharField(max_length=150)
    text = models.TextField(max_length=20000)
    course_id = models.ForeignKey(Dota, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.course_name} - {self.block_name}"


class UserDota(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    block_id = models.ForeignKey(DotaBlocks, on_delete=models.CASCADE)
    block_name = models.CharField(max_length=25)
    course_name = models.CharField(max_length=25)
    status = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.course_name} - {self.block_name}'

    class Meta:
        ordering = ['block_id', 'course_name']