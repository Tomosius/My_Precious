# Generated by Django 5.0.2 on 2024-02-19 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='biography',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=50)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='users.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='SocialMediaLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField()),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media_links', to='users.userprofile')),
            ],
        ),
    ]
