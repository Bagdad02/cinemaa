# Generated by Django 4.0 on 2022-05-04 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('movies', '0003_alter_movie_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='owner',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='ЛАЙК')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='movies.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to='account.customuser')),
            ],
            options={
                'unique_together': {('movie', 'user')},
            },
        ),
    ]
