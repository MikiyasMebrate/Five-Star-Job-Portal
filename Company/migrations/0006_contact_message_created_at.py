# Generated by Django 4.2.3 on 2024-04-28 05:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0005_contact_message_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_message',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
