# Generated by Django 3.2 on 2021-07-27 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0009_auto_20210727_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionanswer',
            name='question_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='user_id',
            field=models.IntegerField(unique=True),
        ),
    ]
