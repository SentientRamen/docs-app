# Generated by Django 3.0.4 on 2020-04-03 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0002_auto_20200403_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdocumentinfo',
            name='last_visited',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]