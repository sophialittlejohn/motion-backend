import random
import string

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def code_generator(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class Profile(models.Model):
    user = models.OneToOneField(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    followees = models.ManyToManyField(
        verbose_name='followees',
        to=settings.AUTH_USER_MODEL,
        blank=True,
        related_name='followers',
    )
    registration_code = models.CharField(
        verbose_name='registration code',
        max_length=15,
        # unique=True,
        default=code_generator,
    )
    profile_pic = models.FileField(
        upload_to='profile_pics/',
        blank=True
    )

    def generate_new_code(self):
        self.registration_code = code_generator()
        self.save()


# when user is created this automatically creates the profile for the user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()


class Post(models.Model):
    """
    Get access to likes by calling post.likes.all()
    """
    content = models.TextField(
        verbose_name='content'
    )
    user = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='posts',
    )
    created = models.DateTimeField(
        verbose_name='created',
        auto_now_add=True,
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created']


class Like(models.Model):
    user = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    post = models.ForeignKey(
        verbose_name='post',
        to='feed.Post',
        # when post is deleted the likes also go away
        on_delete=models.CASCADE,
        related_name='likes',
    )

    # meta classes are information about our models for django
    class Meta:
        # takes a list of tuples: these are the fields that are created but not on the database level
        unique_together = [
            ('user', 'post'),
        ]


class Friendship(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    STATUS_CHOICES = [
        (PENDING, 'Friend request pending'),
        (ACCEPTED, 'Friend request accepted'),
        (DECLINED, 'Friend request declined')
    ]

    sender = models.ForeignKey(
        verbose_name='sender',
        to=settings.AUTH_USER_MODEL,
        blank=True,
        related_name='friend_request',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        verbose_name='receiver',
        to=settings.AUTH_USER_MODEL,
        blank=True,
        related_name='friend_requested',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        verbose_name='status',
        choices=STATUS_CHOICES,
        default=PENDING,
        max_length=10,
    )
