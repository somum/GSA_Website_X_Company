# Generated by Django 2.2.7 on 2019-12-11 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sairweb', '0008_destination_dest_created_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='wadmin',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(default='', max_length=50)),
                ('password', models.CharField(default='', max_length=50)),
                ('email', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
