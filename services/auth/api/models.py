from django.db import models

class User(models.Model):
    ## normal user model
    username = models.CharField(max_length=255, unique=True , null=True)
    email = models.EmailField(max_length=255, unique=True , null=True)
    password = models.CharField(max_length=255 , null=True)
    
    ## 42 user model
    username_42 = models.CharField(max_length=255, unique=True, null=True)
    email_42 = models.EmailField(max_length=255, unique=True, null=True)

    ## common user model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_authenticated = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'
        ordering = ['created_at']
        unique_together = ['email', 'username']
    