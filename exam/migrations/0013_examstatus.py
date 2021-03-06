# Generated by Django 3.2 on 2021-08-02 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0012_auto_20210731_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('exam_id', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('time_left', models.CharField(choices=[('completed', 'Completed'), ('started', 'Started')], max_length=20)),
            ],
            options={
                'verbose_name': 'ExamStatus',
                'verbose_name_plural': 'ExamStatuses',
            },
        ),
    ]
