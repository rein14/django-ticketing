from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from cms.fields import OrderField
from cms.mixins import GetAbsoluteUrl
from pathlib import Path
#from django.contrib.auth.models import User
import random
# from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import Group


from django.utils import timezone
from django.db import models
from notifications.models import notify_handler
from notifications.signals import notify
from notifications.models import Notification

# Create your models here.


class NotificationCTA(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    cta_link = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.cta_link)


def custom_notify_handler(*args, **kwargs):
    notifications = notify_handler(*args, **kwargs)
    cta_link = kwargs.get("cta_link", "")
    for notification in notifications:
        NotificationCTA.objects.create(notification=notification, cta_link=cta_link)
    return notifications


notify.disconnect(notify_handler, dispatch_uid='notifications.models.notification')
notify.connect(custom_notify_handler)  # , dispatch_uid='notifications.models.notification')



class TimeStamped(models.Model):
    creation_date = models.DateTimeField(editable=False)
    last_modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now()

        self.last_modified = timezone.now()
        return super(TimeStamped, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Folder(TimeStamped):
    title = models.CharField(max_length=255, verbose_name='Folder')
    slug = models.SlugField(default="")
    order = OrderField(blank=True, verbose_name='Order #')
    # group = models.ForeignKey(Group, on_delete=models.CASCADE)
 
    def __str__(self):
        return self.title

    def save(self):
        self.slug =  slugify('{}'.format(self.title))
        return super().save()

    class Meta:
        db_table = 'folder'
        verbose_name = 'Folder'
        verbose_name_plural = "Folders"
        ordering = ('order', )

    # def get_absolute_url(self):
    #     return reverse("app:memo-list", kwargs={"folder": self.id})

    def get_absolute_url(self):
        return reverse('app:folder-detail', kwargs={'pk': self.id})


class Memo(TimeStamped):
    PENDING = 1
    CLOSED = 2
    CHOICES = (
        (PENDING, 'Pending'),
        (CLOSED, 'Closed'),
    )
    folder = models.ForeignKey(Folder, verbose_name='Folder', on_delete=models.CASCADE,null=False,blank=False)
    # user = models.ForeignKey(User,
    #                          verbose_name='User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name='Title')
    date_sent = models.DateField(
        null=True, verbose_name='Date', help_text='YYYY-mm-dd')
    memo_choices = models.PositiveSmallIntegerField(
        choices=CHOICES, default=PENDING, verbose_name='status')
    description = models.TextField(verbose_name="Content")
    order = OrderField(blank=True, verbose_name='Order #')
    waiting_for = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='waiting_for', blank=True,
                                    null=True, verbose_name='Waiting For', on_delete=models.CASCADE)
    sent_by = models.CharField(max_length=255, blank=True,
                               null=True, verbose_name="Sender")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='assigned_to',
                                         blank=True,
                                         verbose_name='Assigned')
   

    def __str__(self):
        return self.title

    def userassignment(self):
        return ",".join([str(p) for p in self.assigned_to.all()])

    def save(self, *args, **kwargs):
        # self.assignment = [str(p) for p in self.assigned_to.all()]
        super().save(*args, **kwargs)

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    # def get_absolute_url(self):
    #     return reverse("todo:task_detail", kwargs={"task_id": self.id})

    # @staticmethod
    # def get_products_by_id(ids):
    #     return Memo.objects.filter(id__in=ids)

    # @staticmethod
    # def get_all_products():
    #     return Memo.objects.all()

    # @staticmethod
    # def get_all_products_by_categoryid(folder_id):
    #     if folder_id:
    #         return Memo.objects.filter(folder=folder_id)
    #     else:
    #         return Memo.get_all_products()

    # def get_absolute_url(self):
    #    return reverse('app:memo-update', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'memo'
        ordering = ['order']
        verbose_name = 'Memo'
        verbose_name_plural = 'Memos'

    def get_absolute_url(self):
        return reverse('app:memo-list')


class Comment(TimeStamped):
    memo = models.ForeignKey(
        Memo, on_delete=models.CASCADE, verbose_name='Memo')
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='User', on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False, verbose_name='Comment')
    order = OrderField(blank=True, for_fields=[
                       'memo'], verbose_name='Order #')

    def __str__(self):
        return str(self.slug)

    def save(self, *args, **kwargs):
        self.slug = slugify('{}-{}'.format('F', random.random(),
                                           self.memo.pk))
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("app:comment-list", kwargs={"memo": self.memo})

    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #     super().save_model(request, obj, form, change)

    # def get_absolute_url(self):
    #     return reverse("comment_detail", kwargs={"pk": self.pk})

    class Meta:
        db_table = 'comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('order', 'last_modified')


class File(TimeStamped):
    memo = models.ForeignKey(
        Memo, on_delete=models.CASCADE, verbose_name='Memo')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          verbose_name='User', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/', null=True,
                            blank=True, max_length=255, verbose_name='Filename')
    
    order = OrderField(blank=True, for_fields=[
                       'memo'], verbose_name='Order #')

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


































