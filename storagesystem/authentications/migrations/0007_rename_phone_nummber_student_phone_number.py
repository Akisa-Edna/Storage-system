# Generated by Django 4.2.6 on 2023-10-31 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0006_rename_phone_storageprovider_phone_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='phone_nummber',
            new_name='phone_number',
        ),
    ]
