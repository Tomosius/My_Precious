# Generated by Django 5.0.2 on 2024-02-28 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['created_at']},
        ),
    ]
