# Generated by Django 5.1.3 on 2024-11-28 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExecutionModel',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('keys', models.CharField(db_index=True, max_length=50)),
                ('value', models.TextField()),
            ],
        ),
    ]
