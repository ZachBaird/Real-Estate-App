# Generated by Django 2.2.2 on 2019-07-15 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_auto_20190715_1538'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inquiry',
            old_name='contact_date',
            new_name='last_updated',
        ),
    ]
