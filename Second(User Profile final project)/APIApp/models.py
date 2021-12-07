
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings

class ManageUserProfile(BaseUserManager):
    '''Manage user profile'''

    def create_user(self, email, name, password=None):
        '''create a new user'''

        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        '''create a superuser with details'''

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        return user


# our models starts from here
class UserProfile(AbstractBaseUser, PermissionsMixin):

    '''database model for users in the system.
    
    Arguments:
        AbstractBaseUser ([type]): [description]
        PermissionMixin ([type]): [Add the fields and methods necessary to support the Group and Permission model using the Model Backend.]'''

    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ManageUserProfile()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        '''Return string representation of our user.'''
        return self.email

# creating a task model for user
class Task(models.Model):
    '''Task model of user'''

    user_profile = models.ForeignKey(
        #settings.AUTH_USER_MODEL,
        UserProfile,
        on_delete=models.CASCADE,
        blank=True,
        default=None
    )

    Title = models.CharField(max_length=25)
    Description = models.TextField(max_length=100)
    Status = models.BooleanField(default=False)

    class Meta:
        db_table = 'task'

    def __str__(self):
        return self.Title