# Generated by Django 3.2.6 on 2022-03-28 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='user',
        ),
    ]
