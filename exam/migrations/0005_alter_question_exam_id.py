# Generated by Django 3.2 on 2021-06-01 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_question_exam_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='exam_id',
            field=models.IntegerField(),
        ),
    ]
