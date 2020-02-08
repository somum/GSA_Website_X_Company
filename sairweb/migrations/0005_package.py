# Generated by Django 2.2.7 on 2019-11-27 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sairweb', '0004_auto_20191126_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pkg_name', models.CharField(default='', max_length=50)),
                ('pkg_dest_name', models.CharField(default='', max_length=50)),
                ('pkg_rating', models.CharField(default='', max_length=50)),
                ('pkg_price', models.CharField(default='', max_length=50)),
                ('pkg_desc', models.CharField(default='', max_length=50)),
                ('pkg_img', models.ImageField(default='', upload_to='sairweb/images/pkg_img')),
            ],
        ),
    ]
