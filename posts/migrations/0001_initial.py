# Generated by Django 5.0.2 on 2024-02-21 09:26

import cloudinary.models
import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoundPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=15, max_digits=20, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=15, max_digits=20, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('event_date', models.DateField(default=datetime.date.today)),
                ('date_uncertainty_days', models.CharField(choices=[('0', 'exact'), ('1', '1 day'), ('3', '3 days'), ('7', 'week'), ('14', '2 weeks'), ('30', 'month'), ('90', '3 months')], default='0', help_text='Select how much the actual event date could differ.', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LostPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=15, max_digits=20, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=15, max_digits=20, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('event_date', models.DateField(default=datetime.date.today)),
                ('date_uncertainty_days', models.CharField(choices=[('0', 'exact'), ('1', '1 day'), ('3', '3 days'), ('7', 'week'), ('14', '2 weeks'), ('30', 'month'), ('90', '3 months')], default='0', help_text='Select how much the actual event date could differ.', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
    ]