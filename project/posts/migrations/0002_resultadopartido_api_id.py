# Generated by Django 5.1.2 on 2024-11-24 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultadopartido',
            name='api_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
