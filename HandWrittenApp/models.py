from django.db import models
from django.contrib.auth.models import User


class PredictionImage(models.Model):
    image = models.ImageField(upload_to='predictions/')
    predicted_digit = models.IntegerField(null=True, blank=True)
    prediction_accuracy = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"

class UploadedImage(models.Model):
    # title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


# models.py


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username
