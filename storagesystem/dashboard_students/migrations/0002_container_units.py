# Generated by Django 4.2.6 on 2023-10-27 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='units',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
