# Generated by Django 4.2 on 2024-10-31 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_venue_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
