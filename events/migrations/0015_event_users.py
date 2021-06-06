# Generated by Django 2.2.4 on 2021-06-06 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0014_auto_20210606_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=2252)),
                ('password', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='title', max_length=45)),
                ('date', models.CharField(default='2012-06-06', max_length=45)),
                ('description', models.CharField(default='description', max_length=2252)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attended_by', models.ManyToManyField(related_name='attended_events', to='events.Users')),
                ('event_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_event', to='events.Users')),
            ],
        ),
    ]