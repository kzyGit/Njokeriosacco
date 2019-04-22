from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, first_name, middle_name, sur_name,
                    id_number):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        self.first_name = first_name
        self.middle_name = middle_name
        self.sur_name = sur_name
        self.id_number = id_number
        user = self.model(
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            sur_name=sur_name,
            id_number=id_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email,
                         first_name,
                         middle_name,
                         sur_name,
                         id_number,
                         password=None):
        user = self.create_user(email, password, first_name, middle_name,
                                sur_name, id_number)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=False, max_length=100, unique=True)
    password = models.CharField(blank=False, max_length=100)
    first_name = models.CharField(blank=False, max_length=100)
    middle_name = models.CharField(blank=False, max_length=100)
    sur_name = models.CharField(blank=False, max_length=100)
    id_number = models.IntegerField(blank=False, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'sur_name', 'id_number']

    def __str__(self):
        return "{} {}".format(self.first_name, self.sur_name)


class CommonFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Savings(CommonFields):
    amount = models.IntegerField(blank=False, default=0)
    user = models.ForeignKey(
        User, related_name='user', on_delete=models.CASCADE)
    mode = models.CharField(default='cash', blank=False, max_length=100)


class Loans(CommonFields):
    amount = models.IntegerField(blank=False, default=0)
    user = models.ForeignKey(
        User, related_name='loaner', on_delete=models.CASCADE)
    status = models.CharField(default='pending', blank=False, max_length=100)


class LoanRepayment(CommonFields):
    amount = models.IntegerField(blank=False, default=0)
    loan = models.ForeignKey(
        Loans, related_name='loan', on_delete=models.CASCADE)
