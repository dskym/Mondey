# Generated by Django 2.2.5 on 2019-10-12 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mondey', '0004_user_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='token',
            new_name='firebase_token',
        ),
    ]
