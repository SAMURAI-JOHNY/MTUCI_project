from django.db import models
from django.core.validators import MinLengthValidator


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    avatar = models.ImageField()
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Courses(models.Model):
    course_block_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class Usercourses(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_block_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    status = models.BooleanField(default=0)


    class Meta:
        order_with_respect_to = 'user_id'