# Generated by Django 2.0.8 on 2019-02-17 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_read_articles'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_lecture',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]