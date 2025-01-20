from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    
    class Meta:
        db_table = "user_profile"

    special_choices = [
        ("death", "Death"),
        ("chaos", "Chaos")
    ]
    user = models.OneToOneField(to = User, primary_key = True, on_delete = models.CASCADE, related_name = "profile")
    special = models.CharField(choices= special_choices, max_length = 40)
    avatar_url = models.URLField()
    mobile_number = models.CharField(max_length = 15)

    

