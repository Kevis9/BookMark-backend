# Generated by Django 3.2 on 2021-04-29 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='like_num',
        ),
    ]
