# Generated by Django 4.0 on 2022-05-04 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liked', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]