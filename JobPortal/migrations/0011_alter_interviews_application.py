# Generated by Django 4.2.3 on 2024-05-03 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JobPortal', '0010_alter_application_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviews',
            name='application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application', to='JobPortal.application'),
        ),
    ]