# Generated by Django 2.0.8 on 2019-02-16 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=99, null=True, verbose_name='نبذة تعريفية'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='facebook',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='فيسبوك'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='github',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='جيت هب'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='رقم الهاتف'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='تويتر'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='whatsapp_mobile',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name=' رقم الهاتف واتس اب'),
        ),
    ]