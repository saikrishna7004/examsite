# Generated by Django 3.2 on 2021-07-23 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0007_auto_20210608_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionanswer',
            name='ans_status',
            field=models.CharField(default='aamfr', max_length=10),
        ),
    ]
