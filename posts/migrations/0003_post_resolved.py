# Generated by Django 5.0.2 on 2024-04-14 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='resolved',
            field=models.BooleanField(default=False, help_text='Indicates whether the post has been resolved.'),
        ),
    ]
