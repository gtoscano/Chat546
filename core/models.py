from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_file_size, validate_image_extension


class User(AbstractUser):
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username  # Fallback to username if name is missing


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_style = models.CharField(
        max_length=20,
        choices=[
            ("identicon", "Identicon"),
            ("monsterid", "MonsterID"),
            ("wavatar", "Wavatar"),
            ("retro", "Retro"),
            ("robohash", "RoboHash"),
            ("blank", "Blank"),
        ],
        default="identicon",
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
