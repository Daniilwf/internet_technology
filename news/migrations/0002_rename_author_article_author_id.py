# Generated by Django 5.0.3 on 2024-03-13 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='author',
            new_name='author_id',
        ),
    ]
