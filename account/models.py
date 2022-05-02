from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


# class Role(models.Model):
#     '''
#     The Role entries are managed by the system,
#     automatically created via a Django data migration.
#     '''
#     SECRETARY = 1
#     DIRECTOR = 2
#     ADMINISTRATOR = 3
#     STAFF = 4
#     ADMIN = 5

#     ROLE_CHOICES = (
#         (SECRETARY, 'Secretary'),
#         (DIRECTOR, 'Director'),
#         (ADMINISTRATOR, 'Administrator'),
#         (STAFF, 'Staff'),
#         (ADMIN, 'Admin')
#     )

#     id = models.PositiveSmallIntegerField(
#         choices=ROLE_CHOICES, primary_key=True)

#     def __str__(self):
#         return self.get_id_display()

ROLE_CHOICES = (
    ('REGISTRAR', 'Registrar'),
    ('STAFF', 'Staff'),
    ('COMMISSIONER', 'Commissioner'),
)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_cleared = models.BooleanField(_('cleared'), default=False)
    full_names = models.CharField(_('full name'), max_length=30, blank=True)
    #be_owner = models.BooleanField(_('full name'), default=False)
    
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    roles = models.CharField(choices=ROLE_CHOICES, max_length=150)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        self.full_names = '%s %s' % (self.first_name, self.last_name)
        super().save(*args, **kwargs)

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return 'Mr.' + ' ' + self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
