from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
# from django.db.models.query_utils import check_rel_lookup_compatibility

# Create your models here.

TYPE_CHOICES = (
    (1, "foundation"),
    (2, "non-governmental organisation"),
    (3, "local collection"),
)


class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Custom user model manager where email is the unique identifiers
        for authentication instead of usernames.
        """
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)

        # GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    """
    Overrides default User model
    """
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.PositiveSmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.PositiveIntegerField()
    city = models.CharField(max_length=256)
    zip_code = models.PositiveIntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=1024)
    user = models.ForeignKey(CustomUser, null=True, default=None, on_delete=models.CASCADE)