from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from payments.models import Student
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, role="Student", **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "Admin")
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(email, password, **extra_fields)

class Account(AbstractBaseUser,PermissionsMixin):
    # student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True,related_name='account_profile')
    account_id = models.AutoField(primary_key=True, db_column="AccountID")
    email = models.EmailField(unique=True, db_column="Email")
    password = models.CharField(max_length=100, db_column="Password")
    role = models.CharField(max_length=20, db_column="Role")
    is_active = models.BooleanField(default=True, db_column="IsActive")
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    class Meta:
        db_table = "Accounts"
    
    def __str__(self):
        return self.email

    @property
    def id(self):   # thêm cái này
        return self.account_id
    
class Tokens(models.Model):
    token_id = models.AutoField(primary_key=True, db_column="TokenID")
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="AccountID")
    access_token = models.TextField(db_column="AccessToken")
    refresh_token = models.TextField(db_column="RefreshToken")
    access_token_expiry = models.DateTimeField(db_column="AccessTokenExpiry")
    refresh_token_expiry = models.DateTimeField(db_column="RefreshTokenExpiry")
    created_at = models.DateTimeField(auto_now_add=True, db_column="CreatedAt")
    is_revoked = models.BooleanField(default=False, db_column="IsRevoked")

    class Meta:
        db_table = "Tokens"