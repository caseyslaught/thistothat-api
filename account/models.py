
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

from thistothat.common import get_utc_datetime_now


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        email = self.normalize_email(email).lower()
        account = self.model(email=email, **extra_fields)

        account.set_password(password)
        account.save(using=self._db)
        return account


class Account(AbstractBaseUser, PermissionsMixin):

    datetime_created = models.DateTimeField(default=get_utc_datetime_now)
    datetime_updated = models.DateTimeField(null=True)
    datetime_deleted = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    email = models.EmailField(unique=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['email']

    def __str__(self):
        return f'{self.email}'

