# Generated by Django 4.0.3 on 2022-04-05 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0021_alter_questionanswer_question_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='examdata',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
