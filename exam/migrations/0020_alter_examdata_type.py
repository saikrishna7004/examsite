# Generated by Django 3.2 on 2021-08-12 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0019_examdata_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examdata',
            name='type',
            field=models.CharField(default='custom-21', max_length=10),
        ),
    ]
