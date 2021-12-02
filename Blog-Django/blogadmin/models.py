from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Create your models here.



class customUserManager(BaseUserManager):
    def create_user(self, username, password, ad, soyad, yas, **extra_field):
        user = self.model(username=username, ad=ad, soyad=soyad, yas=yas,**extra_field)
        user.set_password(raw_password=password)
        user.save()

    def create_superuser(self, username, password, ad, soyad, yas, **extra_field):

        extra_field.setdefault('is_admin', True)
        extra_field.setdefault('is_yazar', True)
        user = self.model(username=username, ad=ad, soyad=soyad, yas=yas,**extra_field)

        user.set_password(raw_password=password)
        user.save()


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    username = models.CharField(max_length=40, verbose_name="Kullanıcı Adı", unique=True)
    password = models.CharField(max_length=40, verbose_name="Şifre")
    ad = models.CharField(max_length=40, verbose_name="Ad")
    soyad = models.CharField(max_length=40, verbose_name="Soyad")
    yas = models.IntegerField(verbose_name="Yaş")
    is_admin = models.BooleanField(default=False, verbose_name="Admin?")
    is_yazar = models.BooleanField(default=False, verbose_name="Yazar mı?")

    objects=customUserManager()

    REQUIRED_FIELDS=["ad","soyad","yas"]
    USERNAME_FIELD="username"
    def __str__(self) -> str:
        return self.username
