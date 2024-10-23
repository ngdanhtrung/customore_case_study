import uuid
from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, db_index=True, unique=True)
    fullname = models.CharField(max_length=255, db_index=True, default="")
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    avatar = models.CharField(max_length=255, default="")

    USERNAME_FIELD = "username"  # email
    # REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return "%s: %s" % (self.username, self.is_active)


class TaskStatusEnum(models.TextChoices):
    PENDING = "Pending"
    COMPLETED = "Completed"


class Task(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=TaskStatusEnum.choices, default=TaskStatusEnum.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
