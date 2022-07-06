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

class Category(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Group(models.Model):
    name = models.CharField(max_length=45)
    desc = models.CharField(max_length=255)
    member = models.ManyToManyField(User, related_name='group_members')
    creator = models.ForeignKey(User, related_name='created_groups', on_delete=models.CASCADE, null=True)
    gr_admin = models.ManyToManyField(User, related_name='admin_members', default=None)
    active_group = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Recipe(models.Model):
    rec_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='cat_recipes', max_length=45, on_delete=models.CASCADE)
    prep_time = models.CharField(max_length=20)
    procedure = models.CharField(max_length=1000, null=True)
    ingredients = models.TextField(max_length=455, null=True)
    creator = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE, null=True)
    favorite = models.ManyToManyField(User, related_name='fav_recipes')
    group_rec = models.ForeignKey(Group, related_name='group_recs', on_delete=models.CASCADE, default=None)
    notes = models.TextField(max_length=455, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TestRec(models.Model):
    rec_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='test_cat_recipes', max_length=45, on_delete=models.CASCADE)
    prep_time = models.CharField(max_length=20)
    procedure = models.CharField(max_length=1000, null=True)
    ingredients = models.TextField(max_length=455, null=True)
    creator = models.ForeignKey(User, related_name='test_recipes', on_delete=models.CASCADE, null=True)
    notes = models.TextField(max_length=455, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='images', default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    for_recipe = models.ForeignKey(Recipe, related_name='images', on_delete=models.CASCADE, null=True)
    profile_pic = models.ForeignKey(User, related_name='profile_pics', on_delete=models.CASCADE, null=True)
    knife_roll_pic = models.ForeignKey(User, related_name='kn_ro_pics', on_delete=models.CASCADE, null=True)
    wall_pic = models.ForeignKey(User, related_name='wall_pics', on_delete=models.CASCADE, null=True)


class Post(models.Model):
    post_title = models.CharField(max_length=45)
    content = models.CharField(max_length=455)
    post_image = models.OneToOneField(Image, on_delete=models.CASCADE, primary_key=True,)
    poster = models.ForeignKey(User, related_name='my_posts', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Suggestion(models.Model):
    rec_name = models.CharField(max_length=255)
    category = models.CharField(max_length=45)
    prep_time = models.CharField(max_length=20)
    procedure = models.CharField(max_length=455)
    ingredients = models.TextField(max_length=455)
    link = models.OneToOneField(Recipe, related_name='links', on_delete=models.CASCADE)
    helper = models.ForeignKey(User, related_name='help', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Invite(models.Model):
    sender = models.OneToOneField(User, on_delete=models.CASCADE)
    for_group = models.ForeignKey(Group, related_name='requests', on_delete=models.CASCADE)
    msg_txt = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
