# Generated by Django 3.0.5 on 2020-05-02 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200430_1851'),
        ('list_item', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='listitem',
            unique_together={('name', 'list')},
        ),
    ]