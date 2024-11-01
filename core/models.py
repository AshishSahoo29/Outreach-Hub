from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_field):
        if not email:
            raise ValueError("User must have an email address")
        if not phone:
            raise ValueError("User must have a phone number")
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            **extra_field,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_field):
        if not email:
            raise ValueError("Admin must have an email address")
        if not phone:
            raise ValueError("Admin must have a phone number")
        user = self.create_user(email, phone, password, **extra_field)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = PhoneNumberField(region="IN", unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
