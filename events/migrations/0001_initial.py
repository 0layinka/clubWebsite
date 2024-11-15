# Generated by Django 4.2 on 2024-10-30 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Venue Name')),
                ('adress', models.CharField(max_length=300)),
                ('zip_code', models.CharField(max_length=15, verbose_name='Zip Code')),
                ('phone', models.CharField(blank=True, max_length=25, verbose_name='Phone Number')),
                ('web', models.URLField(blank=True, verbose_name='Website Adress')),
                ('email', models.CharField(blank=True, max_length=200, verbose_name='Email Adress')),
                ('owner', models.IntegerField(default=1, verbose_name='Venue Owner')),
            ],
        ),
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Event Name')),
                ('date', models.DateTimeField(max_length=200, verbose_name='Event date')),
                ('description', models.TextField(blank=True, null=True)),
                ('attendees', models.ManyToManyField(blank=True, related_name='attenddees', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(blank=True, max_length=150, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager', to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.venue')),
            ],
        ),
    ]
