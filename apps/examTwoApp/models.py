from __future__ import unicode_literals
import re
from django.db import models
import bcrypt

Name_Regex = re.compile(r'^[a-zA-Z]\w+$')

# Create your models here.

class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = []
        if len(postData['name']) < 3 or len(postData['username']) < 3:
            errors.append('Name and Username cannot be fewer than 3 characters')
        if not re.match(Name_Regex, postData['name']) or not re.match(Name_Regex, postData['username']):
            errors.append('Name and Username can have only letters')
        if len(postData['password']) < 8:
            errors.append('Password is too small')
        if not (postData['password'] == postData['confirm_password']):
            errors.append('Passwords do not match')
        if not errors:
            hashing = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(10))                                  
            user = User.objects.create(
                name=postData['name'],
                username=postData['username'], 
                date_hired=postData['date_hired'], 
                password=hashing)
            return user
        return errors
    
    def validate_login(self, postData):
        errors = []
        if len(self.filter(username=postData['username'])) > 0:
            user = self.filter(username=postData['username'])[0]
            if not (bcrypt.hashpw(postData['password'].encode(), user.password.encode())):
                errors.append('Incorrect Password')
        else:
            errors.append('Incorrect Email and Password')
        if errors:
            return errors
        return user

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    date_hired = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    # magic function!
    # def __str__(self):
    #     return self.name

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_uploader = models.ForeignKey(User, related_name='uploaded')
    liked_user = models.ManyToManyField(User, related_name='liked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    # magic function!
    # def __str__(self):
    #     return (self.item_name, self.item_uploader)