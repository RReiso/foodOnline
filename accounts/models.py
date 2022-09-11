from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


# will contain only methods
class UserManager(BaseUserManager):
  # These methods are called when you use commands like python manage.py createsuperuser
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email')
        if not username:
            raise ValueError('User must have a username')

        # self.model refers to User model
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)  # encodes, using SHA

        # self._db refers to default db to store the user
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email')
        if not username:
            raise ValueError('User must have a username')

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        # self._db refers to default db to store the user
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):  # will contain fields
    RESTAURANT = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (RESTAURANT, 'Restaurant'),
        (CUSTOMER, 'Customer'),
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICE, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # will use email as login field
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()  # tells which manager should be used for this model

    def __str__(self):  # string representation of model in admin panel
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin  # returns boolean

    def has_module_perms(self, app_label):
        return True


class UserProfile(models.Model):
    # one user profile belongs to one user
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(
        upload_to='users/cover_pictures', blank=True, null=True)
    address_line_1 = models.CharField(max_length=200, blank=True, null=True)
    address_line_2 = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.CharField(max_length=30, blank=True, null=True)
    longitude = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
