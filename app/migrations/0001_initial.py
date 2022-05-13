# Generated by Django 3.2.6 on 2022-05-13 10:01

import cms.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.NOTIFICATIONS_NOTIFICATION_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('title', models.CharField(max_length=255, verbose_name='Folder')),
                ('slug', models.SlugField(default='')),
                ('order', cms.fields.OrderField(blank=True, verbose_name='Order #')),
            ],
            options={
                'verbose_name': 'Folder',
                'verbose_name_plural': 'Folders',
                'db_table': 'folder',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='NotificationCTA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cta_link', models.CharField(blank=True, max_length=200)),
                ('notification', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.NOTIFICATIONS_NOTIFICATION_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('date_sent', models.DateField(help_text='YYYY-mm-dd', null=True, verbose_name='Date')),
                ('memo_choices', models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'Closed')], default=1, verbose_name='status')),
                ('description', models.TextField(verbose_name='Content')),
                ('order', cms.fields.OrderField(blank=True, verbose_name='Order #')),
                ('sent_by', models.CharField(blank=True, max_length=255, null=True, verbose_name='Sender')),
                ('assigned_to', models.ManyToManyField(blank=True, related_name='assigned_to', to=settings.AUTH_USER_MODEL, verbose_name='Assigned')),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.folder', verbose_name='Folder')),
                ('waiting_for', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='waiting_for', to=settings.AUTH_USER_MODEL, verbose_name='Waiting For')),
            ],
            options={
                'verbose_name': 'Memo',
                'verbose_name_plural': 'Memos',
                'db_table': 'memo',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('file', models.FileField(blank=True, max_length=255, null=True, upload_to='files/', verbose_name='Filename')),
                ('order', cms.fields.OrderField(blank=True, verbose_name='Order #')),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.memo', verbose_name='Memo')),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
                'db_table': 'file',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField(editable=False)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug')),
                ('comment', models.TextField(verbose_name='Comment')),
                ('order', cms.fields.OrderField(blank=True, verbose_name='Order #')),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.memo', verbose_name='Memo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'db_table': 'comment',
                'ordering': ('order', 'last_modified'),
            },
        ),
    ]
