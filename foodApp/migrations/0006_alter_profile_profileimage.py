# Generated by Django 4.0.4 on 2022-04-26 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodApp', '0005_alter_profile_profileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ProfileImage',
            field=models.FileField(default='images/users/user.png', upload_to='images/users'),
        ),
    ]
