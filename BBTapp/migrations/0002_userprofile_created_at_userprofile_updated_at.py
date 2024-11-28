# Generated by Django 5.1.3 on 2024-11-28 08:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BBTapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userprofile",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
