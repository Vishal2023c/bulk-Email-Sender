# Generated by Django 5.0.3 on 2024-03-25 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_receiverfilemodel_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiverfilemodel',
            name='file',
            field=models.FileField(upload_to='media'),
        ),
        migrations.AlterField(
            model_name='senderfilemodel',
            name='file',
            field=models.FileField(upload_to='media'),
        ),
    ]
