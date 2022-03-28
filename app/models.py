from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from cms.fields import OrderField
from cms.mixins import GetAbsoluteUrl
from pathlib import Path
#from django.contrib.auth.models import User

# from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Ticket(models.Model):
    PENDING = 1
    DONE = 2
    CHOICES = (
        (PENDING, 'Pending'),
        (DONE, 'Done'),
    )

    # user = models.ForeignKey(User,
    #                          verbose_name='User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name='Title')
    date_sent = models.DateField(
        null=True, verbose_name='Date Sent', help_text='YYYY-mm-dd')
    ticket_choices = models.PositiveSmallIntegerField(
        choices=CHOICES, default=PENDING, verbose_name='status')
    description = models.TextField(verbose_name="Description")
    order = OrderField(blank=True, verbose_name='Order #')
    waiting_for = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='waiting_for', blank=True,
                                    null=True, verbose_name='Waiting For', on_delete=models.CASCADE)
    sent_by = models.CharField(max_length=255, blank=True,
                               null=True,)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='assigned_to',
                                         blank=True,
                                         verbose_name='Assigned to')
    closed_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def assignment(self):
        return ",".join([str(p) for p in self.assigned_to.all()])

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    # def get_absolute_url(self):
    #     return reverse('app:ticket-update', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'ticket'
        ordering = ['order']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, verbose_name='Ticket')
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='User',on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False)
    order = OrderField(blank=True, for_fields=[
                       'ticket'], verbose_name='Order #')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)

    def save(self, *args, **kwargs):
        self.slug = slugify('{}-{}-{}'.format('F',
                                              self.ticket.title, self.ticket.pk))
        super().save(*args, **kwargs)

    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user

    #     super().save_model(request, obj, form, change)

    class Meta:
        db_table = 'comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('order', 'created')


class File(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, verbose_name='Ticket')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          verbose_name='User', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/', null=True,
                            blank=True, max_length=255, verbose_name='Filename')
    uploaded_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name='File uploaded at')
    order = OrderField(blank=True, for_fields=[
                       'ticket'], verbose_name='Order #')

    @property
    def filename(self):
        return Path(self.file.name).name

    def __str__(self):
        return self.filename

    def save(self, *args, **kwargs):
        if self.pk:
            old_file = File.objects.get(pk=self.pk).file
            if not old_file == self.file:
                storage = old_file.storage
                if storage.exists(old_file.name):
                    storage.delete(old_file.name)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage = self.file.storage
        if storage.exists(self.file.name):
            storage.delete(self.file.name)
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'file'
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ('order', )
