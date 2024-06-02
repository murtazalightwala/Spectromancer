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
    user = models.OneToOneField(primary_key = True,to = User, related_name = "user", on_delete = models.CASCADE)
    special = models.CharField(choices= special_choices, max_length = 40)
    avatar_url = models.URLField()
    mobile_number = models.CharField(max_length = 15)

    

