# Generated by Django 4.2.3 on 2024-04-26 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobPortal', '0003_job_posting_compensation_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_posting',
            name='compensation_type',
            field=models.CharField(blank=True, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly'), ('hourly', 'Hourly'), ('commission', 'Commission'), ('bonus', 'Bonus'), ('benefits', 'Benefits')], max_length=30, null=True),
        ),
    ]