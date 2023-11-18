# Generated by Django 4.2.6 on 2023-11-02 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0008_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, unique=True)),
                ('is_in_use', models.BooleanField(default=False)),
            ],
        ),
    ]
