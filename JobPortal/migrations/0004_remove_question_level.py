# Generated by Django 4.2.3 on 2024-05-10 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('JobPortal', '0003_alter_candidate_skill_alter_skill_validable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='level',
        ),
    ]