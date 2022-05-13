# Generated by Django 4.0.4 on 2022-04-20 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=50)),
                ('Password', models.CharField(max_length=12)),
                ('IsActive', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'master',
            },
        ),
    ]
