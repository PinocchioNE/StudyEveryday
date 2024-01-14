from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class CustomUser(AbstractUser):
    id_card = models.CharField(max_length=18, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_staff_member = models.BooleanField(default=False)
    # 新增性别字段，使用了一个选择字段
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
        ('other', '其他'),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='other')
    # 新增年龄字段
    age = models.PositiveIntegerField(null=True, blank=True)
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=15)

class Room(models.Model):
    ROOM_TYPES = (
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('SUITE', 'Suite'),
    )
    room_type = models.CharField(max_length=6, choices=ROOM_TYPES)
    room_number = models.CharField(max_length=5, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.room_number} - {self.get_room_type_display()} - ${self.price}"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_date = models.DateField(default=timezone.now)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Booking by {self.user.username} for {self.room}"

class Emergency(models.Model):
    EMERGENCY_TYPES = (
        ('loss', '物品遗失'),
        ('damage', '设施损坏'),
        ('accident', '意外事故'),
        ('other', '其他'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    emergency_type = models.CharField(max_length=10, choices=EMERGENCY_TYPES)
    description = models.TextField()
    reported_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.emergency_type}"


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}"


# class Booking(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     booked_on = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return f"{self.user} - {self.room}"