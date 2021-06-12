from django.db import models
import re
from datetime import date

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        users = User.objects.all()
        if len(postData['first_name']) < 2:
            errors['firt_name'] = 'First name must be at least 2 characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'
        for user in users:
            if (postData ['email']) == user.email:
                errors['email'] = 'User already exists'
        if (postData ['pass_confirm']) != (postData ['password']):
            errors['pass_confirm'] = 'Passwords must match'
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = (postData ['email']))
        if not user:
            errors['email'] = 'Email not yet registered'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    pass_confirm = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()