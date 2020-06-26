from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Making User Model email field as unique
User._meta.get_field('email')._unique = True


class Profile(models.Model):
    """ Profile Model class. Creates Instance once user instance created """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=False)
    phone_number = models.CharField(max_length=12, blank=False)
    passport_number = models.CharField(max_length=10, blank=False)
    birth_date = models.DateField(null=True, blank=False)
    age = models.IntegerField(null=True, blank=False)
    profile_image = models.ImageField(default='default-avatar.png', upload_to='users/', null=True, blank=True)

    def __str__(self):
        return self.full_name

    @property
    def profileimageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ Post_save signal creates Profile Instance once User instance is created """
    if created:
        Profile.objects.create(
            user=instance, full_name=instance.first_name+' '+instance.last_name)
    else:
        instance.profile.save()
