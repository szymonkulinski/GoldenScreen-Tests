# Generated by Django 3.2.10 on 2022-03-27 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_useropinion_createddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useropinion',
            name='createdDate',
            field=models.DateField(auto_now_add=True),
        ),
    ]