# Generated by Django 4.2.3 on 2024-04-25 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0001_initial'),
        ('UserManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Company.company'),
        ),
    ]