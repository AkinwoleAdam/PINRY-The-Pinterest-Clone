# Generated by Django 4.1 on 2022-09-29 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pin', '0002_alter_board_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='status',
            field=models.CharField(blank=True, choices=[('private', 'private'), ('public', 'public')], default='public', max_length=200, null=True),
        ),
    ]
