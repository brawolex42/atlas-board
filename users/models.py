from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import StrEnum

class UserPositions(StrEnum):
    CEO = "CEO"
    CTO = "CTO"
    DESIGNER = "Designer"
    PRODUCT_OWNER = "Product Owner"
    PROJECT_OWNER = "Project Owner"
    BACKEND_DEVELOPER = "Backend Developer"
    FRONTEND_DEVELOPER = "Frontend Developer"
    IOS_DEVELOPER = "iOS Developer"
    MOBILE_DEVELOPER = "Mobile Developer"
    DEVOPS_ENGINEER = "DevOps Engineer"
    DATA_SCIENTIST = "Data Scientist"
    DATA_ENGINEER = "Data Engineer"
    DATABASE_ADMIN = "Database Admin"
    ML_ENGINEER = "ML Engineer"
    PROJECT_MANAGER = "Project Manager"
    QA = "QA"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

class CustomUserManager(models.Manager):
    def create_user(self, email, username, first_name, last_name, position=UserPositions.BACKEND_DEVELOPER, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        if not username:
            raise ValueError(_('Username is required'))
        if len(first_name) < 2:
            raise ValueError(_('First name must be at least 2 characters'))
        if len(last_name) < 2:
            raise ValueError(_('Last name must be at least 2 characters'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, position=position.name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, position=UserPositions.BACKEND_DEVELOPER, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, first_name, last_name, position, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=50, unique=True)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    position = models.CharField(_('position'), max_length=50, choices=UserPositions.choices(), default=UserPositions.BACKEND_DEVELOPER.name)

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), null=True, blank=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    deleted = models.BooleanField(_('deleted'), default=False)
    deleted_at = models.DateTimeField(_('deleted at'), null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'position']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"