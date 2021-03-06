# Generated by Django 3.0.5 on 2020-05-17 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_auto_20200515_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='photo',
            name='url',
            field=models.URLField(default=0),
        ),
        migrations.AddField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='photo_created', to=settings.AUTH_USER_MODEL),
        ),
    ]
