from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.query_utils import check_rel_lookup_compatibility

# Create your models here.
TYPE_CHOICES = (
    (1, "foundation"),
    (2, "non-governmental organisation"),
    (3, "local collection"),
)


class User(AbstractUser):
    """
    Overrides default User model
    """
    pass


class Category(models.Model):
    name = models.CharField(max_length=256)


class Institution(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.PositiveSmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.PositiveIntegerField()
    city = models.CharField(max_length=256)
    zip_code = models.PositiveSmallIntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=1024)
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)