# Generated by Django 3.2 on 2021-08-22 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserVerifyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=15, unique=True)),
                ('verified', models.BooleanField()),
                ('otp', models.IntegerField()),
            ],
            options={
                'verbose_name': 'UserVerifyData',
                'verbose_name_plural': 'UserVerifyDatas',
            },
        ),
    ]
