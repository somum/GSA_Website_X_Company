# Generated by Django 2.2.7 on 2019-12-24 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sairweb', '0017_remove_visainfo_ref_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visainfo',
            name='visa_img',
        ),
        migrations.CreateModel(
            name='visaInfoFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visa_img', models.FileField(default='', upload_to='sairweb/images/visa_img')),
                ('visaInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sairweb.visaInfo')),
            ],
        ),
    ]
