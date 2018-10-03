# Generated by Django 2.1.1 on 2018-09-30 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Boardgame',
            fields=[
                ('name', models.TextField()),
                ('rating', models.FloatField()),
                ('ranking', models.IntegerField()),
                ('minNumPlayers', models.IntegerField()),
                ('maxNumPlayers', models.IntegerField()),
                ('playTime', models.IntegerField()),
                ('complexityWeight', models.FloatField()),
                ('bggId', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('bggUrl', models.TextField()),
                ('numRatings', models.IntegerField()),
            ],
        ),
    ]