# Generated by Django 3.0 on 2019-12-24 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('device_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('device_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('word', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('display_content', models.TextField()),
                ('src_content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LookUpRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lookup_amount', models.IntegerField(default=0)),
                ('last_lookup_time', models.DateTimeField(verbose_name='date published')),
                ('remembered', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('device_id', models.CharField(max_length=50, null=True)),
                ('user_id', models.IntegerField(null=True)),
                ('vocabulary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='translaterservice.Vocabulary')),
            ],
        ),
    ]
