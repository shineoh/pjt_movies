# Generated by Django 3.2.9 on 2022-05-26 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_moviecomment_rank'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moviecomment',
            old_name='rank',
            new_name='rating',
        ),
    ]
