from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    headline = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    text = models.CharField(max_length=4096)
    category = models.ForeignKey(Category, null=True, default=None, on_delete=models.CASCADE, related_name="Category")
    image = models.ImageField(upload_to='article_images/%Y/%m/%d', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author_profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline


class Event(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    date = models.DateField()
    image = models.ImageField(upload_to='event_images/%Y/%m/%d', blank=True)
    address = models.CharField(max_length=255, default="null")  # Адрес события
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)  # Широта
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)  # Долгота

    def __str__(self):
        return self.title
