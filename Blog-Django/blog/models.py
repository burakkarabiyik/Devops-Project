from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.utils.text import slugify
import string
import random
# Create your models here.




def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class Post(models.Model):
    user = models.ForeignKey(
        'blogadmin.User', related_name='post', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="Başlık")
    content = models.TextField(max_length=2000, verbose_name="İçerik")
    publishing_date = models.DateTimeField(
        verbose_name="Yayın Tarihi", auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to="post")
    slug = models.SlugField(unique=True, editable=False, max_length=130)
    status = models.TextField(verbose_name="Kategori isim", max_length=15)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.title)
            super(Post, self).save(*args, **kwargs)
        else:
            super(Post, self).save(*args, **kwargs)


class Meta:
    ordering = ['-publishing_date', 'id']


class MyCategories(models.Model):
    categoryname = models.CharField(
        max_length=50, verbose_name="Kategori ismi")

    def __str__(self) -> str:
        return self.categoryname
