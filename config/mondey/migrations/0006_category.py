# Generated by Django 2.2.5 on 2019-10-27 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mondey', '0005_auto_20191012_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.EmailField(max_length=20, unique=True)),
            ],
        ),
    ]
