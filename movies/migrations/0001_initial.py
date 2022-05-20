# Generated by Django 3.2.11 on 2022-05-20 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Productioncountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Spokenlanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('poster_path', models.TextField()),
                ('overview', models.TextField()),
                ('collection_ids', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='movies.collection')),
                ('genre_ids', models.ManyToManyField(related_name='movie_genre', to='movies.Genre')),
                ('language_ids', models.ManyToManyField(related_name='movie_spokenlanguage', to='movies.Spokenlanguage')),
                ('productioncountry_ids', models.ManyToManyField(related_name='movie_productioncountry', to='movies.Productioncountry')),
            ],
        ),
    ]
