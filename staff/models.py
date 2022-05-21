from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from staff.managers import UserManager
from django.utils.translation import gettext_lazy as _
from branches.models import Branch


class Staff(AbstractUser):

    first_name = models.CharField(verbose_name=_('First Name'), blank=False, max_length=100)
    last_name = models.CharField(verbose_name=_('Last Name'), blank=False, max_length=100)
    national_id = models.IntegerField(verbose_name=_('National ID Number'), null=True)
    phone_number = models.CharField(max_length=50, unique=True, verbose_name=_('Phone Number'))
    email = models.EmailField(verbose_name=_('Email'), unique=True, max_length=100, blank=False)
    username = models.CharField(verbose_name=_('User name'), max_length=50, blank=True, null=True)
    branch = models.ForeignKey(Branch, blank=True, null=True, on_delete=models.PROTECT)
    email_confirmed = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    dob = models.DateField(verbose_name=_('Date of birth'), max_length=250, blank=True, default='1990-01-01')
    nationality = models.CharField(verbose_name=_('Nationality'), max_length=50, blank=True, null=True, default='Kenyan')
    postal_address = models.CharField(verbose_name=_('Postal address'), max_length=200, blank=True, null=True)
    city = models.CharField(verbose_name=_('City'), max_length=200, blank=True, null=True)
    street = models.CharField(verbose_name=_('Street or road'), max_length=200, blank=True, null=True)
    house = models.CharField(verbose_name=_('House or plot number'), max_length=200, blank=True, null=True)
    occupation = models.CharField(verbose_name=_('Occupation'), max_length=200, blank=True, null=True)
    employer = models.CharField(verbose_name=_('Employer'), max_length=250, blank=True)
    marital_status = models.CharField(
        verbose_name=_('Marital Status'),
        max_length=50,
        choices=(
            ('single', _('Single')),
            ('married', _('Married')),
            ('divorced', _('Divorced')),
            ('other', _('Other')),
        ),
        default='single'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['national_id', 'first_name', 'last_name', 'phone_number']

    class Meta:

        verbose_name = _('staff')
        verbose_name_plural = _('staff')

    def validate_staff_email(self, email=''):
        staff = Staff.objects.get(email=email)
        if staff:
            raise ValidationError(
                _('%(email)s already exist'),
                params={'email': email},
            )

    def get_short_name(self):
        '''
        Returns the last name for the user.
        '''
        return self.last_name

    def __str__(self):
        return self.get_full_name()

