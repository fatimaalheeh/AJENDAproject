# Generated by Django 2.2.4 on 2021-06-06 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20210606_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.CharField(default='2012-06-06', max_length=45),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(default='description', max_length=2252),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(default='title', max_length=45),
        ),
    ]