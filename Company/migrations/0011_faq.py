# Generated by Django 4.2.3 on 2024-05-13 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0010_remove_company_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=70)),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
