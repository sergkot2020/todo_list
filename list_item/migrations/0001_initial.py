# Generated by Django 2.2.2 on 2020-04-21 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_done', models.BooleanField(default=False)),
                ('priority', models.SmallIntegerField(default=0, verbose_name='Приоритет')),
                ('expire_date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ListModel', verbose_name='Список дел')),
            ],
            options={
                'verbose_name': 'Элемент списка',
            },
        ),
    ]
