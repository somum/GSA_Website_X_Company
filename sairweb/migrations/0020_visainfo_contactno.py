# Generated by Django 2.2.7 on 2020-01-27 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sairweb', '0019_visainfo_vcountry'),
    ]

    operations = [
        migrations.AddField(
            model_name='visainfo',
            name='contactNo',
            field=models.CharField(default='', max_length=50),
        ),
    ]
