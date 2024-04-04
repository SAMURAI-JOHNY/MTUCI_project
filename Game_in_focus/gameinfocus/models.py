from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from .managers import UserManager


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    points = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_username(self):
        return self.username

    def tokens(self):
        pass


class Dota(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=25)

    def __str__(self):
        return self.course_name


class DotaBlocks(models.Model):
    block_id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=25)
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


class Lol(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=25)

    def __str__(self):
        return self.course_name


class LolBlocks(models.Model):
    block_id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=25)
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

    class Meta:
        ordering = ['block_id', 'course_name']