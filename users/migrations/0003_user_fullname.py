# Generated by Django 4.2.6 on 2023-10-13 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fullname',
            field=models.CharField(blank=True, max_length=350, null=True, verbose_name='полное имя'),
        ),
    ]
